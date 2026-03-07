from pyguardian.notifications_rich import build_slack_rich, build_teams_adaptive_card


def main():
    payload = {"cost": {"health_score": 85.3}, "gate": {"threshold": 80.0, "fail": False}, "dashboard_url": "http://localhost:8080/ci_dashboard.html"}
    print(build_slack_rich(payload))
    print(build_teams_adaptive_card(payload))


if __name__ == "__main__":
    main()
