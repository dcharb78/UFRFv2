import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import argparse, json, os
import pandas as pd
import matplotlib.pyplot as plt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    with open(args.results, "r") as f:
        data = json.load(f)

    df = pd.DataFrame(data["composites"])

    # Histogram of Δu
    plt.figure(figsize=(8,5))
    bins = range(int(df["delta"].min())-1, int(df["delta"].max())+2)
    plt.hist(df["delta"], bins=bins, edgecolor='black')
    plt.title("Distribution of Δu = u(K1#K2) - [u(K1)+u(K2)]")
    plt.xlabel("Δu (negative = subadditive)")
    plt.ylabel("Count")
    p1 = os.path.join(args.out, "plot_delta_hist.png")
    plt.tight_layout()
    plt.savefig(p1); plt.close()

    # Δu vs cosine similarity
    plt.figure(figsize=(8,5))
    plt.scatter(df["cosine"], df["delta"], s=10, alpha=0.6)
    plt.title("Δu vs Cosine Similarity")
    plt.xlabel("Cosine similarity")
    plt.ylabel("Δu")
    p2 = os.path.join(args.out, "plot_delta_vs_cosine.png")
    plt.tight_layout()
    plt.savefig(p2); plt.close()

    # Δu vs opposed-phase overlap
    plt.figure(figsize=(8,5))
    plt.scatter(df["oppose_overlap"], df["delta"], s=10, alpha=0.6)
    plt.title("Δu vs Opposed-Phase Overlap")
    plt.xlabel("Opposed-phase overlap")
    plt.ylabel("Δu")
    p3 = os.path.join(args.out, "plot_delta_vs_overlap.png")
    plt.tight_layout()
    plt.savefig(p3); plt.close()

    # Summary CSV
    df.to_csv(os.path.join(args.out, "composite_metrics.csv"), index=False)

    # Print a small summary
    print("N composites:", len(df))
    print("Fraction subadditive:", (df["delta"] < 0).mean())
    print("Mean Δu:", df["delta"].mean())

from ufrf_knots.analysis_utils import permutation_test_subadditivity, simple_regression_delta, stability_check
import json, os, glob

if __name__ == "__main__":
    main()

    # After main ran, try to locate the latest output args via env (when called by run_all.sh)
    import sys
    # This block assumes the script is run as in the README; otherwise ignore.
    try:
        # Infer recent results path from argv
        res_idx = sys.argv.index("--results") + 1
        res_path = sys.argv[res_idx]
        with open(res_path, "r") as f:
            data = json.load(f)
        comps = pd.DataFrame(data["composites"])

        print("\n--- Permutation test (subadditivity fraction) ---")
        pval = permutation_test_subadditivity(comps, n_perm=2000)
        print(f"permutation_p: {pval:.6g}")

        print("\n--- Regression: delta ~ cosine + overlap ---")
        reg = simple_regression_delta(comps)
        print("coeffs:", reg["coeffs"])
        print("stderr:", reg["stderr"])
        print("tstats:", reg["tstats"])

        # Optional stability if re-diagramming outputs exist alongside
        rd_dir = os.path.join(os.path.dirname(os.path.dirname(res_path)), "rediag_runs")
        if os.path.isdir(rd_dir):
            run_files = sorted(glob.glob(os.path.join(rd_dir, "rediag_*.csv")))
            if run_files:
                dfs = [pd.read_csv(p) for p in run_files]
                stab = stability_check(dfs)
                print("\n--- Re-diagramming stability ---")
                print(json.dumps(stab, indent=2))
    except Exception as e:
        print("Extra analyses skipped:", e)



# Extra analyses for paper-ready stats
if __name__ == "__main__":
    pass
