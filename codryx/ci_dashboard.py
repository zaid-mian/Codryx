import json
import os
from http.server import SimpleHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional


def write_metrics(report_dir: str, payload: Dict[str, Any]) -> str:
    os.makedirs(report_dir, exist_ok=True)
    out = os.path.join(report_dir, "metrics.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return out


class _MetricsHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: Optional[str] = None, **kwargs):
        super().__init__(*args, directory=directory, **kwargs)


def start_server(report_dir: str, host: str = "127.0.0.1", port: int = 8080) -> HTTPServer:
    os.makedirs(report_dir, exist_ok=True)
    handler = lambda *args, **kwargs: _MetricsHandler(*args, directory=report_dir, **kwargs)  # type: ignore
    httpd = HTTPServer((host, port), handler)
    return httpd
