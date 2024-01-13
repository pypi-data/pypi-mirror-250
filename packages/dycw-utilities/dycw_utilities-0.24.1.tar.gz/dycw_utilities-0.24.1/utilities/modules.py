from __future__ import annotations

from collections.abc import Callable, Iterator
from contextlib import suppress
from importlib import import_module
from pkgutil import walk_packages
from types import ModuleType
from typing import Any


def yield_modules(
    module: ModuleType, /, *, recursive: bool = False
) -> Iterator[ModuleType]:
    """Yield all the modules under a package.

    Optionally, recurse into sub-packages.
    """
    name = module.__name__
    try:
        path = module.__path__
    except AttributeError:
        yield module
    else:
        with suppress(ModuleNotFoundError):
            for info in walk_packages(path):
                imported = import_module(f"{name}.{info.name}")
                if (is_pkg := info.ispkg) and recursive:
                    yield from yield_modules(imported, recursive=recursive)
                elif not is_pkg:
                    yield imported


def yield_module_contents(
    module: ModuleType,
    /,
    *,
    recursive: bool = False,
    type: type[Any] | tuple[type[Any], ...] | None = None,  # noqa: A002
    predicate: Callable[[Any], bool] | None = None,
) -> Iterator[Any]:
    """Yield all the module contents under a package.

    Optionally, recurse into sub-packages.
    """
    for mod in yield_modules(module, recursive=recursive):
        for name in dir(mod):
            obj = getattr(mod, name)
            if ((type is None) or isinstance(obj, type)) and (
                (predicate is None) or predicate(obj)
            ):
                yield obj


def yield_module_subclasses(
    module: ModuleType,
    cls: type[Any],
    /,
    *,
    recursive: bool = False,
    predicate: Callable[[type[Any]], bool] | None = None,
) -> Iterator[Any]:
    """Yield all the module subclasses under a package.

    Optionally, recurse into sub-packages.
    """

    def predicate_use(obj: type[Any], /) -> bool:
        return (
            issubclass(obj, cls)
            and not issubclass(cls, obj)
            and ((predicate is None) or predicate(obj))
        )

    return yield_module_contents(
        module, recursive=recursive, type=type, predicate=predicate_use
    )


__all__ = ["yield_module_contents", "yield_module_subclasses", "yield_modules"]
