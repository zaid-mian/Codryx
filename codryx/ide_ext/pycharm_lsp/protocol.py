from typing import Any, Dict, List, Tuple


def to_diagnostics(highlights: List[Tuple[int, int, str]], hints: List[str]) -> Dict[str, Any]:
    diags = []
    for ln, col, tag in highlights:
        diags.append({"line": ln, "column": col, "severity": "INFO", "message": "Guarded function"})
    for h in hints:
        diags.append({"line": 1, "column": 0, "severity": "WARNING", "message": h})
    return {"version": 1, "diagnostics": diags}
