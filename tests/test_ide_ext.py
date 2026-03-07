import unittest
from pyguardian.ide_ext.vscode import export_diagnostics as vs_export
from pyguardian.ide_ext.pycharm import export_diagnostics as pc_export


class TestIDEExt(unittest.TestCase):
    def test_vscode_export(self):
        src = "import os\n@guard('arg0 > 0')\ndef foo(x):\n    return x\n"
        d = vs_export(src)
        self.assertIn("diagnostics", d)
        self.assertTrue(any(dd.get("code") == "PG001" for dd in d["diagnostics"]))
    def test_pycharm_export(self):
        src = "import os\n@guard('arg0 > 0')\ndef foo(x):\n    return x\n"
        d = pc_export(src)
        self.assertIn("diagnostics", d)
        self.assertTrue(any(dd.get("severity") == "INFO" for dd in d["diagnostics"]))


if __name__ == "__main__":
    unittest.main()
