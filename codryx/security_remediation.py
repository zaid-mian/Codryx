from typing import Dict, List


def generate_remediation_suggestions() -> List[str]:
    try:
        from .security import security_scan
        vulns = security_scan()
    except Exception:
        vulns = {}
    suggestions: List[str] = []
    for pkg, items in vulns.items():
        if items:
            suggestions.append(f"Upgrade {pkg} to latest to address {len(items)} vulnerabilities")
    return suggestions


def generate_pipeline(provider: str = "github") -> str:
    suggestions = generate_remediation_suggestions()
    if provider == "github":
        return """name: PyGuardian Remediation
on:
  workflow_dispatch:
jobs:
  remediate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.x'
      - run: pip install -U -r requirements.txt
      - run: echo \"Remediation suggestions:\\n""" + "\\n".join(suggestions) + "\""
    if provider == "gitlab":
        return """stages:
  - remediate
remediate:
  stage: remediate
  image: python:3
  script:
    - pip install -U -r requirements.txt
    - echo "Remediation suggestions:\\n""" + "\\n".join(suggestions) + "\""
    return "Unsupported provider"
