# scripts/pairing_permutation_test.py
import json, argparse, pandas as pd, numpy as np, os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ufrf_knots.pd_features import pd_to_phase_vector
from ufrf_knots.phase_features import l1_cost, composite_cost

def load_pd_map(knots_csv):
    df = pd.read_csv(knots_csv, comment="#")
    m = {}
    for _, r in df.iterrows():
        kid = str(r["knot_id"])
        pd_code = r.get("pd_code", "")
        if not str(pd_code).strip():
            continue
        m[kid] = pd_code
    return m

def build_composite_metrics(left_ids, right_ids, pd_map):
    rows = []
    for L, R in zip(left_ids, right_ids):
        pdL = pd_map.get(L, None); pdR = pd_map.get(R, None)
        if not pdL or not pdR: 
            continue
        v1 = pd_to_phase_vector(pdL); v2 = pd_to_phase_vector(pdR)
        u1 = l1_cost(v1); u2 = l1_cost(v2)
        u12 = composite_cost(v1, v2)
        rows.append(u12 - (u1 + u2))
    arr = np.array(rows, dtype=float)
    return arr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--knots", required=True)        # data/real_knots.csv
    ap.add_argument("--composites", required=True)   # data/real_composites.csv
    ap.add_argument("--n_perm", type=int, default=1000)
    args = ap.parse_args()

    pd_map = load_pd_map(args.knots)
    C = pd.read_csv(args.composites)
    left = C["left_id"].tolist()
    right = C["right_id"].tolist()

    # Observed fraction subadditive
    obs_deltas = build_composite_metrics(left, right, pd_map)
    obs_frac = float((obs_deltas < 0).mean())
    print(f"Observed fraction subadditive: {obs_frac:.6f}  (N={len(obs_deltas)})")

    # Pairing-permutation null
    rng = np.random.default_rng(144001)
    cnt = 0
    for _ in range(args.n_perm):
        rng.shuffle(right)  # re-pair with a random right_id
        deltas = build_composite_metrics(left, right, pd_map)
        frac = float((deltas < 0).mean())
        if frac >= obs_frac:
            cnt += 1
    pval = (cnt + 1) / (args.n_perm + 1)
    print(f"Pairing-permutation p-value: {pval:.6g}")

if __name__ == "__main__":
    main()
