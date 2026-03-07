from typing import List, Tuple
import ast


def guard_highlights(source: str) -> List[Tuple[int, int, str]]:
    items: List[Tuple[int, int, str]] = []
    try:
        tree = ast.parse(source)
    except Exception:
        return items
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            decos = node.decorator_list or []
            for d in decos:
                if isinstance(d, ast.Name) and d.id == "guard":
                    items.append((node.lineno, node.col_offset, "guarded"))
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Name) and d.func.id == "guard":
                    items.append((node.lineno, node.col_offset, "guarded"))
    return items


def health_hints(source: str) -> List[str]:
    hints: List[str] = []
    try:
        tree = ast.parse(source)
    except Exception:
        return hints
    unused_imports = set()
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                unused_imports.add(n.asname or n.name)
        if isinstance(node, ast.ImportFrom):
            for n in node.names:
                unused_imports.add(n.asname or n.name)
        if isinstance(node, ast.Name):
            names.add(node.id)
    dead = sorted(list(unused_imports - names))
    if dead:
        hints.append(f"Unused imports: {', '.join(dead)}")
    return hints
