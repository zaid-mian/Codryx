import asyncio
import inspect
from typing import Any, Callable, Dict, Iterable, Optional, Union

from .rule_loader import get_rules
from .utils import is_production, is_strict, json_log, set_strict
from .expr import safe_eval


def enable_strict_mode() -> None:
    set_strict(True)


def _evaluate_condition(expr: str, args: tuple, kwargs: dict) -> bool:
    ctx: Dict[str, Any] = {}
    ctx.update(kwargs)
    for i, v in enumerate(args):
        ctx[f"arg{i}"] = v
    return safe_eval(expr, ctx)


def _check_rules(rules: Iterable[Union[str, Dict[str, Any]]], args: tuple, kwargs: dict) -> None:
    for r in rules:
        if isinstance(r, str):
            ok = _evaluate_condition(r, args, kwargs)
            if not ok:
                json_log("guard_fail", {"rule": r})
                raise PermissionError("Guard condition failed")
        elif isinstance(r, dict):
            expr = r.get("condition") or ""
            ok = _evaluate_condition(expr, args, kwargs)
            if not ok:
                json_log("guard_fail", {"rule": expr})
                raise PermissionError("Guard condition failed")


def guard(condition: Optional[Union[str, Iterable[Union[str, Dict[str, Any]]]]]=None, rules: Optional[str]=None) -> Callable:
    def decorator(fn: Callable) -> Callable:
        async def async_wrapper(*args, **kwargs):
            if not is_production() or is_strict():
                if rules:
                    rule_set = get_rules(rules)
                    _check_rules(rule_set.get("rules", []), args, kwargs)
                elif condition:
                    items = [condition] if isinstance(condition, str) else list(condition)
                    _check_rules(items, args, kwargs)
            return await fn(*args, **kwargs)

        def sync_wrapper(*args, **kwargs):
            if not is_production() or is_strict():
                if rules:
                    rule_set = get_rules(rules)
                    _check_rules(rule_set.get("rules", []), args, kwargs)
                elif condition:
                    items = [condition] if isinstance(condition, str) else list(condition)
                    _check_rules(items, args, kwargs)
            return fn(*args, **kwargs)

        if inspect.iscoroutinefunction(fn):
            return async_wrapper
        return sync_wrapper
    return decorator
