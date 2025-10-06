import numpy as np
import json

def parse_pd(pd_str):
    """
    Parse a very simple PD format:
    - Input: JSON string of a list of crossings; each crossing is a 4-tuple of ints (a,b,c,d)
      following a PD-like convention (over/under arcs listed cyclically).
    - This is intentionally lightweight. For serious use, replace with a robust PD parser.
    """
    if isinstance(pd_str, (list, tuple)):
        return [tuple(int(x) for x in t) for t in pd_str]
    return [tuple(int(x) for x in t) for t in json.loads(pd_str)]

def pd_writhe(pd):
    """
    Crude writhe proxy from PD:
    Count 'right-handed' vs 'left-handed' crossings using a toy rule:
    - For each crossing (a,b,c,d), use (a-c)*(b-d) sign as orientation proxy.
    This is NOT a rigorous writhe; it's a consistent numeric feature for our pipeline demos.
    """
    s = 0
    for (a,b,c,d) in pd:
        val = (a - c)*(b - d)
        s += 1 if val > 0 else (-1 if val < 0 else 0)
    return s

def multiscale_pd_signal(pd):
    """
    Build a 1D signal from PD by walking crossings and appending a signed magnitude
    based on local index differences; then compute multiscale summaries.
    """
    sig = []
    for i,(a,b,c,d) in enumerate(pd):
        base = abs(a-b) + abs(c-d) + abs(a-d) + abs(b-c)
        sign = -1.0 if (i % 2 == 0) else 1.0
        sig.append(sign * float((base % 9) + 1))
    return np.array(sig, dtype=float)

def window_features(signal, windows=(3,5,7,9,11,13)):
    feats = []
    for w in windows:
        if w > len(signal):
            feats.extend([0.0,0.0,0.0])
            continue
        kernel = np.ones(w)
        conv = np.convolve(signal, kernel, mode='valid')
        feats.append(float(conv.mean()))
        feats.append(float(conv.std()))
        m = int(np.argmax(np.abs(conv)))
        feats.append(float(conv[m]))
    return np.array(feats, dtype=float)

def project_to_13(feats, seed=144013):
    rng = np.random.default_rng(seed)
    P = rng.normal(size=(13, feats.shape[0]))
    v = P @ feats
    return np.rint(v).astype(int)

def pd_to_phase_vector(pd_str_or_list):
    pd = parse_pd(pd_str_or_list)
    s = multiscale_pd_signal(pd)
    f = window_features(s)
    v13 = project_to_13(f)
    return v13
