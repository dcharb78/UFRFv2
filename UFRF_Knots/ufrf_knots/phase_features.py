import json
import numpy as np

def parse_phase_vector(s: str) -> np.ndarray:
    if isinstance(s, (list, tuple)):
        arr = np.array(s, dtype=int)
    else:
        arr = np.array(json.loads(s), dtype=int)
    if arr.shape[0] != 13:
        raise ValueError("phase_vector must have length 13")
    return arr

def l1_cost(v: np.ndarray) -> int:
    return int(np.abs(v).sum())

def composite_cost(v1: np.ndarray, v2: np.ndarray) -> int:
    oppose = (v1 * v2) < 0
    overlap = np.minimum(np.abs(v1), np.abs(v2)) * oppose
    return int(np.abs(v1).sum() + np.abs(v2).sum() - overlap.sum())

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    a = float(np.linalg.norm(v1))
    b = float(np.linalg.norm(v2))
    if a == 0.0 or b == 0.0:
        return 0.0
    return float(np.dot(v1, v2) / (a * b))

def opposed_phase_overlap(v1: np.ndarray, v2: np.ndarray) -> int:
    oppose = (v1 * v2) < 0
    return int((np.minimum(np.abs(v1), np.abs(v2)) * oppose).sum())


from .mwrithe import dt_to_phase_vector_multiscale as dt_to_phase_vector_ms

def composite_cost_ms(dt1, dt2):
    v1 = dt_to_phase_vector_ms(dt1)
    v2 = dt_to_phase_vector_ms(dt2)
    return composite_cost(v1, v2)
