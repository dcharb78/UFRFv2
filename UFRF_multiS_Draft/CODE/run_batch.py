
import argparse, os, glob, json, pandas as pd
from CODE.run_prior_test import run_one

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", required=False, default="DATA", help="Folder with .s1p/.s2p files")
    ap.add_argument("--sij", default="11", help="11,21,12,22")
    ap.add_argument("--outdir", required=False, default="results/batch", help="Output root")
    ap.add_argument("--prior", choices=["on","off"], default="on")
    ap.add_argument("--test-frac", type=float, default=0.2)
    ap.add_argument("--split", choices=["random","interleave"], default="random")
    ap.add_argument("--n-cycles", type=int, default=13)
    ap.add_argument("--poly-deg", type=int, default=3)
    ap.add_argument("--ridge", type=float, default=1e-3)
    ap.add_argument("--z0", type=float, default=None)
    ap.add_argument("--delay", choices=["on","off"], default="on")
    ap.add_argument("--gate-threshold", type=float, default=0.02)
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.indir, "*.s?p")))
    os.makedirs(args.outdir, exist_ok=True)
    leaderboard = []
    for fp in files:
        name = os.path.splitext(os.path.basename(fp))[0]
        outdir = os.path.join(args.outdir, f"{name}_S{args.sij}")
        try:
            run_one(fp, outdir, sij=args.sij, prior=(args.prior=="on"),
                    test_frac=args.test_frac, split=args.split,
                    n_cycles=args.n_cycles, poly_deg=args.poly_deg, ridge=args.ridge, z0_override=args.z0,
                    delay=(args.delay=="on"), gate_threshold=args.gate_threshold)
            with open(os.path.join(outdir,"params.json")) as f:
                res = json.load(f)
            row = {"file": os.path.basename(fp), "Sij": res["Sij"],
                   "baseline_test_MSE": res["baseline"]["test_MSE"]}
            if "ufrf_prior" in res:
                row["ufrf_test_MSE"] = res["ufrf_prior"]["test_MSE"]
                row["improvement_percent"] = res["ufrf_prior"]["improvement_percent"]
            # include gating meta if present
            if "train_improvement_percent" in res:
                row["train_improvement_percent"] = res["train_improvement_percent"]
            if "gate_threshold_percent" in res:
                row["gate_threshold_percent"] = res["gate_threshold_percent"]
            if "gated" in res:
                row["gated"] = res["gated"]
            leaderboard.append(row)
        except Exception as e:
            leaderboard.append({"file": os.path.basename(fp), "Sij": f"S{args.sij}", "error": str(e)})
    pd.DataFrame(leaderboard).to_csv(os.path.join(args.outdir,"leaderboard.csv"), index=False)
    print(f"Wrote {len(files)} results to {args.outdir}")

if __name__ == "__main__":
    main()
