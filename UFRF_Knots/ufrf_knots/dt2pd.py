import json

def dt_to_pd(dt):
    """
    Toy DT→PD mapper:
    - Input: list of even ints (DT code).
    - Output: list of 4-tuples forming a synthetic PD-like structure for demo purposes.
    This does NOT reproduce a true PD; replace with a real converter if available.
    """
    if isinstance(dt, str):
        dt = json.loads(dt)
    dt = [int(x) for x in dt]
    pd = []
    n = len(dt)
    for i, val in enumerate(dt):
        a = 2*i + 1
        b = (2*i + 2)
        c = (2*((i+1)%n) + 1) if n else 1
        d = (2*((i+2)%n) + 2) if n > 2 else (b + 2)
        pd.append((a, b+val, c, d+val//2))
    return pd
