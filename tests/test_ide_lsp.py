import unittest
from pyguardian.ide_ext.lsp import apply_quickfix
from pyguardian.ide_ext.vscode_lsp.protocol import to_diagnostics as vs_to
from pyguardian.ide_ext.pycharm_lsp.protocol import to_diagnostics as pc_to
from pyguardian.ide_plugin import guard_highlights, health_hints


class TestIDELSP(unittest.TestCase):
    def test_quickfix_unused_imports(self):
        src = "import os\n@guard('arg0 > 0')\ndef foo(x):\n    return x\n"
        fixed, removed = apply_quickfix(src, "unused_imports", "vscode")
        self.assertTrue(any("import os" in r for r in removed))
        fixed2, removed2 = apply_quickfix(src, "unused_imports", "pycharm")
        self.assertTrue(any("import os" in r for r in removed2))
    def test_protocols_build_diagnostics(self):
        src = "import os\n@guard('arg0 > 0')\ndef foo(x):\n    return x\n"
        hl = guard_highlights(src)
        hints = health_hints(src)
        d1 = vs_to(hl, hints)
        d2 = pc_to(hl, hints)
        self.assertIn("diagnostics", d1)
        self.assertIn("diagnostics", d2)


if __name__ == "__main__":
    unittest.main()
