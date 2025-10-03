
import csv, math, argparse, os, time
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def read_csv(path):
    rows = []
    with open(path, "r", newline="") as f:
        r = csv.DictReader(f)
        for row in r:
            rows.append({k: (v.strip() if isinstance(v,str) else v) for k,v in row.items()})
    return rows

def to_f(x):
    try:
        if x is None or x == "": return None
        return float(x)
    except:
        return None

def pca_pc1(X):
    X = np.array(X, dtype=float)
    col_means = np.nanmean(X, axis=0)
    inds = np.where(np.isnan(X))
    X[inds] = np.take(col_means, inds[1])
    mu = np.mean(X, axis=0)
    sd = np.std(X, axis=0); sd[sd==0]=1.0
    Z = (X - mu)/sd
    U, s, Vt = np.linalg.svd(Z, full_matrices=False)
    scores = U[:,0]*s[0]
    var = (s[0]**2)/np.sum(s**2) if np.sum(s**2)>0 else float("nan")
    return scores, var

def ols_log_linear(S, O):
    y = np.log(np.maximum(1e-300, O))
    x = np.array(S, dtype=float)
    X = np.vstack([np.ones_like(x), x]).T
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    a, b = beta
    resid = y - (a + b*x)
    dof = max(1, len(y)-2)
    s2 = float(resid.T @ resid) / dof
    return a, b, s2

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wl", default="data/locuss_wl_m500.csv")
    ap.add_argument("--hse", default="data/locuss_hse_m500.csv")
    ap.add_argument("--out", default="runs")
    args = ap.parse_args()

    outdir = Path(args.out) / time.strftime("%Y%m%d_%H%M%S")
    outdir.mkdir(parents=True, exist_ok=True)

    wl = read_csv(args.wl)
    hse = read_csv(args.hse)

    wl_by = {r["cluster_id"]: r for r in wl}
    rows = []
    for r in hse:
        cid = r["cluster_id"]
        if cid in wl_by:
            rr = {"cluster_id": cid, "z": r.get("z") or wl_by[cid].get("z")}
            rr.update({k: wl_by[cid].get(k) for k in wl_by[cid]})
            rr.update({k: r.get(k) for k in r})
            rows.append(rr)

    # Build per-probe S
    X_wl = [[to_f(r.get("psf_over_size")), to_f(r.get("snr")), to_f(r.get("photoz_width"))] for r in rows]
    X_hse = [[to_f(r.get("hydro_bkg")), to_f(r.get("temp_model_flex"))] for r in rows]
    import numpy as np
    S_wl, var_wl = pca_pc1(X_wl)
    S_hse, var_hse = pca_pc1(X_hse)

    M_wl = np.array([to_f(r.get("M500_WL")) for r in rows], dtype=float)
    M_hse = np.array([to_f(r.get("M500_HSE")) for r in rows], dtype=float)

    a_wl, b_wl, s2_wl = ols_log_linear(S_wl, M_wl)
    a_hse, b_hse, s2_hse = ols_log_linear(S_hse, M_hse)

    # Ratio regression in log space: ln(M_HSE/M_WL) = a + b*(S_hse - S_wl) + eps
    ratio = np.log(np.maximum(1e-300, M_hse / M_wl))
    S_ratio = S_hse - S_wl
    X = np.vstack([np.ones_like(S_ratio), S_ratio]).T
    beta, *_ = np.linalg.lstsq(X, ratio, rcond=None)
    a_r, b_r = beta
    resid = ratio - (a_r + b_r*S_ratio)
    dof = max(1, len(ratio)-2)
    s2_r = float(resid.T @ resid) / dof

    # Write summary
    with open(outdir/"RUN_SUMMARY.md", "w") as f:
        f.write("# LoCuSS UFRF Projection Validation\n\n")
        f.write("## Per-probe fits (log M = a + b S)\n\n")
        f.write("probe, PC1_var, b(≈dM·α), M_*(S=0)\n")
        f.write(f"WL,{var_wl:.3f},{b_wl:.6g},{math.exp(a_wl):.6g}\n")
        f.write(f"HSE,{var_hse:.3f},{b_hse:.6g},{math.exp(a_hse):.6g}\n\n")
        f.write("## Mass-ratio regression\n\n")
        f.write("model, slope, intercept, residual_var\n")
        f.write(f"ln(M_HSE/M_WL) ~ (S_hse - S_wl),{b_r:.6g},{a_r:.6g},{s2_r:.6g}\n")

    # Plots
    import matplotlib.pyplot as plt
    xs = np.linspace(np.nanmin(S_wl), np.nanmax(S_wl), 200)
    plt.figure(); plt.title("WL: log M vs S_WL")
    plt.scatter(S_wl, M_wl); plt.plot(xs, np.exp(a_wl + b_wl*xs))
    plt.xlabel("S_WL (PC1)"); plt.ylabel("M500_WL")
    plt.savefig(outdir/"FIT_WL.png", dpi=120, bbox_inches="tight"); plt.close()

    xs2 = np.linspace(np.nanmin(S_hse), np.nanmax(S_hse), 200)
    plt.figure(); plt.title("HSE: log M vs S_HSE")
    plt.scatter(S_hse, M_hse); plt.plot(xs2, np.exp(a_hse + b_hse*xs2))
    plt.xlabel("S_HSE (PC1)"); plt.ylabel("M500_HSE")
    plt.savefig(outdir/"FIT_HSE.png", dpi=120, bbox_inches="tight"); plt.close()

    xs3 = np.linspace(np.nanmin(S_ratio), np.nanmax(S_ratio), 200)
    plt.figure(); plt.title("ln(M_HSE/M_WL) vs S_HSE - S_WL")
    plt.scatter(S_ratio, ratio); plt.plot(xs3, a_r + b_r*xs3)
    plt.xlabel("S_ratio"); plt.ylabel("ln ratio")
    plt.savefig(outdir/"RATIO_vs_S.png", dpi=120, bbox_inches="tight"); plt.close()

    print("WROTE", outdir/"RUN_SUMMARY.md")

if __name__ == "__main__":
    main()
