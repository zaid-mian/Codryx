from typing import Any, Dict, List, Tuple
from ..ide_plugin import guard_highlights, health_hints


def export_diagnostics(source: str) -> Dict[str, Any]:
    highlights = guard_highlights(source)
    hints = health_hints(source)
    diags: List[Dict[str, Any]] = []
    for ln, col, tag in highlights:
        diags.append({"line": ln, "column": col, "severity": "INFO", "message": "Guarded function"})
    for h in hints:
        diags.append({"line": 1, "column": 0, "severity": "WARNING", "message": h})
    return {"version": 1, "diagnostics": diags}


def quickfix_unused_imports(source: str) -> Tuple[str, List[str]]:
    lines = source.splitlines()
    removed: List[str] = []
    for i, ln in enumerate(list(lines)):
        s = ln.strip()
        if s.startswith("import ") or s.startswith("from "):
            removed.append(ln)
            lines[i] = ""
    return "\n".join(lines), removed
