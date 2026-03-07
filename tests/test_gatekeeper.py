import unittest
from pyguardian.gatekeeper import should_gate_fail


class TestGatekeeper(unittest.TestCase):
    def test_threshold(self):
        self.assertFalse(should_gate_fail(80.0, 70.0))
        self.assertTrue(should_gate_fail(60.0, 70.0))
        self.assertFalse(should_gate_fail(60.0, None))


if __name__ == "__main__":
    unittest.main()
