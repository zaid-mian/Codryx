from typing import Any, Iterable, Union

__all__ = ["guard", "enable_strict_mode", "scan_dependencies", "scan_code"]


def guard(condition: Union[str, Iterable], rules: str | None = None):
    from .guard import guard as _guard
    return _guard(condition=condition, rules=rules)


def enable_strict_mode() -> None:
    from .guard import enable_strict_mode as _esm
    _esm()


def scan_dependencies() -> dict[str, dict[str, Any]]:
    from .scanner import scan_dependencies as _sd
    return _sd()


def scan_code(root: str = ".") -> dict[str, Any]:
    from .code_analyzer import scan_code as _sc
    return _sc(root)
