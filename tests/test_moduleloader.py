import pytest

from module_importer import ModuleLoader

from .modules.module import Module

valid_path = "/Users/sedov/GIT/module-importer/tests/modules"


@pytest.fixture
def loader():
    return ModuleLoader(valid_path)


@pytest.fixture
def wrong_path():
    return str("some_path")


def test_load_modules_class(loader):
    classes = loader.load_modules(mode="class")
    assert isinstance(classes, list)
    assert len(classes) > 0


def test_load_modules_invalid_path(wrong_path):
    with pytest.raises(ValueError):
        ModuleLoader(wrong_path)


def test_load_modules_invalid_mode(loader):
    with pytest.raises(ValueError):
        loader.load_modules(mode="invalid")


def test_get_path_valid(loader):
    path = loader.path
    assert path == valid_path


def test_load_module(loader):
    module = loader.load_modules()[0]
    m: Module = module()
    assert m.au == "I'm module"
