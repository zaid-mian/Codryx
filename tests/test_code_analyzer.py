import unittest
import tempfile
import os
from pyguardian.code_analyzer import scan_code


class TestCodeAnalyzer(unittest.TestCase):
    def test_unused_imports_and_dead_files(self):
        with tempfile.TemporaryDirectory() as d:
            f1 = os.path.join(d, "a.py")
            f2 = os.path.join(d, "b.py")
            with open(f1, "w", encoding="utf-8") as f:
                f.write("import math\n\ndef foo():\n    return 1\n")
            with open(f2, "w", encoding="utf-8") as f:
                f.write("def bar():\n    return 2\n")
            res = scan_code(d)
            self.assertTrue(any("a.py" in s for s in res["unused_imports"]))
            self.assertTrue(any(f2 in s for s in res["dead_files"]))


if __name__ == "__main__":
    unittest.main()
