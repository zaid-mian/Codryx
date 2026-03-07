import os
from typing import Dict, List, Optional, Tuple

import requests


def _declared() -> List[Tuple[str, Optional[str]]]:
    items: List[Tuple[str, Optional[str]]] = []
    paths = ["requirements.txt", "reqs.txt", "pyproject.toml"]
    for p in paths:
        if p.endswith(".toml"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for ln in f:
                        t = ln.strip()
                        if t.startswith('"') or t.startswith("'"):
                            t = t.strip(",").strip().strip('"').strip("'")
                            if not t:
                                continue
                            name = t.split(">=")[0].split("==")[0]
                            ver = None
                            if ">=" in t:
                                ver = t.split(">=")[1]
                            elif "==" in t:
                                ver = t.split("==")[1]
                            items.append((name.strip(), ver.strip() if ver else None))
            except Exception:
                continue
        elif os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    for ln in f:
                        s = ln.strip()
                        if not s or s.startswith("#"):
                            continue
                        if "==" in s:
                            name, ver = s.split("==", 1)
                            items.append((name.strip(), ver.strip()))
                        else:
                            items.append((s, None))
            except Exception:
                continue
    return items


def _vulns(package: str, version: Optional[str]) -> List[Dict]:
    try:
        if version:
            url = f"https://pypi.org/pypi/{package}/{version}/json"
        else:
            url = f"https://pypi.org/pypi/{package}/json"
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return []
        data = r.json()
        vulns = data.get("vulnerabilities", [])
        return vulns if isinstance(vulns, list) else []
    except Exception:
        return []


def security_scan() -> Dict[str, List[Dict]]:
    results: Dict[str, List[Dict]] = {}
    for name, ver in _declared():
        v = _vulns(name, ver)
        if v:
            results[name] = v
    return results
