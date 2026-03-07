import json
import os
from typing import Any, Dict, Optional


def is_production() -> bool:
    return os.getenv("PY_GUARDIAN_MODE", "").lower() == "production"


def is_strict() -> bool:
    return os.getenv("PY_GUARDIAN_STRICT", "").lower() in {"1", "true", "yes"}


def set_strict(enabled: bool) -> None:
    os.environ["PY_GUARDIAN_STRICT"] = "1" if enabled else "0"


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_yaml(path: str) -> Any:
    import importlib
    yaml = importlib.import_module("yaml")
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_rules(path: str) -> Dict[str, Any]:
    if path.endswith(".json"):
        data = load_json(path)
    elif path.endswith(".yml") or path.endswith(".yaml"):
        data = load_yaml(path)
    else:
        raise ValueError("Unsupported rule file")
    return data if isinstance(data, dict) else {"rules": data}


def json_log(event: str, data: Optional[Dict[str, Any]] = None) -> None:
    payload = {"event": event}
    if data:
        payload.update(data)
    try:
        from .config import load_config
        from .audit import get_audit_logger
        cfg = load_config()
        if cfg.audit_async:
            logger = get_audit_logger()
            logger.start()
            import asyncio
            if asyncio.get_event_loop().is_running():
                asyncio.create_task(logger.log_async(event, data))
            else:
                asyncio.run(logger.log_async(event, data))
            return
    except Exception:
        pass
    print(json.dumps(payload, ensure_ascii=False))
