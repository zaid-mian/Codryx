import asyncio
import json
from typing import Any, Dict, Optional


class AsyncAuditLogger:
    def __init__(self, maxsize: int = 1024):
        self.queue: asyncio.Queue[Dict[str, Any]] = asyncio.Queue(maxsize=maxsize)
        self.task: Optional[asyncio.Task] = None

    async def _worker(self):
        while True:
            item = await self.queue.get()
            try:
                print(json.dumps(item, ensure_ascii=False))
            finally:
                self.queue.task_done()

    def start(self):
        if not self.task:
            loop = asyncio.get_event_loop()
            self.task = loop.create_task(self._worker())

    def stop(self):
        if self.task:
            self.task.cancel()
            self.task = None

    async def log_async(self, event: str, data: Optional[Dict[str, Any]] = None):
        payload = {"event": event}
        if data:
            payload.update(data)
        try:
            await self.queue.put(payload)
        except asyncio.QueueFull:
            print(json.dumps(payload, ensure_ascii=False))


_audit_instance: Optional[AsyncAuditLogger] = None


def get_audit_logger() -> AsyncAuditLogger:
    global _audit_instance
    if not _audit_instance:
        _audit_instance = AsyncAuditLogger()
    return _audit_instance
