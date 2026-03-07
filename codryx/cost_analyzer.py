from typing import Dict


def estimate_cost(dep_scan: Dict[str, Dict[str, str]]) -> Dict[str, float]:
    total = len(dep_scan)
    outdated = sum(1 for v in dep_scan.values() if v.get("outdated") == "yes")
    score = 100.0 - (outdated / max(total, 1)) * 50.0
    build_time_penalty = outdated * 0.5
    return {"health_score": round(score, 2), "build_time_penalty_minutes": round(build_time_penalty, 2)}
