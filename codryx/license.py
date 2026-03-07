from typing import Any, Callable, Dict, List, Optional, Set, Tuple
import re


def _parse_requires_dist(items: Optional[List[str]]) -> List[str]:
    result: List[str] = []
    if not items:
        return result
    for s in items:
        name = s.split(" ", 1)[0]
        name = re.split(r"[<>=!~]", name)[0]
        if name:
            result.append(name.strip())
    return result


Fetcher = Callable[[str], Dict[str, Any]]


def _default_fetcher(package: str) -> Dict[str, Any]:
    import requests
    r = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=5)
    r.raise_for_status()
    return r.json()


def license_graph(declared: Dict[str, Dict[str, Optional[str]]], fetcher: Optional[Fetcher] = None, max_depth: int = 2) -> Dict[str, Dict[str, Any]]:
    fetch = fetcher or _default_fetcher
    graph: Dict[str, Dict[str, Any]] = {}
    visited: Set[str] = set()

    def walk(pkg: str, depth: int):
        if pkg in visited or depth > max_depth:
            return
        visited.add(pkg)
        try:
            data = fetch(pkg)
            info = data.get("info", {})
            lic = info.get("license") or (info.get("classifiers") or [])
            requires = _parse_requires_dist(info.get("requires_dist"))
            graph[pkg] = {"license": lic, "requires": requires}
            for child in requires:
                walk(child, depth + 1)
        except Exception:
            graph[pkg] = {"license": None, "requires": []}

    for pkg in declared.keys():
        walk(pkg, 0)
    return graph


def license_conflicts(graph: Dict[str, Dict[str, Any]], blocklist: Optional[List[str]] = None) -> List[Tuple[str, Any]]:
    bl = [s.lower() for s in (blocklist or [])]
    conflicts: List[Tuple[str, Any]] = []
    for pkg, meta in graph.items():
        lic = meta.get("license")
        if isinstance(lic, list):
            text = " ".join(lic).lower()
        else:
            text = (lic or "").lower()
        if any(b in text for b in bl):
            conflicts.append((pkg, lic))
    return conflicts
