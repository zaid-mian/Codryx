from typing import Optional


def should_gate_fail(score: float, threshold: Optional[float]) -> bool:
    if threshold is None:
        return False
    return score < float(threshold)
