# Minimal DT-code parsing helpers (stub).
# For real use, prefer a robust library. Here we store DT codes as strings.
# This module keeps the interface tidy even if SnapPy is not installed.

def parse_dt_code(dt: str):
    dt = dt.strip()
    if not dt:
        return None
    # Expect a comma/space separated list of ints inside [ ... ] or raw.
    dt = dt.replace('[','').replace(']','')
    parts = [p.strip() for p in dt.replace(';',',').split(',') if p.strip()]
    try:
        return [int(x) for x in parts]
    except Exception:
        raise ValueError(f"Invalid DT code: {dt}")
