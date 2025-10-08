
import argparse, os, glob, json, pandas as pd
from CODE.run_prior_test_delay import run_one

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--indir", default="DATA")
    ap.add_argument("--sij", choices=["21","12"], default="21")
    ap.add_argument("--outdir", default="results/batch_s21_delay")
    ap.add_argument("--split", choices=["random","interleave","block"], default="block")
    ap.add_argument("--test-frac", type=float, default=0.2)
    ap.add_argument("--block-frac", type=float, default=0.2)
    ap.add_argument("--deg", type=int, default=3)
    ap.add_argument("--ridge", type=float, default=1e-3)
    ap.add_argument("--n-cycles", type=int, default=13)
    ap.add_argument("--gate", type=float, default=0.02)
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(args.indir, "*.s2p")))
    board = []
    for fp in files:
        name = os.path.splitext(os.path.basename(fp))[0]
        outdir = os.path.join(args.outdir, f"{name}_S{args.sij}")
        try:
            run_one(fp, outdir, sij=args.sij, split=args.split, test_frac=args.test_frac,
                    block_frac=args.block_frac, deg=args.deg, ridge=args.ridge,
                    n_cycles=args.n_cycles, gate=args.gate)
            with open(os.path.join(outdir,"params.json")) as f:
                res = json.load(f)
            row = {"file": os.path.basename(fp), **res}
            board.append(row)
        except Exception as e:
            board.append({"file": os.path.basename(fp), "Sij": f"S{args.sij}", "error": str(e)})
    pd.DataFrame(board).to_csv(os.path.join(args.outdir, "leaderboard_delay.csv"), index=False)
    print(f"Wrote {len(files)} results to {args.outdir}")

if __name__=="__main__":
    main()
