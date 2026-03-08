import asyncio
import json
import webbrowser
from typing import Any, Dict, Optional, Tuple, List
from .handlers import handle_diagnostics, handle_quickfix


async def _ws_handler(ws):
    async for msg in ws:
        try:
            data = json.loads(msg)
            action = data.get("action")
            if action == "diagnostics":
                source = data.get("source", "")
                resp = handle_diagnostics(source)
                await ws.send(json.dumps({"ok": True, "data": resp}))
            elif action == "quickfix":
                source = data.get("source", "")
                kind = data.get("kind", "")
                resp = handle_quickfix(source, kind)
                await ws.send(json.dumps({"ok": True, "data": resp}))
            else:
                await ws.send(json.dumps({"ok": False, "error": "unknown_action"}))
        except Exception as e:
            await ws.send(json.dumps({"ok": False, "error": str(e)}))


async def start(host: str, port: int) -> bool:
    try:
        import websockets  # type: ignore
    except Exception:
        return False
    ResponseType = None
    HeadersType = None
    use_response_obj = False
    try:
        import websockets as _ws  # type: ignore
        ver = getattr(_ws, "__version__", "0")
        major = int(str(ver).split(".", 1)[0])
        use_response_obj = major >= 16
    except Exception:
        use_response_obj = False
    if use_response_obj:
        try:
            from websockets.http11 import Response as _R  # type: ignore
            ResponseType = _R
            try:
                from websockets.headers import Headers as _H  # type: ignore
                HeadersType = _H
            except Exception:
                HeadersType = None
        except Exception:
            try:
                from websockets.http import Response as _R  # type: ignore
                ResponseType = _R
                try:
                    from websockets.headers import Headers as _H  # type: ignore
                    HeadersType = _H
                except Exception:
                    HeadersType = None
            except Exception:
                ResponseType = None
    else:
        try:
            from websockets.http import Response as _R  # type: ignore
            ResponseType = _R
            try:
                from websockets.headers import Headers as _H  # type: ignore
                HeadersType = _H
            except Exception:
                HeadersType = None
        except Exception:
            ResponseType = None
    def _resp(status: int, headers: List[Tuple[str, str]], body: bytes):  # type: ignore
        if use_response_obj and ResponseType is not None:
            try:
                if HeadersType is not None and headers:
                    return ResponseType(status, headers=HeadersType(headers), body=body)  # type: ignore
                return ResponseType(status, body=body)  # type: ignore
            except TypeError:
                try:
                    if HeadersType is not None and headers:
                        return ResponseType(status, HeadersType(headers), body)  # type: ignore
                    return ResponseType(status, None, body)  # type: ignore
                except TypeError:
                    pass
        return (status, headers, body)

    def _process_request(path: str, request_headers: Any):
        try:
            upgrade = request_headers.get("Upgrade", "")
            if isinstance(upgrade, bytes):
                upgrade = upgrade.decode("utf-8", errors="ignore")
        except Exception:
            upgrade = ""
        if upgrade.lower() == "websocket":
            return None
        if path in ("/", "/index.html"):
            try:
                from ...visuals import _render  # type: ignore
                html = _render("ide_dashboard.html", {
                    "host": host,
                    "port": port,
                    "ws_url": f"ws://{host}:{port}",
                    "http_url": f"http://{host}:{port}",
                    "flavor": "pycharm",
                    "status": "Running"
                })
            except Exception:
                html = ""
            if not html:
                html = f"""<!doctype html><html><head><meta charset="utf-8"><title>Codryx IDE Dashboard</title><style>body{{font-family:Arial;margin:24px}}</style></head><body><h1>Codryx IDE Dashboard</h1><p>Status: Running</p><p>LSP endpoint: <code>ws://{host}:{port}</code></p><h3>PyCharm Instructions</h3><ol><li>Install/connect a WebSocket client.</li><li>Use endpoint: <code>ws://{host}:{port}</code>.</li><li>Connect to view diagnostics.</li></ol></body></html>"""
            body = html.encode("utf-8")
            headers = [("Content-Type", "text/html; charset=utf-8"), ("Cache-Control", "no-cache")]
            return _resp(200, headers, body)
        body = b"Not Found"
        headers = [("Content-Type", "text/plain; charset=utf-8"), ("Cache-Control", "no-cache")]
        return _resp(404, headers, body)

    await websockets.serve(_ws_handler, host, port, process_request=_process_request)  # type: ignore

    print("Codryx IDE Server started\n")
    print("LSP endpoint:")
    print(f"ws://{host}:{port}\n")
    print("Open dashboard in browser:")
    print(f"http://{host}:{port}\n")
    try:
        webbrowser.open(f"http://{host}:{port}")
    except Exception:
        pass

    await asyncio.Future()
