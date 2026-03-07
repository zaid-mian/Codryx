
# codryx
codryx is a lightweight Python code quality and dependency health toolkit with progressive phases of features (1–6) focused on:

Guarded function contracts with strict mode
Dead code, unused imports, and unused symbols detection
Dependency and security scanning
Migration PR automation with optional auto-merge
License graph and gatekeeper health scoring
Interactive dashboards, IDE helpers, rich notifications
Optional real-time CI dashboards and websocket broadcasting
Installation
Recommended: create a virtual environment and install optional dependencies.
Optional dependencies enhance CLI UX and features but are not required.
# Create venv
python -m venv .venv

# Activate on Windows
.\\.venv\\Scripts\\activate

# Install optional dependencies
pip install typer rich requests pyyaml packaging jinja2 websockets
Quick Start

CLI help: python -m codryx.cli help

Run doctor: python -m codryx.cli doctor

Example scripts: python run_examples.py

CLI Usage

Help: python -m codryx.cli help

Dependencies: codryx deps scan

Code: codryx code scan --root .

Security: codryx security scan

Doctor: codryx doctor

Strict mode: codryx strict

Fallback: without Typer/Rich, use python -m codryx.cli doctor

Python API

Guards: from codryx import guard, enable_strict_mode

Code scan: from codryx import scan_code

Dependency scan: from codryx import scan_dependencies

Example: examples/example_usage.py

Environment Variables

PY_GUARDIAN_MODE: default "development"

PY_GUARDIAN_STRICT: "1"/"true"/"yes" to enable strict mode

PY_GUARDIAN_REPORT_DIR: output directory (default "reports")

PY_GUARDIAN_AUDIT_ASYNC: "1"/"true"/"yes" to enable async audit

PY_GUARDIAN_AUDIT_QUEUE: queue size (default 1024)

PY_GUARDIAN_HEALTH_THRESHOLD: numeric threshold to fail gate

PY_GUARDIAN_LICENSE_BLOCKLIST: comma-separated license names to flag

PY_GUARDIAN_SLACK_WEBHOOK: Slack incoming webhook URL

PY_GUARDIAN_TEAMS_WEBHOOK: Teams incoming webhook URL

GITHUB_TOKEN / GITLAB_TOKEN: tokens to create PRs

PY_GUARDIAN_APPROVED: "1"/"true"/"yes" allows auto-merge for supported providers

Phase 1–6 Highlights

Phase 1–2: Guards, strict mode, dead code detection, dependency scanning

Phase 3: License graph/conflicts, gatekeeper, dashboards

Phase 4: Notifications, interactive charts, IDE hints

Phase 5: Rich notifications, realtime CI dashboard, security auto-remediation

Phase 6: Optional IDE extension modules, websocket broadcaster, pipeline snippets

Examples

examples/example_usage.py → rules, code scan, PR payload

IDE helpers:

examples/ide_preview.py → guard highlights and health hints

examples/vscode_plugin_example.py → VSCode diagnostics and quickfix

Dashboards:

examples/ci_dashboard_example.py → writes metrics.json

Open codryx/templates/ci_dashboard.html from the reports directory

Notifications:

examples/notifications_example.py → simple webhook use

examples/notifications_rich_example.py → Slack/Teams rich payloads

Security:

examples/security_pipeline_example.py → CI pipeline snippets

Running Examples Easily

Use the helper script: python run_examples.py

This sets PYTHONPATH to the project root and runs all example scripts

Verifying the Build

Activate venv: .\\.venv\\Scripts\\activate

Run CLI commands: help, deps scan, code scan, security scan, doctor, strict

Run examples: python run_examples.py

Run tests: python -m unittest discover -s tests -p "test*.py" -q

Optional Modules

IDE extensions (VSCode/PyCharm): codryx/ide_ext/

Real-time CI broadcaster: codryx/ci_realtime.py (requires websockets)

Rich notifications: codryx/notifications_rich.py

Security remediation: codryx/security_remediation.py

License
MIT License

Copyright (c) 2026 Your Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[... full MIT license text here ...]

---

✅ You can **copy this entire block** and save it as `README.md` in your project root.  

If you want, I can also make a **ready-to-run one-liner command in PowerShell or Linux terminal** that creates this file automatically for you.  

Do you want me to do that?
provide me all in single markdown

Sure! Here’s your all-in-one README.md in a single markdown block, ready to copy and save as README.md in your project root. It includes the license, instructions, examples, and phase highlights.

# codryx

codryx is a lightweight Python code quality and dependency health toolkit with progressive phases of features (1–6) focused on:

- Guarded function contracts with strict mode
- Dead code, unused imports, and unused symbols detection
- Dependency and security scanning
- Migration PR automation with optional auto-merge
- License graph and gatekeeper health scoring
- Interactive dashboards, IDE helpers, rich notifications
- Optional real-time CI dashboards and websocket broadcasting

## Installation

- Recommended: create a virtual environment and install optional dependencies.
- Optional dependencies enhance CLI UX and features but are not required.

```bash
# Create venv
python -m venv .venv

# Activate on Windows
.\\.venv\\Scripts\\activate

# Install optional dependencies
pip install typer rich requests pyyaml packaging jinja2 websockets
Quick Start

CLI help: python -m codryx.cli help

Run doctor: python -m codryx.cli doctor

Example scripts: python run_examples.py

CLI Usage

Help: python -m codryx.cli help

Dependencies: codryx deps scan

Code: codryx code scan --root .

Security: codryx security scan

Doctor: codryx doctor

Strict mode: codryx strict

Fallback: without Typer/Rich, use python -m codryx.cli doctor

Python API

Guards: from codryx import guard, enable_strict_mode

Code scan: from codryx import scan_code

Dependency scan: from codryx import scan_dependencies

Example: examples/example_usage.py

Environment Variables

PY_GUARDIAN_MODE: default "development"

PY_GUARDIAN_STRICT: "1"/"true"/"yes" to enable strict mode

PY_GUARDIAN_REPORT_DIR: output directory (default "reports")

PY_GUARDIAN_AUDIT_ASYNC: "1"/"true"/"yes" to enable async audit

PY_GUARDIAN_AUDIT_QUEUE: queue size (default 1024)

PY_GUARDIAN_HEALTH_THRESHOLD: numeric threshold to fail gate

PY_GUARDIAN_LICENSE_BLOCKLIST: comma-separated license names to flag

PY_GUARDIAN_SLACK_WEBHOOK: Slack incoming webhook URL

PY_GUARDIAN_TEAMS_WEBHOOK: Teams incoming webhook URL

GITHUB_TOKEN / GITLAB_TOKEN: tokens to create PRs

PY_GUARDIAN_APPROVED: "1"/"true"/"yes" allows auto-merge for supported providers

Phase 1–6 Highlights

Phase 1–2: Guards, strict mode, dead code detection, dependency scanning

Phase 3: License graph/conflicts, gatekeeper, dashboards

Phase 4: Notifications, interactive charts, IDE hints

Phase 5: Rich notifications, realtime CI dashboard, security auto-remediation

Phase 6: Optional IDE extension modules, websocket broadcaster, pipeline snippets

Examples

examples/example_usage.py → rules, code scan, PR payload

IDE helpers:

examples/ide_preview.py → guard highlights and health hints

examples/vscode_plugin_example.py → VSCode diagnostics and quickfix

Dashboards:

examples/ci_dashboard_example.py → writes metrics.json

Open codryx/templates/ci_dashboard.html from the reports directory

Notifications:

examples/notifications_example.py → simple webhook use

examples/notifications_rich_example.py → Slack/Teams rich payloads

Security:

examples/security_pipeline_example.py → CI pipeline snippets

Running Examples Easily

Use the helper script: python run_examples.py

This sets PYTHONPATH to the project root and runs all example scripts

Verifying the Build

Activate venv: .\\.venv\\Scripts\\activate

Run CLI commands: help, deps scan, code scan, security scan, doctor, strict

Run examples: python run_examples.py

Run tests: python -m unittest discover -s tests -p "test*.py" -q

Optional Modules

IDE extensions (VSCode/PyCharm): codryx/ide_ext/

Real-time CI broadcaster: codryx/ci_realtime.py (requires websockets)

Rich notifications: codryx/notifications_rich.py

Security remediation: codryx/security_remediation.py

License
MIT License

Copyright (c) 2026 Muhammad Zaid Tahir

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

