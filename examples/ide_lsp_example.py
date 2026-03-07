from pyguardian.ide_ext.lsp import start_server, apply_quickfix


def main():
    ok, msg = start_server("127.0.0.1", 8766, "vscode")
    print(msg)


if __name__ == "__main__":
    main()
