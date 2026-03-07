import os
import sys
import subprocess


def main() -> int:
    root = os.path.dirname(os.path.abspath(__file__))
    env = os.environ.copy()
    env["PYTHONPATH"] = root
    examples = [
        os.path.join(root, "examples", "example_usage.py"),
        os.path.join(root, "examples", "ide_preview.py"),
        os.path.join(root, "examples", "vscode_plugin_example.py"),
        os.path.join(root, "examples", "notifications_example.py"),
        os.path.join(root, "examples", "notifications_rich_example.py"),
        os.path.join(root, "examples", "security_pipeline_example.py"),
        os.path.join(root, "examples", "ci_dashboard_example.py"),
        os.path.join(root, "examples", "ci_realtime_example.py"),
    ]
    rc = 0
    for path in examples:
        if not os.path.exists(path):
            continue
        print(f"==> Running {os.path.relpath(path, root)}")
        try:
            proc = subprocess.run([sys.executable, path], env=env, capture_output=False)
            if proc.returncode != 0:
                rc = proc.returncode
        except Exception as e:
            print(f"Error running {path}: {e}")
            rc = 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
