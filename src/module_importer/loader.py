import sys
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import import_module
from inspect import isclass
from pathlib import Path
from pkgutil import iter_modules
from typing import Generic, List, Literal, Optional, Set, TypeVar, cast, get_args

V = TypeVar("V")


_MODES = Literal["class", "module"]
_LOAD_TYPE = Literal["just_load", "update"]


@dataclass
class Errors:
    not_string = "Input must be string, "
    path_not_exists = "Path not exists"
    wrong_mode = "Mode can be {mode_type} only"
    not_implemented = "Not implemented method {method_name}"


@contextmanager
def temp_user_sys_path(user_path: str):
    if not isinstance(user_path, str):
        raise ValueError(Errors.not_string, user_path)

    try:
        yield sys.path.append(user_path)
    finally:
        sys.path.remove(user_path)


class ModuleLoader(Generic[V]):
    """_summary_: Generic module loader

    Args:
        Generic (_type_): The type of modules (classes) tha are awaited to be loaded.

        _path_: (str): Valid (existing path to modules folder)
    """

    def __init__(self, path: str):
        self.path = path
        self.modules: Optional[List[V]] = None

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value: str):
        if not isinstance(value, str):
            raise ValueError(Errors.not_string, value)

        self._path = self.get_path(value)

    def get_path(self, value: str):
        p = Path(value).resolve()

        if p.exists() == False:
            raise ValueError(Errors.path_not_exists, p)
        return str(p)

    def load_modules(
        self,
        mode: _MODES = "class",
        load_type: _LOAD_TYPE = "just_load",
    ) -> List[V]:
        mode_condition = None
        classes: Set = set()

        modes = list(get_args(_MODES))

        if not mode in modes:
            raise ValueError(Errors.wrong_mode.format(mode_type=list(get_args(_MODES))))

        match mode:
            case "class":
                mode_condition = isclass
            case "module":
                raise NotImplementedError(
                    Errors.not_implemented.format(not_implemented="module")
                )

        with temp_user_sys_path(str(self.path)):
            for _, module_name, _ in iter_modules([self.path]):  # type: ignore
                try:
                    module = import_module(f"{module_name}")

                    for attribute_name in dir(module):
                        attribute = getattr(module, attribute_name)

                        if mode_condition(attribute):
                            all_classes = str(attribute).split(".")

                            for cl in all_classes:
                                if module_name in cl:
                                    classes.add(cast(V, attribute))
                except Exception as e:
                    raise ImportError(e)

        match load_type:
            case "just_load":
                pass
            case "update":
                self.modules = list(classes)

        return list(classes)
