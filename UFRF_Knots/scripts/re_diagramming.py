import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse, json, os, numpy as np, pandas as pd
from ufrf_knots.pd_features import pd_to_phase_vector
from ufrf_knots.dt2pd import dt_to_pd
from ufrf_knots.diagram_formats import parse_dt_code
from ufrf_knots.phase_features import l1_cost, composite_cost, cosine_similarity, opposed_phase_overlap

def random_pd_perturb(pd_list, seed=None, n_swaps=2):
    rng = np.random.default_rng(seed)
    pd_list = [list(c) for c in pd_list]
    for _ in range(n_swaps):
        i = rng.integers(0, len(pd_list))
        a,b,c,d = pd_list[i]
        # swap b<->c or c<->d randomly
        if rng.random() < 0.5:
            pd_list[i] = [a,c,b,d]
        else:
            pd_list[i] = [a,b,d,c]
    return [tuple(x) for x in pd_list]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--knots", required=True)
    ap.add_argument("--composites", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--runs", type=int, default=10)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    K = pd.read_csv(args.knots)
    C = pd.read_csv(args.composites)
    kmap = { r.knot_id: r for _,r in K.iterrows() }

    all_runs = []
    for rix in range(args.runs):
        rows = []
        for _, c in C.iterrows():
            L = kmap[c.left_id]
            R = kmap[c.right_id]
            # Build PDs (dt->pd fallback if pd_code col missing)
            try:
                pdL = json.loads(L.get("pd_code",""))
            except Exception:
                pdL = None
            if pdL is None or pdL == "" or pdL == []:
                dtL = parse_dt_code(str(L.dt_code)) if str(L.dt_code).strip() else []
                pdL = dt_to_pd(dtL) if dtL else []
            try:
                pdR = json.loads(R.get("pd_code",""))
            except Exception:
                pdR = None
            if pdR is None or pdR == "" or pdR == []:
                dtR = parse_dt_code(str(R.dt_code)) if str(R.dt_code).strip() else []
                pdR = dt_to_pd(dtR) if dtR else []
            # Perturb
            pdL2 = random_pd_perturb(pdL, seed=rix)
            pdR2 = random_pd_perturb(pdR, seed=rix+1)
            # Phase
            v1 = pd_to_phase_vector(pdL2) if pdL2 else None
            v2 = pd_to_phase_vector(pdR2) if pdR2 else None
            if v1 is None or v2 is None:
                continue
            u1 = l1_cost(v1); u2 = l1_cost(v2)
            u12 = composite_cost(v1, v2)
            rows.append({
                "composite_id": c.composite_id,
                "left_id": c.left_id,
                "right_id": c.right_id,
                "u1": int(u1), "u2": int(u2), "u12": int(u12),
                "delta": int(u12 - (u1 + u2)),
                "cosine": float(cosine_similarity(v1, v2)),
                "oppose_overlap": int(opposed_phase_overlap(v1, v2))
            })
        df = pd.DataFrame(rows)
        df.to_csv(os.path.join(args.out, f"rediag_{rix}.csv"), index=False)
        all_runs.append(df)

    # Save a summary index
    with open(os.path.join(args.out, "index.json"), "w") as f:
        json.dump({"runs": args.runs, "files": [f"rediag_{i}.csv" for i in range(args.runs)]}, f, indent=2)

if __name__ == "__main__":
    main()
