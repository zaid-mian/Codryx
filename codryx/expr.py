import ast
from typing import Any, Dict


ALLOWED_NODES = {
    ast.Expression,
    ast.BoolOp,
    ast.BinOp,
    ast.UnaryOp,
    ast.Compare,
    ast.Name,
    ast.Load,
    ast.And,
    ast.Or,
    ast.Not,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.Is,
    ast.IsNot,
    ast.In,
    ast.NotIn,
    ast.Constant,
    ast.Attribute,
}


def _safe_getattr(obj: Any, attr: str) -> Any:
    try:
        return getattr(obj, attr)
    except Exception:
        return None


def _resolve_attribute(root: Any, path: str) -> Any:
    cur = root
    for part in path.split("."):
        cur = _safe_getattr(cur, part)
    return cur


def safe_eval(expr: str, context: Dict[str, Any]) -> bool:
    try:
        tree = ast.parse(expr, mode="eval")
    except Exception:
        return False
    for node in ast.walk(tree):
        if type(node) not in ALLOWED_NODES:
            return False
    def eval_node(node: ast.AST) -> Any:
        if isinstance(node, ast.Expression):
            return eval_node(node.body)
        if isinstance(node, ast.BoolOp):
            values = [bool(eval_node(v)) for v in node.values]
            if isinstance(node.op, ast.And):
                return all(values)
            return any(values)
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.Not):
            return not bool(eval_node(node.operand))
        if isinstance(node, ast.Compare):
            left = eval_node(node.left)
            for op, comparator in zip(node.ops, node.comparators):
                right = eval_node(comparator)
                if isinstance(op, ast.Eq):
                    if not left == right:
                        return False
                elif isinstance(op, ast.NotEq):
                    if not left != right:
                        return False
                elif isinstance(op, ast.Lt):
                    if not left < right:
                        return False
                elif isinstance(op, ast.LtE):
                    if not left <= right:
                        return False
                elif isinstance(op, ast.Gt):
                    if not left > right:
                        return False
                elif isinstance(op, ast.GtE):
                    if not left >= right:
                        return False
                else:
                    return False
                left = right
            return True
        if isinstance(node, ast.Name):
            return context.get(node.id)
        if isinstance(node, ast.Attribute):
            root = eval_node(node.value)
            return _safe_getattr(root, node.attr)
        if isinstance(node, ast.Constant):
            return node.value
        return False
    return bool(eval_node(tree))
