import argparse, pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--knots", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--pairs", choices=["all","cross"], default="all",
                    help="'all' = all ordered pairs (i!=j); 'cross' = only mirror/paired names if they share a base prefix")
    args = ap.parse_args()

    df = pd.read_csv(args.knots, comment="#")
    ids = [k for k in df["knot_id"].tolist() if isinstance(k, str) and len(k) > 0]

    rows = []
    if args.pairs == "all":
        for i, a in enumerate(ids):
            for j, b in enumerate(ids):
                if i == j: 
                    continue
                rows.append({"composite_id": f"C_{a}__{b}", "left_id": a, "right_id": b})
    else:
        # 'cross' mode: pair items that end with '_mirror' to their non-mirror base
        base = {}
        for k in ids:
            if k.endswith("_mirror"):
                base.setdefault(k.replace("_mirror",""), []).append(k)
            else:
                base.setdefault(k, [])
        for b, mirrors in base.items():
            for m in mirrors:
                rows.append({"composite_id": f"C_{b}__{m}", "left_id": b, "right_id": m})
                rows.append({"composite_id": f"C_{m}__{b}", "left_id": m, "right_id": b})

    out_df = pd.DataFrame(rows)
    out_df.to_csv(args.out, index=False)
    print(f"Wrote {args.out} with {len(out_df)} composites.")

if __name__ == "__main__":
    main()
