
import numpy as np
import json

def _normalize(vec):
    n = np.linalg.norm(vec)
    return vec if n == 0 else vec / n

def dt_to_signal(dt_seq):
    # Convert DT even integers to a 1D signed "crossing signal"
    # Alternate sign by index to mimic over/under orientation.
    s = []
    for i, val in enumerate(dt_seq):
        sign = -1.0 if (i % 2 == 0) else 1.0
        amp = float((val // 2) % 7 + 1)  # bounded magnitude
        s.append(sign * amp)
    return np.array(s, dtype=float)

def multiscale_writhe_signal(signal, scales=(3,5,7,9,11,13)):
    # For each odd window size, compute a convolution (moving sum)
    # and take summary stats (mean, std, signed max) to form features.
    feats = []
    for w in scales:
        if w > len(signal):
            # pad with zeros to keep dimensions stable
            feats.extend([0.0, 0.0, 0.0])
            continue
        kernel = np.ones(w)
        conv = np.convolve(signal, kernel, mode='valid')
        feats.append(float(conv.mean()))
        feats.append(float(conv.std()))
        # signed extreme to preserve orientation bias
        max_idx = int(np.argmax(np.abs(conv)))
        feats.append(float(conv[max_idx]))
    return np.array(feats, dtype=float)

def project_to_13_phase(feat_vec):
    # Map the multiscale feature vector (len = 3*len(scales)) to 13 bins:
    # simple linear projection with a fixed pseudo-random matrix (seeded).
    rng = np.random.default_rng(144000)
    P = rng.normal(size=(13, feat_vec.shape[0]))
    v = P @ feat_vec
    # round to nearest integer to interpret as discrete obstruction units
    return np.rint(v).astype(int)

def dt_to_phase_vector_multiscale(dt_seq):
    s = dt_to_signal(dt_seq)
    f = multiscale_writhe_signal(s)
    v13 = project_to_13_phase(f)
    return v13
