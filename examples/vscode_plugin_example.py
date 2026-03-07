from pyguardian.ide_ext.vscode import export_diagnostics, quickfix_unused_imports


def main():
    source = "import os\n@guard('arg0 > 0')\ndef foo(x):\n    return x\n"
    diags = export_diagnostics(source)
    print(diags)
    fixed, removed = quickfix_unused_imports(source)
    print(removed)


if __name__ == "__main__":
    main()
