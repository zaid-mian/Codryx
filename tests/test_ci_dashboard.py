import unittest
import tempfile
import os
import json
from pyguardian.ci_dashboard import write_metrics


class TestCIDashboard(unittest.TestCase):
    def test_write_metrics(self):
        with tempfile.TemporaryDirectory() as d:
            payload = {"cost": {"health_score": 88.0}, "gate": {"threshold": 90.0, "fail": True}}
            path = write_metrics(d, payload)
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["cost"]["health_score"], 88.0)


if __name__ == "__main__":
    unittest.main()
