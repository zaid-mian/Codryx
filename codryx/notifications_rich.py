from typing import Any, Dict, List


def build_slack_rich(payload: Dict[str, Any]) -> Dict[str, Any]:
    score = payload.get("cost", {}).get("health_score", 0)
    gate = payload.get("gate", {})
    color = "#e74c3c" if gate.get("fail") else "#2ecc71"
    fields = [
        {"type": "mrkdwn", "text": f"*Health Score*: {score}"},
        {"type": "mrkdwn", "text": f"*Threshold*: {gate.get('threshold')}"},
        {"type": "mrkdwn", "text": f"*Status*: {'FAIL' if gate.get('fail') else 'PASS'}"},
    ]
    blocks = [
        {"type": "section", "text": {"type": "mrkdwn", "text": "*PyGuardian Gate Status*"}},
        {"type": "divider"},
        {"type": "section", "fields": fields},
        {"type": "actions", "elements": [{"type": "button", "text": {"type": "plain_text", "text": "View Dashboard"}, "url": payload.get("dashboard_url", "")}]},
    ]
    return {"attachments": [{"color": color, "blocks": blocks}]}


def build_teams_adaptive_card(payload: Dict[str, Any]) -> Dict[str, Any]:
    score = payload.get("cost", {}).get("health_score", 0)
    gate = payload.get("gate", {})
    body = [
        {"type": "TextBlock", "text": "PyGuardian Gate Status", "weight": "Bolder", "size": "Medium"},
        {"type": "TextBlock", "text": f"Health Score: {score}"},
        {"type": "TextBlock", "text": f"Threshold: {gate.get('threshold')}"},
        {"type": "TextBlock", "text": f"Status: {'FAIL' if gate.get('fail') else 'PASS'}"},
        {"type": "ActionSet", "actions": [{"type": "Action.OpenUrl", "title": "View Dashboard", "url": payload.get("dashboard_url", "")}]},
    ]
    return {"type": "AdaptiveCard", "version": "1.2", "body": body}
