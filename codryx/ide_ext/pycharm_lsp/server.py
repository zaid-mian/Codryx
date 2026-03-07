import asyncio
import json
from typing import Any, Dict
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
    await websockets.serve(_ws_handler, host, port)  # type: ignore
    await asyncio.Future()
