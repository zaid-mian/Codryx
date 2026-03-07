import json
import sys
import builtins
from typing import Optional

try:
    import typer  # type: ignore
except Exception:
    typer = None  # type: ignore

try:
    from rich import print as rprint
    from rich.table import Table
except Exception:
    rprint = builtins.print
    Table = None

from .guard import enable_strict_mode


if typer:
    app = typer.Typer(add_completion=False, help="PyGuardian CLI")

    @app.command("deps")
    def deps(cmd: str = typer.Argument(..., help="subcommand: scan")):
        if cmd != "scan":
            raise typer.BadParameter("Use: pyguardian deps scan")
        from .scanner import scan_dependencies
        data = scan_dependencies()
        if Table:
            table = Table(title="Dependencies")
            table.add_column("Package")
            table.add_column("Declared")
            table.add_column("Latest")
            table.add_column("Outdated")
            for k, v in data.items():
                table.add_row(k, str(v.get("declared")), str(v.get("latest")), str(v.get("outdated")))
            rprint(table)
        else:
            rprint(json.dumps(data, indent=2))

    @app.command("code")
    def code(cmd: str = typer.Argument(..., help="subcommand: scan"), root: Optional[str] = typer.Option(".", "--root")):
        if cmd != "scan":
            raise typer.BadParameter("Use: pyguardian code scan")
        from .code_analyzer import scan_code
        data = scan_code(root)
        print(json.dumps(data, indent=2))

    @app.command("security")
    def security(cmd: str = typer.Argument(..., help="subcommand: scan")):
        if cmd != "scan":
            raise typer.BadParameter("Use: pyguardian security scan")
        from .security import security_scan
        data = security_scan()
        print(json.dumps(data, indent=2))

    @app.command("doctor")
    def doctor():
        from .scanner import scan_dependencies
        from .code_analyzer import scan_code
        from .security import security_scan
        from .cost_analyzer import estimate_cost
        from .config import load_config
        from .visuals import generate_dashboard
        from .license import license_graph, license_conflicts
        from .migration import plan_migration
        from .gatekeeper import should_gate_fail
        deps = scan_dependencies()
        code = scan_code(".")
        sec = security_scan()
        cost = estimate_cost(deps)
        cfg = load_config()
        lic_graph = license_graph(deps)
        conflicts = license_conflicts(lic_graph, [s.strip() for s in cfg.license_blocklist.split(",") if s.strip()])
        migration_tasks = plan_migration(deps)
        gate_fail = should_gate_fail(cost.get("health_score", 0.0), cfg.health_threshold)
        payload = {"cost": cost, "unused": code.get("unused_symbols"), "vulnerabilities": {k: len(v) for k, v in sec.items()}, "licenses": lic_graph, "conflicts": conflicts, "migration": {"tasks": migration_tasks}, "gate": {"threshold": cfg.health_threshold, "fail": gate_fail}}
        rprint(json.dumps(payload, indent=2))
        path = generate_dashboard(cfg.report_dir, cfg.dashboard_filename, deps, code, sec, cost, lic_graph, conflicts, {"threshold": cfg.health_threshold, "fail": gate_fail}, {"tasks": migration_tasks})
        if path:
            rprint(f"Dashboard: {path}")
        if gate_fail:
            import sys as _sys
            _sys.exit(1)
        else:
            try:
                from .notifications import send_gate_failure_notifications
                msg = f"PyGuardian gate passed with score {cost.get('health_score')}"
                send_gate_failure_notifications(msg)
            except Exception:
                pass

    @app.command("help")
    def help_cmd():
        rprint("Commands:")
        rprint("pyguardian deps scan")
        rprint("pyguardian code scan")
        rprint("pyguardian security scan")
        rprint("pyguardian doctor")
        rprint("pyguardian ide serve")

    @app.command("strict")
    def strict():
        enable_strict_mode()
        rprint("Strict mode enabled")
    
    @app.command("ide")
    def ide(cmd: str = typer.Argument(..., help="subcommand: serve"), host: Optional[str] = typer.Option("127.0.0.1", "--host"), port: Optional[int] = typer.Option(8766, "--port"), flavor: Optional[str] = typer.Option("vscode", "--flavor")):
        if cmd != "serve":
            raise typer.BadParameter("Use: pyguardian ide serve")
        from .ide_ext.lsp import start_server
        ok, msg = start_server(host or "127.0.0.1", int(port or 8766), flavor or "vscode")
        rprint(msg)
else:
    def app():
        if len(sys.argv) >= 2 and sys.argv[1] == "help":
            rprint("Commands:")
            rprint("pyguardian deps scan")
            rprint("pyguardian code scan")
            rprint("pyguardian security scan")
            rprint("pyguardian doctor")
        elif len(sys.argv) >= 2 and sys.argv[1] == "doctor":
            try:
                def _read_requirements() -> dict:
                    import os as _os
                    items = {}
                    for p in ["requirements.txt", "reqs.txt"]:
                        if _os.path.exists(p):
                            with open(p, "r", encoding="utf-8") as f:
                                for line in f:
                                    s = line.strip()
                                    if not s or s.startswith("#"):
                                        continue
                                    if "==" in s:
                                        name, ver = s.split("==", 1)
                                        items[name.strip()] = {"declared": ver.strip(), "latest": None, "outdated": None}
                                    else:
                                        items[s] = {"declared": None, "latest": None, "outdated": None}
                    return items
                def _read_pyproject_deps() -> dict:
                    import os as _os
                    path = "pyproject.toml"
                    items = {}
                    if not _os.path.exists(path):
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
                                name = t.split(">=")[0].split("==")[0].strip()
                                ver = None
                                if ">=" in t:
                                    ver = t.split(">=")[1].strip()
                                elif "==" in t:
                                    ver = t.split("==")[1].strip()
                                items[name] = {"declared": ver, "latest": None, "outdated": None}
                    except Exception:
                        pass
                    return items
                deps = _read_requirements()
                for k, v in _read_pyproject_deps().items():
                    deps.setdefault(k, v)
                from .code_analyzer import scan_code
                from .cost_analyzer import estimate_cost
                from .config import load_config
                from .visuals import generate_dashboard
                code = scan_code(".")
                try:
                    from .security import security_scan
                    sec = security_scan()
                except Exception:
                    sec = {}
                try:
                    from .license import license_graph, license_conflicts
                    cfg = load_config()
                    lic_graph = license_graph(deps)
                    conflicts = license_conflicts(lic_graph, [s.strip() for s in cfg.license_blocklist.split(",") if s.strip()])
                except Exception:
                    cfg = load_config()
                    lic_graph = {}
                    conflicts = []
                from .migration import plan_migration
                from .gatekeeper import should_gate_fail
                cost = estimate_cost(deps)
                migration_tasks = plan_migration(deps)
                gate_fail = should_gate_fail(cost.get("health_score", 0.0), cfg.health_threshold)
                payload = {"cost": cost, "unused": code.get("unused_symbols"), "vulnerabilities": {k: len(v) for k, v in sec.items()}, "licenses": lic_graph, "conflicts": conflicts, "migration": {"tasks": migration_tasks}, "gate": {"threshold": cfg.health_threshold, "fail": gate_fail}}
                rprint(json.dumps(payload, indent=2))
                path = generate_dashboard(cfg.report_dir, cfg.dashboard_filename, deps, code, sec, cost, lic_graph, conflicts, {"threshold": cfg.health_threshold, "fail": gate_fail}, {"tasks": migration_tasks})
                if path:
                    rprint(f"Dashboard: {path}")
                if gate_fail:
                    import sys as _sys
                    _sys.exit(1)
                else:
                    try:
                        from .notifications import send_gate_failure_notifications
                        msg = f"PyGuardian gate passed with score {cost.get('health_score')}"
                        send_gate_failure_notifications(msg)
                    except Exception:
                        pass
            except Exception:
                rprint("Typer not installed. Use: python -m pyguardian.cli help")
        else:
            rprint("Typer not installed. Use: python -m pyguardian.cli help")

if __name__ == "__main__":
    app()
