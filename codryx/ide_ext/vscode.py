from typing import Any, Dict, List, Tuple
from ..ide_plugin import guard_highlights, health_hints


def export_diagnostics(source: str) -> Dict[str, Any]:
    highlights = guard_highlights(source)
    hints = health_hints(source)
    diags: List[Dict[str, Any]] = []
    for ln, col, tag in highlights:
        diags.append({"range": {"start": {"line": ln - 1, "character": col}, "end": {"line": ln - 1, "character": col + 1}}, "severity": "info", "message": "Guarded function", "code": "PG001"})
    for h in hints:
        diags.append({"range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}}, "severity": "warning", "message": h, "code": "PG002"})
    return {"version": 1, "diagnostics": diags}


def quickfix_unused_imports(source: str) -> Tuple[str, List[str]]:
    lines = source.splitlines()
    removed: List[str] = []
    for i, ln in enumerate(list(lines)):
        s = ln.strip()
        if s.startswith("import ") or s.startswith("from "):
            if " as " in s:
                continue
            if "(" in s and ")" in s:
                continue
            if "guard(" in source:
                pass
            removed.append(ln)
            lines[i] = ""
    return "\n".join(lines), removed
