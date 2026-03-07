from typing import Dict, Optional, Any


def notify_slack(webhook: str, message: str) -> bool:
    try:
        import requests
        r = requests.post(webhook, json={"text": message}, timeout=5)
        return 200 <= r.status_code < 300
    except Exception:
        return False


def notify_teams(webhook: str, message: str) -> bool:
    try:
        import requests
        r = requests.post(webhook, json={"text": message}, timeout=5)
        return 200 <= r.status_code < 300
    except Exception:
        return False


def send_gate_failure_notifications(message: str) -> Dict[str, bool]:
    import os
    results: Dict[str, bool] = {}
    slack = os.getenv("PY_GUARDIAN_SLACK_WEBHOOK", "")
    teams = os.getenv("PY_GUARDIAN_TEAMS_WEBHOOK", "")
    if slack:
        results["slack"] = notify_slack(slack, message)
    if teams:
        results["teams"] = notify_teams(teams, message)
    return results


def build_slack_blocks(payload: Dict[str, Any]) -> Dict[str, Any]:
    score = payload.get("cost", {}).get("health_score", 0)
    gate = payload.get("gate", {})
    rows = [
        ["Health Score", str(score)],
        ["Gate Threshold", str(gate.get("threshold"))],
        ["Gate Status", "FAIL" if gate.get("fail") else "PASS"],
    ]
    table = "\n".join([f"*{k}*: {v}" for k, v in rows])
    return {"text": "PyGuardian Gate Status", "blocks": [{"type": "section", "text": {"type": "mrkdwn", "text": table}}]}


def build_teams_card(payload: Dict[str, Any]) -> Dict[str, Any]:
    score = payload.get("cost", {}).get("health_score", 0)
    gate = payload.get("gate", {})
    text = f"**PyGuardian Gate**\n\n- Health Score: {score}\n- Threshold: {gate.get('threshold')}\n- Status: {'FAIL' if gate.get('fail') else 'PASS'}"
    return {"text": text}
