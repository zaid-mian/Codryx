from typing import Any, Dict
from ...ide_plugin import guard_highlights, health_hints
from ..pycharm import quickfix_unused_imports
from .protocol import to_diagnostics


def handle_diagnostics(source: str) -> Dict[str, Any]:
    hl = guard_highlights(source)
    hints = health_hints(source)
    return to_diagnostics(hl, hints)


def handle_quickfix(source: str, kind: str) -> Dict[str, Any]:
    if kind == "unused_imports":
        fixed, removed = quickfix_unused_imports(source)
        return {"fixed": fixed, "removed": removed}
    return {"fixed": source, "removed": []}
