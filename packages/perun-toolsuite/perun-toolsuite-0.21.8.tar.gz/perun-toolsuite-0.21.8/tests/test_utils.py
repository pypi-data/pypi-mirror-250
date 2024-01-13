"""Basic tests for utility package and sanity checks"""

import glob
import pkgutil
import os
import re
import subprocess
import signal
import sys

import pytest

import perun.utils as utils
import perun.vcs as vcs
import perun.collect as collect
import perun.postprocess as postprocess
import perun.logic.config as config
import perun.logic.commands as commands
import perun.view as view
import perun.utils.helpers as helpers
import perun.testing.asserts as asserts
import perun.utils.log as log
from perun.utils.exceptions import (
    SystemTapScriptCompilationException,
    SystemTapStartupException,
    ResourceLockedException,
    UnsupportedModuleFunctionException,
)
from perun.collect.trace.optimizations.structs import Complexity

from perun.utils.structs import Unit, OrderedEnum
from perun.utils.helpers import HandledSignals


def assert_all_registered_modules(package_name, package, must_have_function_names):
    """Asserts that for given package all of its modules are properly registered in Perun

    Moreover checks that all of the must have functions are implemented as well.

    Arguments:
        package_name(str): name of the package we are checking all the modules
        package(module): checked package
        must_have_function_names(list): list of functions that the module from package has to have
          registered
    """
    registered_modules = utils.get_supported_module_names(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        module = utils.get_module(module_name)
        for must_have_function_name in must_have_function_names:
            assert hasattr(module, must_have_function_name) and "Missing {} in module {}".format(
                must_have_function_name, module_name
            )

        # Each module has to be registered in get_supported_module_names
        unit_name = module_name.split(".")[-1]
        assert unit_name in registered_modules and "{} was not registered properly".format(
            module_name
        )


def assert_all_registered_cli_units(package_name, package, must_have_function_names):
    """Asserts that for given package all of its modules are properly registered in Perun

    Moreover checks that it has the CLI interface function in order to be called through click,
    and that certain functions are implemented as well (namely collect/postprocess) in order
    to automate the process of profile generation and postprocessing.

    Arguments:
        package_name(str): name of the package we are checking all the modules
        package(module): checked package (one of collect, postprocess, view)
        must_have_function_names(list): list of functions that the module from package has to have
          registered
    """
    registered_modules = utils.get_supported_module_names(package_name)
    for _, module_name, _ in pkgutil.iter_modules(package.__path__, package.__name__ + "."):
        # Each module has to have run.py module
        module = utils.get_module(module_name)
        assert hasattr(module, "run") and "Missing module run.py in the '{}' module".format(
            package_name
        )
        run_module = utils.get_module(".".join([module_name, "run"]))
        for must_have_function_name in must_have_function_names:
            assert (
                not must_have_function_name
                or hasattr(run_module, must_have_function_name)
                and "run.py is missing '{}' function".format(must_have_function_name)
            )

        # Each module has to have CLI interface function of the same name
        unit_name = module_name.split(".")[-1]
        assert hasattr(run_module, unit_name) and "{} is missing CLI function point".format(
            unit_name
        )

        # Each module has to be registered in get_supported_module_names
        # Note: As of Click 7.0 we have to (de)sanitize _ and -
        assert Unit.desanitize_unit_name(
            unit_name
        ) in registered_modules and "{} was not registered properly".format(module_name)


def test_get_supported_modules():
    """Test whether all currently compatible modules are registered in the function

    This serves and sanity check for new modules that could be added in future. Namely it checks
    all of the collectors, postprocessors and view that they can be used from the CLI and also
    tests that VCS modules can be used as a backend for perun.

    Expecting no errors and every supported module registered in the function
    """
    # Check that all of the internal modules (vcs) are properly registered and has interface for
    # concrete functions.
    assert_all_registered_modules(
        "vcs",
        vcs,
        [
            "_init",
            "_get_minor_head",
            "_walk_minor_versions",
            "_walk_major_versions",
            "_get_minor_version_info",
            "_get_head_major_version",
            "_check_minor_version_validity",
            "_massage_parameter",
        ],
    )

    # Check that all of the CLI units (collectors, postprocessors and visualizations) are properly
    # registered.
    assert_all_registered_cli_units("collect", collect, ["collect"])
    assert_all_registered_cli_units("postprocess", postprocess, ["postprocess"])
    assert_all_registered_cli_units("view", view, [])


def test_paging_and_config(monkeypatch, capsys):
    """Helper function for testing various configs of paging through turn_off_paging_wrt_config"""
    cfg = config.Config("shared", "", {"general": {"paging": "always"}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert commands.turn_off_paging_wrt_config("status")
    assert commands.turn_off_paging_wrt_config("log")

    cfg = config.Config("shared", "", {"general": {"paging": "only-log"}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert not commands.turn_off_paging_wrt_config("status")
    assert commands.turn_off_paging_wrt_config("log")

    cfg = config.Config("shared", "", {"general": {"paging": "only-status"}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert commands.turn_off_paging_wrt_config("status")
    assert not commands.turn_off_paging_wrt_config("log")

    cfg = config.Config("shared", "", {"general": {"paging": "never"}})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert not commands.turn_off_paging_wrt_config("status")
    assert not commands.turn_off_paging_wrt_config("log")

    cfg = config.Config("shared", "", {})
    monkeypatch.setattr("perun.logic.config.shared", lambda: cfg)
    assert commands.turn_off_paging_wrt_config("status")
    assert commands.turn_off_paging_wrt_config("log")
    out, _ = capsys.readouterr()
    assert "warn" in out and "missing ``general.paging``" in out


def test_binaries_lookup():
    # Build test binaries using non-blocking make
    script_dir = os.path.split(__file__)[0]
    testdir = os.path.join(script_dir, "sources", "utils_tree")
    args = {
        "cwd": testdir,
        "shell": True,
        "universal_newlines": True,
        "stdout": subprocess.PIPE,
    }
    with utils.nonblocking_subprocess("make", args) as p:
        # Verify if the call is non blocking
        for _ in p.stdout:
            pass

    # Find all executables in tree with build directories
    binaries = utils.get_project_elf_executables(testdir)
    assert len(binaries) == 2
    assert binaries[0].endswith("utils_tree/build/quicksort")
    assert binaries[1].endswith("utils_tree/build/_build/quicksort")

    # Find all executables with debug symbols in a tree that has no build directories
    testdir2 = os.path.join(testdir, "testdir")
    binaries2 = utils.get_project_elf_executables(testdir2, True)
    assert len(binaries2) == 2
    assert binaries2[0].endswith("utils_tree/testdir/quicksort")
    assert binaries2[1].endswith("utils_tree/testdir/nobuild/quicksort")

    # Remove all testing executable files in the build directory (all 'quicksort' files)
    [os.remove(filename) for filename in glob.glob(testdir + "**/**/quicksort", recursive=True)]


def test_size_formatting():
    """Test the file size formatting"""
    # Test small size values
    assert utils.format_file_size(148) == "   148 B  "
    assert utils.format_file_size(1012) == "  1012 B  "
    # Test some larger values
    assert utils.format_file_size(23456) == "  22.9 KiB"
    assert utils.format_file_size(1054332440) == "1005.5 MiB"
    # Test some ridiculously large values
    assert utils.format_file_size(8273428342423) == "   7.5 TiB"
    assert utils.format_file_size(81273198731928371) == "72.2 PiB"
    assert utils.format_file_size(87329487294792342394293489232) == "77564166018710.8 PiB"


def test_nonblocking_subprocess():
    """Test the nonblocking_process utility with interruptions caused by various exceptions"""

    def termination_wrapper(pid=None):
        """The wrapper function for process termination that can - but doesn't have to -
        accept one argument

        :param int pid: the pid of the process to terminate
        """
        if pid is None:
            pid = proc_dict["pid"]
        os.kill(pid, signal.SIGINT)

    # Obtain the 'waiting' binary for testing
    target_dir = os.path.join(os.path.split(__file__)[0], "sources", "collect_trace")
    target = os.path.join(target_dir, "tst_waiting")
    # Test the subprocess interruption with default termination handler
    with pytest.raises(SystemTapScriptCompilationException) as exception:
        with utils.nonblocking_subprocess(target, {}):
            raise SystemTapScriptCompilationException("testlog", 1)
    assert "compilation failure" in str(exception.value)

    # Test the subprocess interruption with custom termination handler with no parameters
    proc_dict = {}
    with pytest.raises(SystemTapStartupException) as exception:
        with utils.nonblocking_subprocess(target, {}, termination_wrapper) as waiting_process:
            proc_dict["pid"] = waiting_process.pid
            raise SystemTapStartupException("testlog")
    assert "startup error" in str(exception.value)

    # Test the subprocess interruption with custom termination handler and custom parameter
    with pytest.raises(ResourceLockedException) as exception:
        with utils.nonblocking_subprocess(
            target, {}, termination_wrapper, proc_dict
        ) as waiting_process:
            proc_dict["pid"] = waiting_process.pid
            raise ResourceLockedException("testlog", waiting_process.pid)
    assert "already being used" in str(exception.value)


def test_signal_handler():
    """Tests default signal handler"""
    with HandledSignals(signal.SIGINT):
        os.kill(os.getpid(), signal.SIGINT)


def test_safe_key_get():
    """Tests the get_key_with_aliases functions"""
    test_dict = {"key": 1}
    assert helpers.get_key_with_aliases(test_dict, ("hello", "key")) == 1
    assert helpers.get_key_with_aliases(test_dict, ("foku", "me", "kokakola"), 2) == 2
    with pytest.raises(KeyError):
        helpers.get_key_with_aliases(test_dict, ("foku", "me", "kokakola"))


def test_ordered_enum():
    """Tests variosu operations with ordered enums that are not covered by other tests"""
    assert Complexity.CONSTANT < Complexity.LINEAR
    assert Complexity.CUBIC > Complexity.QUADRATIC
    assert Complexity.GENERIC >= Complexity.CUBIC
    assert Complexity.LINEAR <= Complexity.LINEAR

    class DummyOrderable(OrderedEnum):
        ONE = "one"
        TWO = "two"

    with pytest.raises(TypeError):
        assert Complexity.CONSTANT < DummyOrderable.ONE
    with pytest.raises(TypeError):
        assert Complexity.CUBIC > DummyOrderable.TWO
    with pytest.raises(TypeError):
        assert Complexity.GENERIC >= DummyOrderable.ONE
    with pytest.raises(TypeError):
        assert Complexity.LINEAR <= DummyOrderable.TWO


def test_get_interpreter():
    """Tests that the python interpreter can be obtained in reasonable format"""
    assert re.search("python", utils.get_current_interpreter(required_version="3+"))
    assert re.search("python", utils.get_current_interpreter(required_version="3"))


def test_common(capsys):
    """Tests common functions from utils"""

    def simple_generator():
        for i in range(0, 10):
            yield i

    chunks = list(map(list, utils.chunkify(simple_generator(), 2)))
    assert chunks == [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]

    with pytest.raises(UnsupportedModuleFunctionException):
        utils.dynamic_module_function_call("perun.vcs", "git", "nonexisting")

    with pytest.raises(SystemExit):
        utils.get_supported_module_names("nonexisting")

    with pytest.raises(subprocess.CalledProcessError):
        utils.run_safely_external_command("ls -3", quiet=False, check_results=True)
    out, _ = capsys.readouterr()
    assert "captured stdout" in out


def test_predicates(capsys):
    """Test predicates used for testing"""
    with pytest.raises(AssertionError):
        asserts.predicate_from_cli(["hello"], False)
    out, _ = capsys.readouterr()
    assert "=== Captured output ===" in out
    assert "hello\n" in out
    with pytest.raises(AssertionError):
        asserts.predicate_from_cli("hello", False)
    assert "=== Captured output ===" in out
    assert "hello\n" in out


def test_logger(capsys):
    stdout_log = log.Logger(sys.stdout)

    stdout_log.write("hello")
    stdout_log.flush()
    out, _ = capsys.readouterr()
    assert out == "hello"
    assert stdout_log.writable()
    stdout_log.writelines(["hello", "world"])
    out, _ = capsys.readouterr()
    assert out == "helloworld"
    assert stdout_log.truncate() == 0
    assert stdout_log.truncate(2) == 2
    assert stdout_log.tell() == 0
    assert stdout_log.seekable()
    assert stdout_log.seek(2) == 2
    assert not stdout_log.readable()
    assert not stdout_log.isatty()
