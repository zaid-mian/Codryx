from typing import Dict, List, Optional, Tuple
import json
from .security import security_scan


def plan_migration(dep_scan: Dict[str, Dict[str, str]]) -> List[str]:
    tasks: List[str] = []
    for name, info in dep_scan.items():
        if info.get("outdated") == "yes":
            latest = info.get("latest")
            if latest:
                tasks.append(f"Update {name} to {latest}")
    return tasks


def create_pr_payload(provider: str, repo: str, title: str, tasks: List[str], branch: str = "pyguardian/migration", auto_merge: bool = False) -> Dict[str, str]:
    remediation = _security_remediation()
    body = "Automated dependency migration:\n\n" + "\n".join(f"- {t}" for t in tasks)
    if remediation:
        body += "\n\nSecurity auto-remediation suggestions:\n" + "\n".join(f"- {r}" for r in remediation)
    return {"provider": provider, "repo": repo, "title": title, "body": body, "branch": branch, "auto_merge": "1" if auto_merge else "0"}


def try_post_pr(payload: Dict[str, str]) -> Tuple[bool, Optional[str]]:
    try:
        import os
        import requests
        provider = payload["provider"]
        if provider.lower() == "github":
            token = os.getenv("GITHUB_TOKEN")
            if not token:
                return False, "Missing GITHUB_TOKEN"
            owner_repo = payload["repo"]
            url = f"https://api.github.com/repos/{owner_repo}/pulls"
            headers = {"Authorization": f"token {token}"}
            data = {"title": payload["title"], "head": payload["branch"], "base": "main", "body": payload["body"]}
            r = requests.post(url, headers=headers, json=data, timeout=10)
            if r.status_code >= 200 and r.status_code < 300:
                url = r.json().get("html_url")
                if payload.get("auto_merge") == "1" and os.getenv("PY_GUARDIAN_APPROVED", "0") in {"1", "true", "yes"}:
                    pr_number = r.json().get("number")
                    if pr_number:
                        merge_url = f"https://api.github.com/repos/{owner_repo}/pulls/{pr_number}/merge"
                        r2 = requests.put(merge_url, headers=headers, json={"commit_title": payload["title"]}, timeout=10)
                        if 200 <= r2.status_code < 300:
                            return True, url
                return True, url
            return False, r.text
        if provider.lower() == "gitlab":
            token = os.getenv("GITLAB_TOKEN")
            if not token:
                return False, "Missing GITLAB_TOKEN"
            url = f"https://gitlab.com/api/v4/projects/{payload['repo']}/merge_requests"
            headers = {"PRIVATE-TOKEN": token}
            data = {"title": payload["title"], "source_branch": payload["branch"], "target_branch": "main", "description": payload["body"]}
            r = requests.post(url, headers=headers, data=data, timeout=10)
            if 200 <= r.status_code < 300:
                if payload.get("auto_merge") == "1" and os.getenv("PY_GUARDIAN_APPROVED", "0") in {"1", "true", "yes"}:
                    pass
                return True, r.text
            return False, r.text
        return False, "Unsupported provider"
    except Exception as e:
        return False, str(e)


def _security_remediation() -> List[str]:
    try:
        vulns = security_scan()
        suggestions: List[str] = []
        for pkg, items in vulns.items():
            if items:
                suggestions.append(f"Upgrade {pkg} to latest to address {len(items)} vulnerabilities")
        return suggestions
    except Exception:
        return []
