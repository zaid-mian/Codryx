from pyguardian.notifications import send_gate_failure_notifications


def main():
    res = send_gate_failure_notifications("Gate failed at score 65")
    print(res)


if __name__ == "__main__":
    main()
