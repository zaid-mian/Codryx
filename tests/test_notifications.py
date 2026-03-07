import unittest
import os
from pyguardian.notifications import send_gate_failure_notifications


class TestNotifications(unittest.TestCase):
    def test_no_webhooks(self):
        os.environ.pop("PY_GUARDIAN_SLACK_WEBHOOK", None)
        os.environ.pop("PY_GUARDIAN_TEAMS_WEBHOOK", None)
        res = send_gate_failure_notifications("Gate failed")
        self.assertEqual(res, {})


if __name__ == "__main__":
    unittest.main()
