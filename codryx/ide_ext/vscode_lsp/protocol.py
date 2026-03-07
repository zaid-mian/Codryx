from typing import Any, Dict, List, Tuple


def to_diagnostics(highlights: List[Tuple[int, int, str]], hints: List[str]) -> Dict[str, Any]:
    diags: List[Dict[str, Any]] = []
    for ln, col, tag in highlights:
        diags.append({"range": {"start": {"line": ln - 1, "character": col}, "end": {"line": ln - 1, "character": col + 1}}, "severity": "info", "message": "Guarded function", "code": "PG001"})
    for h in hints:
        diags.append({"range": {"start": {"line": 0, "character": 0}, "end": {"line": 0, "character": 0}}, "severity": "warning", "message": h, "code": "PG002"})
    return {"version": 1, "diagnostics": diags}
