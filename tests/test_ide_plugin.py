import unittest
from pyguardian.ide_plugin import guard_highlights, health_hints


class TestIDEPlugin(unittest.TestCase):
    def test_guard_highlights_and_hints(self):
        src = "import os\n@guard('arg0 > 0')\ndef foo(x):\n    return x\n"
        hl = guard_highlights(src)
        self.assertTrue(any(tag == "guarded" for _, _, tag in hl))
        hints = health_hints(src)
        self.assertTrue(any("Unused imports" in h for h in hints))


if __name__ == "__main__":
    unittest.main()
