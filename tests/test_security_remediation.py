import unittest
from pyguardian.security_remediation import generate_pipeline


class TestSecurityRemediation(unittest.TestCase):
    def test_pipeline_github(self):
        yml = generate_pipeline("github")
        self.assertIn("workflow_dispatch", yml)
    def test_pipeline_gitlab(self):
        yml = generate_pipeline("gitlab")
        self.assertIn("stages", yml)


if __name__ == "__main__":
    unittest.main()
