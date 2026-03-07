from typing import Any, Dict, Optional

from .utils import load_rules


def get_rules(source: Optional[str]) -> Dict[str, Any]:
    if not source:
        return {"rules": []}
    return load_rules(source)
