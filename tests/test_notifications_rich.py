import unittest
from pyguardian.notifications import build_slack_blocks, build_teams_card


class TestNotificationsRich(unittest.TestCase):
    def test_slack_blocks(self):
        payload = {"cost": {"health_score": 75.5}, "gate": {"threshold": 80.0, "fail": True}}
        blocks = build_slack_blocks(payload)
        self.assertIn("blocks", blocks)
        self.assertIn("PyGuardian Gate Status", blocks.get("text", ""))
    def test_teams_card(self):
        payload = {"cost": {"health_score": 90.0}, "gate": {"threshold": 80.0, "fail": False}}
        card = build_teams_card(payload)
        self.assertIn("PyGuardian Gate", card.get("text", ""))


if __name__ == "__main__":
    unittest.main()
