import ast
import os
from typing import Dict, List, Set, Tuple


def _python_files(root: str) -> List[str]:
    files: List[str] = []
    for base, _, names in os.walk(root):
        if any(s in base for s in ["venv", ".venv", "__pycache__", ".git"]):
            continue
        for n in names:
            if n.endswith(".py"):
                files.append(os.path.join(base, n))
    return files


def _definitions(tree: ast.AST) -> Set[str]:
    defs: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            defs.add(node.name)
        if isinstance(node, ast.ClassDef):
            defs.add(node.name)
    return defs


def _references(tree: ast.AST) -> Set[str]:
    refs: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            refs.add(node.id)
        if isinstance(node, ast.Attribute):
            refs.add(node.attr)
    return refs


def _imports(tree: ast.AST) -> List[Tuple[str, str]]:
    imps: List[Tuple[str, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for n in node.names:
                imps.append((n.name, n.asname or n.name))
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            for n in node.names:
                imps.append((f"{mod}.{n.name}" if mod else n.name, n.asname or n.name))
    return imps


def scan_code(root: str = ".") -> Dict[str, List[str]]:
    files = _python_files(root)
    all_defs: Set[str] = set()
    all_refs: Set[str] = set()
    per_file_refs: Dict[str, Set[str]] = {}
    per_file_defs: Dict[str, Set[str]] = {}
    per_file_import_aliases: Dict[str, Set[str]] = {}
    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8") as f:
                src = f.read()
            tree = ast.parse(src)
            defs = _definitions(tree)
            refs = _references(tree)
            imps = _imports(tree)
            all_defs |= defs
            all_refs |= refs
            per_file_defs[fp] = defs
            per_file_refs[fp] = refs
            per_file_import_aliases[fp] = {alias for _, alias in imps}
        except Exception:
            continue
    unused = sorted(list(all_defs - all_refs))
    unused_imports: Dict[str, List[str]] = {}
    for fp, aliases in per_file_import_aliases.items():
        dead = sorted(list(aliases - per_file_refs.get(fp, set())))
        if dead:
            unused_imports[fp] = dead
    dead_files: List[str] = []
    for fp in files:
        defs = per_file_defs.get(fp, set())
        refs_outside = any(alias in (all_refs - per_file_refs.get(fp, set())) for alias in defs)
        if not defs and not per_file_refs.get(fp, set()):
            dead_files.append(fp)
        elif defs and not refs_outside:
            dead_files.append(fp)
    return {"unused_symbols": unused, "unused_imports": [f"{fp}:{','.join(names)}" for fp, names in unused_imports.items()], "dead_files": dead_files, "files_scanned": files}
