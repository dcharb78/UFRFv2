import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse, json, csv, os
import pandas as pd
import numpy as np

from ufrf_knots.phase_features import (
    parse_phase_vector, l1_cost, composite_cost, cosine_similarity, opposed_phase_overlap
)
from ufrf_knots.diagram_formats import parse_dt_code
from ufrf_knots.unknotting_estimator import estimate_unknotting_number_via_snappy, has_snappy
from ufrf_knots.mwrithe import dt_to_phase_vector_multiscale
from ufrf_knots.pd_features import pd_to_phase_vector
from ufrf_knots.dt2pd import dt_to_pd

def load_knots(path):
    rows = []
    df = pd.read_csv(path, comment="#")
    for _, r in df.iterrows():
        rows.append({
            "knot_id": r["knot_id"],
            "dt_code": r.get("dt_code", ""),
            "pd_code": r.get("pd_code", ""),
            "phase_vector": parse_phase_vector(r.get("phase_vector","[0,0,0,0,0,0,0,0,0,0,0,0,0]"))
        })
    return rows

def load_composites(path):
    rows = []
    df = pd.read_csv(path, comment="#")
    for _, r in df.iterrows():
        rows.append({
            "composite_id": r["composite_id"],
            "left_id": r["left_id"],
            "right_id": r["right_id"]
        })
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["phase","snap"], default="phase")
    ap.add_argument("--feature_mode", choices=["heuristic","multiscale"], default="multiscale")
    ap.add_argument("--geometry_mode", choices=["dt","pd"], default="dt")
    ap.add_argument("--knots", required=True)
    ap.add_argument("--composites", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max_depth", type=int, default=2)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)

    knots = load_knots(args.knots)
    comps = load_composites(args.composites)

    knot_map = {k["knot_id"]: k for k in knots}

    results = {
        "mode": args.mode,
        "feature_mode": args.feature_mode,
        "geometry_mode": args.geometry_mode,
        "has_snappy": has_snappy(),
        "single": {},
        "composites": []
    }

    # Single-knot phase costs (baseline; may be overwritten by feature_mode)
    for k in knots:
        v = k["phase_vector"]
        if args.feature_mode == "multiscale":
            if args.geometry_mode == "dt":
                dt = parse_dt_code(str(k["dt_code"])) if str(k["dt_code"]).strip() else []
                if dt:
                    v = dt_to_phase_vector_multiscale(dt)
            else:
                # PD path
                pd_code = k.get("pd_code","")
                if str(pd_code).strip():
                    v = pd_to_phase_vector(pd_code)
                else:
                    dt = parse_dt_code(str(k["dt_code"])) if str(k["dt_code"]).strip() else []
                    v = pd_to_phase_vector(dt_to_pd(dt)) if dt else v
        results["single"][k["knot_id"]] = {
            "l1_cost": l1_cost(v),
            "norm2": float(np.linalg.norm(v)),
        }

    # Optional SnapPy upper bounds: use verifier_snappy with PD
    if args.mode == "snap":
        from ufrf_knots.verifier_snappy import bounded_flip_bfs
        for k in knots:
            # build PD
            pd_code = k.get("pd_code","")
            if not str(pd_code).strip():
                dt = parse_dt_code(str(k["dt_code"])) if str(k["dt_code"]).strip() else []
                pd_code = dt_to_pd(dt) if dt else []
            else:
                # Parse JSON string to list
                try:
                    pd_code = json.loads(str(pd_code))
                except (json.JSONDecodeError, TypeError):
                    pd_code = []
            res = bounded_flip_bfs(pd_code, max_depth=args.max_depth)
            results["single"][k["knot_id"]]["snappy"] = res

    # Composite analysis
    for c in comps:
        L = knot_map[c["left_id"]]
        R = knot_map[c["right_id"]]

        # Build features according to geometry/feature mode
        def build_phase(krec):
            v = krec["phase_vector"]
            if args.feature_mode == "multiscale":
                if args.geometry_mode == "dt":
                    dt = parse_dt_code(str(krec["dt_code"])) if str(krec["dt_code"]).strip() else []
                    if dt:
                        v = dt_to_phase_vector_multiscale(dt)
                else:
                    pd_code = krec.get("pd_code","")
                    if str(pd_code).strip():
                        v = pd_to_phase_vector(pd_code)
                    else:
                        dt = parse_dt_code(str(krec["dt_code"])) if str(krec["dt_code"]).strip() else []
                        v = pd_to_phase_vector(dt_to_pd(dt)) if dt else v
            return v

        v1 = build_phase(L)
        v2 = build_phase(R)

        u1 = l1_cost(v1)
        u2 = l1_cost(v2)
        u12 = composite_cost(v1, v2)

        results["composites"].append({
            "composite_id": c["composite_id"],
            "left_id": L["knot_id"],
            "right_id": R["knot_id"],
            "u1": int(u1),
            "u2": int(u2),
            "u12": int(u12),
            "delta": int(u12 - (u1 + u2)),
            "cosine": float(cosine_similarity(v1, v2)),
            "oppose_overlap": int(opposed_phase_overlap(v1, v2))
        })

    out_json = os.path.join(args.out, "phase_results.json")
    with open(out_json, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Wrote {out_json}")

if __name__ == "__main__":
    main()
