import os
from typing import Any, Dict


def _render(template_name: str, context: Dict[str, Any]) -> str:
    try:
        from jinja2 import Environment, FileSystemLoader
    except Exception:
        return ""
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
    tpl = env.get_template(template_name)
    return tpl.render(**context)


def generate_dashboard(report_dir: str, filename: str, deps: Dict[str, Dict[str, Any]], code: Dict[str, Any], sec: Dict[str, Any], cost: Dict[str, Any], licenses: Dict[str, Any], conflicts: Any, gate: Dict[str, Any], migration: Dict[str, Any]) -> str:
    html = _render("dashboard.html", {"deps": deps, "code": code, "sec": sec, "cost": cost, "licenses": licenses, "conflicts": conflicts, "gate": gate, "migration": migration})
    if not html:
        return ""
    os.makedirs(report_dir, exist_ok=True)
    out = os.path.join(report_dir, filename)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out


def generate_rule_graph(report_dir: str, filename: str, rules: Dict[str, Any]) -> str:
    html = _render("rule_graph.html", {"rules": rules})
    if not html:
        return ""
    os.makedirs(report_dir, exist_ok=True)
    out = os.path.join(report_dir, filename)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out
