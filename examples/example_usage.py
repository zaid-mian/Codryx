from pyguardian import guard, enable_strict_mode, scan_dependencies, scan_code
from pyguardian.rule_loader import get_rules
from pyguardian.visuals import generate_rule_graph
from pyguardian.migration import create_pr_payload
from pyguardian.config import load_config


class User:
    def __init__(self, active: bool):
        self.is_active = active


@guard("user.is_active")
def create_order(user: User):
    return "ok"


def main():
    enable_strict_mode()
    u = User(True)
    create_order(user=u)
    deps = scan_dependencies()
    code = scan_code(".")
    cfg = load_config()
    rules = get_rules("examples/config/business_rules.json")
    generate_rule_graph(cfg.report_dir, cfg.rule_graph_filename, rules)
    pr = create_pr_payload("github", "owner/repo", "PyGuardian Migration", ["Update foo to 1.2.3"])
    print(pr)


if __name__ == "__main__":
    main()
