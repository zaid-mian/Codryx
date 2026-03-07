import unittest
from pyguardian.guard import guard


class Dummy:
    def __init__(self, x: int):
        self.x = x


class TestGuard(unittest.TestCase):
    def test_attribute_condition(self):
        @guard("arg0.x > 1")
        def f(d: Dummy):
            return True
        self.assertTrue(f(Dummy(2)))
        with self.assertRaises(PermissionError):
            f(Dummy(0))

    def test_bool_condition(self):
        @guard("arg0 and arg1")
        def f(a: bool, b: bool):
            return True
        self.assertTrue(f(True, True))
        with self.assertRaises(PermissionError):
            f(True, False)


if __name__ == "__main__":
    unittest.main()
