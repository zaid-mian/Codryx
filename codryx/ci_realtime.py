import asyncio
import json
from typing import Any, Dict, Optional, Set


class Broadcaster:
    def __init__(self):
        self.clients: Set[Any] = set()
        self.enabled = False

    async def start(self, host: str = "127.0.0.1", port: int = 8765) -> None:
        try:
            import websockets  # type: ignore
        except Exception:
            self.enabled = False
            return
        self.enabled = True

        async def handler(ws):
            self.clients.add(ws)
            try:
                async for _ in ws:
                    pass
            finally:
                self.clients.discard(ws)

        await websockets.serve(handler, host, port)  # type: ignore

    async def publish(self, payload: Dict[str, Any]) -> bool:
        if not self.enabled or not self.clients:
            return False
        msg = json.dumps(payload, ensure_ascii=False)
        await asyncio.gather(*(c.send(msg) for c in list(self.clients)))
        return True
