from pyguardian.security_remediation import generate_pipeline


def main():
    print(generate_pipeline("github"))
    print(generate_pipeline("gitlab"))


if __name__ == "__main__":
    main()
