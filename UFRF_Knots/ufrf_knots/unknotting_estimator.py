# Bounded-depth crossing-change search with optional SnapPy verification.
# This is intentionally simple; it demonstrates how you'd integrate a true verifier.

from typing import Optional, Dict, Any
try:
    import snappy
except Exception:
    snappy = None

def has_snappy() -> bool:
    return snappy is not None

def estimate_unknotting_number_via_snappy(dt_code: list[int], max_depth: int = 2) -> Dict[str, Any]:
    if snappy is None:
        return {
            "available": False,
            "reason": "SnapPy not installed",
            "upper_bound": None,
            "verified": False
        }
    # Placeholder: in reality you'd convert DT->PD->SnapPy Link, then BFS crossing flips.
    # We return a stub result to show the JSON schema.
    try:
        # example stub; real conversion omitted
        return {
            "available": True,
            "reason": "stub",
            "upper_bound": None,
            "verified": False
        }
    except Exception as e:
        return {
            "available": False,
            "reason": f"error: {e}",
            "upper_bound": None,
            "verified": False
        }
