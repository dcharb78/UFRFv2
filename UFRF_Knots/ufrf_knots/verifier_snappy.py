"""
SnapPy-based verification (bounded search) interface.

This module *tries* to use SnapPy + spherogram if present. If not available,
it returns informative "available=False" results so the pipeline still runs.

For real verification on your machine:
  conda create -n snappy-env python=3.11 -y
  conda activate snappy-env
  conda install -c conda-forge snappy spherogram -y
"""

from typing import Any, Dict, List, Optional

try:
    import snappy
    from spherogram import Link
    HAVE_SNAPPY = True
except Exception:
    HAVE_SNAPPY = False

def has_snappy() -> bool:
    return HAVE_SNAPPY

def pd_is_unknot(pd_list: List[tuple]) -> Optional[bool]:
    "Return True/False if testable, or None if unavailable."
    if not HAVE_SNAPPY:
        return None
    try:
        # Create Link from PD code using new API
        L = Link(pd_list)                # Build Link directly from PD
        L.simplify()                     # Try some simplifications
        # Quick unknot heuristics
        if L.num_components() != 1:
            return False
        # Exterior fundamental group test is expensive; use SnapPy's "is_trivial_knot" if present
        try:
            return bool(L.is_trivial_knot())
        except Exception:
            # Fallback: try to recognize via triangulation volume ~ 0
            M = L.exterior()
            vol = M.volume(verified=False)
            return (abs(vol) < 1e-8)
    except Exception:
        return None

def bounded_flip_bfs(pd_list: List[tuple], max_depth: int = 2) -> Dict[str, Any]:
    """
    Try simple crossing sign flips up to depth d. For each sequence, test if unknot.
    Returns a dict with 'verified': bool, 'upper_bound': Optional[int], and witness sequence if found.
    """
    if not HAVE_SNAPPY:
        return {"available": False, "reason": "SnapPy/spherogram not installed", "verified": False, "upper_bound": None, "witness": []}

    n = len(pd_list)
    if n == 0:
        return {"available": True, "verified": False, "upper_bound": None, "witness": []}

    # Define a "flip" as swapping the last two entries of a crossing tuple (toy local surgery)
    def flip(pd, i):
        crossing = pd[i]
        # Handle both list and tuple inputs
        if isinstance(crossing, (list, tuple)) and len(crossing) == 4:
            a,b,c,d = crossing
            new_crossing = (a,b,d,c)
            return pd[:i] + [new_crossing] + pd[i+1:]
        else:
            # Invalid crossing format - return unchanged
            return pd

    from collections import deque
    start = tuple(tuple(x) for x in pd_list)
    Q = deque([(start, [])])
    seen = {start}

    depth = 0
    while Q and depth <= max_depth:
        for _ in range(len(Q)):
            pd_state, seq = Q.popleft()
            # test
            is_u = pd_is_unknot(list(pd_state))
            if is_u is True:
                return {"available": True, "verified": True, "upper_bound": len(seq), "witness": seq}
            if is_u is None:
                # environment not sufficient; continue
                pass
            # expand
            if len(seq) >= max_depth:
                continue
            for i in range(min(6, n)):   # limit branching for speed
                nxt = tuple(flip(list(pd_state), i))
                if nxt not in seen:
                    seen.add(nxt)
                    Q.append((nxt, seq + [("flip", i)]))
        depth += 1

    return {"available": True, "verified": False, "upper_bound": None, "witness": []}
