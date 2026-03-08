from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class Config:
    mode: str = "development"
    strict: bool = False
    report_dir: str = "reports"
    dashboard_filename: str = "codryx_report.html"
    rule_graph_filename: str = "rule_graph.html"
    audit_async: bool = True
    audit_queue_size: int = 1024
    health_threshold: Optional[float] = None
    license_blocklist: str = ""


def load_config() -> Config:
    mode = os.getenv("PY_GUARDIAN_MODE", "development")
    strict = os.getenv("PY_GUARDIAN_STRICT", "").lower() in {"1", "true", "yes"}
    report_dir = os.getenv("PY_GUARDIAN_REPORT_DIR", "reports")
    audit_async = os.getenv("PY_GUARDIAN_AUDIT_ASYNC", "1").lower() in {"1", "true", "yes"}
    queue_size = int(os.getenv("PY_GUARDIAN_AUDIT_QUEUE", "1024"))
    ht = os.getenv("PY_GUARDIAN_HEALTH_THRESHOLD")
    threshold = float(ht) if ht is not None and ht != "" else None
    blocklist = os.getenv("PY_GUARDIAN_LICENSE_BLOCKLIST", "")
    return Config(mode=mode, strict=strict, report_dir=report_dir, audit_async=audit_async, audit_queue_size=queue_size, health_threshold=threshold, license_blocklist=blocklist)
