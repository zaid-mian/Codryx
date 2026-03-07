from pyguardian.ide_plugin import guard_highlights, health_hints


def main():
    source = "from math import sqrt\nfrom os import path\n\n@guard('arg0 > 0')\ndef foo(x):\n    return x\n"
    print(guard_highlights(source))
    print(health_hints(source))


if __name__ == "__main__":
    main()
