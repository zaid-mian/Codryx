import json
import os
from typing import Dict, List, Optional, Tuple

import requests
from packaging.version import Version, InvalidVersion


def _read_requirements() -> List[Tuple[str, Optional[str]]]:
    paths = ["requirements.txt", "reqs.txt"]
    items: List[Tuple[str, Optional[str]]] = []
    for p in paths:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "==" in line:
                        name, ver = line.split("==", 1)
                        items.append((name.strip(), ver.strip()))
                    else:
                        items.append((line, None))
    return items


def _read_pyproject_deps() -> List[Tuple[str, Optional[str]]]:
    path = "pyproject.toml"
    items: List[Tuple[str, Optional[str]]] = []
    if not os.path.exists(path):
        return items
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.splitlines()
        in_dep = False
        for ln in lines:
            if ln.strip().startswith("dependencies"):
                in_dep = True
                continue
            if in_dep:
                if ln.strip().startswith("]"):
                    break
                t = ln.strip().strip(",").strip().strip('"').strip("'")
                if not t:
                    continue
                if ">=" in t or "==" in t:
                    name = t.split(">=")[0].split("==")[0]
                    ver = None
                    if ">=" in t:
                        ver = t.split(">=")[1]
                    elif "==" in t:
                        ver = t.split("==")[1]
                    items.append((name.strip(), ver.strip() if ver else None))
                else:
                    items.append((t, None))
    except Exception:
        pass
    return items


def _latest_version(package: str) -> Optional[str]:
    try:
        r = requests.get(f"https://pypi.org/pypi/{package}/json", timeout=5)
        if r.status_code != 200:
            return None
        data = r.json()
        return data.get("info", {}).get("version")
    except Exception:
        return None


def scan_dependencies() -> Dict[str, Dict[str, Optional[str]]]:
    declared = {}
    for name, ver in _read_requirements() + _read_pyproject_deps():
        declared[name] = {"declared": ver, "latest": None, "outdated": None}
    for pkg in declared.keys():
        latest = _latest_version(pkg)
        declared[pkg]["latest"] = latest
        try:
            if declared[pkg]["declared"] and latest:
                dv = Version(declared[pkg]["declared"])
                lv = Version(latest)
                declared[pkg]["outdated"] = "yes" if dv < lv else "no"
            else:
                declared[pkg]["outdated"] = None
        except InvalidVersion:
            declared[pkg]["outdated"] = None
    return declared
