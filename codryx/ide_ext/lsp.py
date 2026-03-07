import asyncio
from typing import Tuple
from .vscode_lsp import server as vscode_server
from .pycharm_lsp import server as pycharm_server
from .vscode import quickfix_unused_imports as vs_qf
from .pycharm import quickfix_unused_imports as pc_qf


def start_server(host: str = "127.0.0.1", port: int = 8766, flavor: str = "vscode") -> Tuple[bool, str]:
    async def runner():
        if flavor == "pycharm":
            ok = await pycharm_server.start(host, port)
            return ok
        ok = await vscode_server.start(host, port)
        return ok
    try:
        asyncio.run(runner())
        return True, f"IDE LSP server started at ws://{host}:{port}/ ({flavor})"
    except Exception as e:
        return False, str(e)


def apply_quickfix(source: str, fix_kind: str, flavor: str = "vscode"):
    if fix_kind == "unused_imports":
        if flavor == "pycharm":
            return pc_qf(source)
        return vs_qf(source)
    return source, []
