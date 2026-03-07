import unittest
from pyguardian.notifications_rich import build_slack_rich, build_teams_adaptive_card


class TestNotificationsRich2(unittest.TestCase):
    def test_slack_rich(self):
        payload = {"cost": {"health_score": 70.0}, "gate": {"threshold": 80.0, "fail": True}, "dashboard_url": "http://example.com"}
        msg = build_slack_rich(payload)
        self.assertIn("attachments", msg)
    def test_teams_card(self):
        payload = {"cost": {"health_score": 88.0}, "gate": {"threshold": 80.0, "fail": False}, "dashboard_url": "http://example.com"}
        msg = build_teams_adaptive_card(payload)
        self.assertEqual(msg.get("type"), "AdaptiveCard")


if __name__ == "__main__":
    unittest.main()
