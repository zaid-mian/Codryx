from pyguardian.ci_dashboard import write_metrics, start_server
from pyguardian.config import load_config
from pyguardian.code_analyzer import scan_code
from pyguardian.cost_analyzer import estimate_cost


def main():
    cfg = load_config()
    code = scan_code(".")
    deps = {}
    cost = estimate_cost(deps)
    payload = {"cost": cost, "code": code, "deps": deps, "gate": {"threshold": cfg.health_threshold, "fail": False}}
    write_metrics(cfg.report_dir, payload)
    print("Metrics written. To serve: start server and open ci_dashboard.html in the report dir.")


if __name__ == "__main__":
    main()
