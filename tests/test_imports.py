import importlib
import sys

import pytest

import invisible_python
from invisible_python import encode


@pytest.fixture(autouse=True)
def import_environment(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(tmp_path))
    monkeypatch.setattr(sys, "meta_path", sys.meta_path.copy())
    yield
    for name in list(sys.modules):
        if name.startswith("invisible_test_"):
            del sys.modules[name]


def test_simple_module(tmp_path):
    filename = tmp_path / "invisible_test_module.ipy"
    filename.write_bytes(encode(b"answer = 42\ndef some_function():\n    return answer\n"))
    invisible_python.install()
    module = importlib.import_module("invisible_test_module")
    assert module.some_function() == 42
    assert module.__name__ == "invisible_test_module"
    assert module.__file__ == str(filename)
    assert module.__package__ == ""


def test_package_and_relative_import(tmp_path):
    package = tmp_path / "invisible_test_package"
    package.mkdir()
    (package / "__init__.ipy").write_bytes(encode(b"from .helper import answer\n"))
    (package / "helper.ipy").write_bytes(encode(b"answer = 42\n"))
    invisible_python.install()
    module = importlib.import_module("invisible_test_package")
    from invisible_test_package import helper

    assert module.answer == helper.answer == 42
    assert module.__package__ == "invisible_test_package"
    assert list(module.__path__) == [str(package)]
    assert helper.__package__ == "invisible_test_package"


def test_install_is_explicit_and_idempotent():
    assert not any(isinstance(finder, invisible_python.InvisibleFinder) for finder in sys.meta_path)
    invisible_python.install()
    invisible_python.install()
    assert sum(isinstance(finder, invisible_python.InvisibleFinder) for finder in sys.meta_path) == 1


def test_ordinary_imports_take_priority(tmp_path):
    (tmp_path / "invisible_test_ordinary.py").write_text("answer = 42\n")
    (tmp_path / "invisible_test_ordinary.ipy").write_bytes(encode(b"answer = 0\n"))
    invisible_python.install()
    module = importlib.import_module("invisible_test_ordinary")
    assert module.answer == 42
    assert module.__file__.endswith(".py")


def test_ordinary_package_takes_priority(tmp_path):
    package = tmp_path / "invisible_test_ordinary_package"
    package.mkdir()
    (package / "__init__.py").write_text("answer = 42\n")
    (package / "__init__.ipy").write_bytes(encode(b"answer = 0\n"))
    invisible_python.install()
    module = importlib.import_module("invisible_test_ordinary_package")
    assert module.answer == 42
    assert module.__file__ == str(package / "__init__.py")
