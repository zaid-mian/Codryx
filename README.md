# codryx

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status">
  <img src="https://img.shields.io/badge/python-3.7+-blue" alt="Python Version">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="License">
</p>

codryx is a lightweight Python code quality and dependency health toolkit that helps you maintain clean, secure, and healthy codebases through progressive feature phases (1–6).

## ✨ Features

- **🔒 Guarded Function Contracts** – Strict mode enforcement for function contracts
- **🔍 Dead Code Detection** – Unused imports, variables, and symbols
- **📦 Dependency Scanning** – Security vulnerabilities and license compliance
- **🤖 Migration PR Automation** – Auto-merge support for GitHub/GitLab
- **📊 License Management** – License graph visualization and gatekeeper scoring
- **📈 Interactive Dashboards** – Real-time CI dashboards with WebSocket broadcasting
- **🔔 Rich Notifications** – Slack, Teams, and webhook integrations
- **🛠️ IDE Integration** – VSCode/PyCharm helpers and quickfixes

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher

### Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate on Windows
.\\.venv\\Scripts\\activate

# Activate on macOS/Linux
source .venv/bin/activate

# Install optional dependencies for enhanced features
pip install typer rich requests pyyaml packaging jinja2 websockets

🎯 Quick Start
# View CLI help
python -m codryx.cli help

# Run health check
python -m codryx.cli doctor

# Run examples
python run_examples.py

## 📖 CLI Usage

| Command | Description |
|---------|-------------|
| `python -m codryx.cli help` | Display help information |
| `codryx deps scan` | Scan dependencies |
| `codryx code scan --root .` | Scan codebase for issues |
| `codryx security scan` | Run security vulnerability scan |
| `codryx doctor` | Run comprehensive health check |
| `codryx strict` | Enable strict mode enforcement |

> **Note:** Without Typer/Rich installed, use `python -m codryx.cli doctor` as fallback.

🐍 Python API
from codryx import guard, enable_strict_mode, scan_code, scan_dependencies

# Enable strict mode for function contracts
enable_strict_mode()

@guard
def critical_function(data):
    """This function is guarded by strict contracts"""
    return process_data(data)

# Scan codebase for issues
issues = scan_code("./src")

# Scan dependencies
vulnerabilities = scan_dependencies()

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PY_GUARDIAN_MODE` | Environment mode | `"development"` |
| `PY_GUARDIAN_STRICT` | Enable strict mode | `"false"` |
| `PY_GUARDIAN_REPORT_DIR` | Output directory | `"reports"` |
| `PY_GUARDIAN_AUDIT_ASYNC` | Enable async audit | `"false"` |
| `PY_GUARDIAN_AUDIT_QUEUE` | Queue size | `"1024"` |
| `PY_GUARDIAN_HEALTH_THRESHOLD` | Health gate threshold | `"70"` |
| `PY_GUARDIAN_LICENSE_BLOCKLIST` | Blocked licenses | `""` |
| `PY_GUARDIAN_SLACK_WEBHOOK` | Slack webhook URL | `""` |
| `PY_GUARDIAN_TEAMS_WEBHOOK` | Teams webhook URL | `""` |
| `GITHUB_TOKEN` / `GITLAB_TOKEN` | VCS tokens | `""` |
| `PY_GUARDIAN_APPROVED` | Auto-merge approval | `"false"` |

## 📊 Feature Roadmap

| Phase | Features |
|-------|----------|
| 1–2 | Guard contracts, strict mode, dead code detection, dependency scanning |
| 3 | License graph/conflicts, gatekeeper, dashboards |
| 4 | Notifications, interactive charts, IDE hints |
| 5 | Rich notifications, real-time CI dashboard, security auto-remediation |
| 6 | IDE extension modules, WebSocket broadcaster, pipeline snippets |

### IDE Integration
- `examples/ide_preview.py` – Guard highlights and health hints
- `examples/vscode_plugin_example.py` – VSCode diagnostics and quickfix

### Dashboards
```bash
# Generate metrics dashboard
python examples/ci_dashboard_example.py
# Open reports/ci_dashboard.html

### Notifications
- `examples/notifications_example.py` – Simple webhook integration
- `examples/notifications_rich_example.py` – Slack/Teams rich payloads

### Security
- `examples/security_pipeline_example.py` – CI pipeline security snippets

✅ Verifying Installation
# 1. Activate virtual environment
.\.venv\Scripts\activate

# 2. Test CLI commands
python -m codryx.cli help
python -m codryx.cli doctor

# 3. Run examples
python run_examples.py

# 4. Run tests
python -m unittest discover -s tests -p "test*.py" -q

## 🔧 Optional Modules

| Module | Path | Requirements |
|--------|------|--------------|
| IDE Extensions | `codryx/ide_ext/` | VSCode/PyCharm |
| Real-time CI | `codryx/ci_realtime.py` | websockets |
| Rich Notifications | `codryx/notifications_rich.py` | rich, requests |
| Security Remediation | `codryx/security_remediation.py` | requests |

📁 Project Structure
codryx/
├── codryx/           # Main package
├── examples/         # Usage examples
├── tests/           # Unit tests
├── templates/       # Dashboard templates
└── reports/         # Generated reports

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

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