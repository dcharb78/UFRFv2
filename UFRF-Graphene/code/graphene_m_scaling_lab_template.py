#!/usr/bin/env python3
import os, argparse, math, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def ols_with_ci(X, y, alpha=0.05):
    X = np.asarray(X)
    y = np.asarray(y).reshape(-1, 1)
    n, p = X.shape
    XtX = X.T @ X
    XtX_inv = np.linalg.inv(XtX)
    beta = XtX_inv @ X.T @ y
    yhat = X @ beta
    resid = y - yhat
    dof = max(n - p, 1)
    sigma2 = float((resid.T @ resid) / dof)
    se = np.sqrt(np.diag(XtX_inv) * sigma2).reshape(-1, 1)
    # t critical via normal approx (avoid scipy dependency)
    from math import erf, sqrt
    def approx_tcrit(alpha, dof):
        # crude: use normal quantile ~1.96 for 95%
        return 1.96
    tcrit = approx_tcrit(alpha, dof)
    ci_low = (beta - tcrit * se).flatten()
    ci_high = (beta + tcrit * se).flatten()
    beta = beta.flatten()
    ss_tot = float(((y - y.mean())**2).sum())
    ss_res = float((resid**2).sum())
    r2 = 1 - ss_res/ss_tot if ss_tot > 0 else float("nan")
    return beta, se.flatten(), tcrit, ci_low, ci_high, yhat.flatten(), r2

def analyze(meas_path, ratios_path, dM, outdir):
    os.makedirs(outdir, exist_ok=True)

    df = pd.read_csv(meas_path)
    if "technique" not in df or "S_log_M_ratio" not in df or "O_meas" not in df:
        raise ValueError("Missing required columns in measurements CSV.")

    # Per-technique fits
    fit_rows = []
    tech_pred = {}
    for tname, sub in df.groupby("technique"):
        X = np.c_[np.ones(len(sub)), sub["S_log_M_ratio"].values]
        y = np.log(sub["O_meas"].values)
        beta, se, tcrit, lo, hi, yhat, r2 = ols_with_ci(X, y, alpha=0.05)
        a, b = beta
        a_lo, b_lo = lo
        a_hi, b_hi = hi
        fit_rows.append({
            "technique": tname,
            "b_est": b,
            "b_ci_low": b_lo,
            "b_ci_high": b_hi,
            "a_est": a,
            "a_ci_low": a_lo,
            "a_ci_high": a_hi,
            "r2": r2
        })
        xs = np.linspace(sub["S_log_M_ratio"].min(), sub["S_log_M_ratio"].max(), 200)
        Xp = np.c_[np.ones_like(xs), xs]
        yhat_lin = Xp @ np.array([a, b])
        tech_pred[tname] = (xs, np.exp(yhat_lin))

    fit_df = pd.DataFrame(fit_rows)
    fit_df.to_csv(os.path.join(outdir, "per_technique_fits.csv"), index=False)

    # Pooled fixed-effects (technique + device if present)
    tech_dum = pd.get_dummies(df["technique"], prefix="tech", drop_first=True)
    dev_dum = pd.get_dummies(df["device"], prefix="dev", drop_first=True) if "device" in df else pd.DataFrame(index=df.index)
    X_pooled = np.c_[np.ones(len(df)), df["S_log_M_ratio"].values, tech_dum.values, dev_dum.values]
    y_pooled = np.log(df["O_meas"].values)
    beta_pooled, se_pooled, tcrit_pooled, lo_pooled, hi_pooled, yhat_pooled, r2_pooled = ols_with_ci(X_pooled, y_pooled, alpha=0.05)

    coef_names = (["intercept","S"] + tech_dum.columns.tolist() + dev_dum.columns.tolist())
    pooled_table = pd.DataFrame({
        "term": coef_names,
        "beta": beta_pooled[:len(coef_names)],
        "ci_low": lo_pooled[:len(coef_names)],
        "ci_high": hi_pooled[:len(coef_names)],
        "se": se_pooled[:len(coef_names)]
    })
    pooled_table.to_csv(os.path.join(outdir, "pooled_model_coeffs.csv"), index=False)

    baseline_tech = sorted(df["technique"].unique())[0]
    tech_offsets = {baseline_tech: 0.0}
    for col, beta_val in zip(tech_dum.columns.tolist(), beta_pooled[2:2+len(tech_dum.columns)]):
        tech_name = col.replace("tech_", "")
        tech_offsets[tech_name] = beta_val

    # O_* estimates: remove technique offset; CI from intercept bounds
    Ostar_rows = []
    for _, row in fit_df.iterrows():
        tname = row["technique"]
        a_est = row["a_est"]
        offset = tech_offsets.get(tname, 0.0)
        O_star_est = math.exp(a_est - offset)
        O_lo = math.exp(row["a_ci_low"] - offset)
        O_hi = math.exp(row["a_ci_high"] - offset)
        Ostar_rows.append({"technique": tname, "O_star_est": O_star_est, "O_star_CI_low": O_lo, "O_star_CI_high": O_hi})
    Ostar_df = pd.DataFrame(Ostar_rows)
    Ostar_df.to_csv(os.path.join(outdir, "O_star_estimates.csv"), index=False)

    # Plots
    import matplotlib.pyplot as plt
    # α bar with CI
    order = list(fit_df["technique"])
    xpos = np.arange(len(order))
    b_est = fit_df.set_index("technique").loc[order, "b_est"].values
    b_lo = fit_df.set_index("technique").loc[order, "b_ci_low"].values
    b_hi = fit_df.set_index("technique").loc[order, "b_ci_high"].values
    yerr = np.vstack([b_est - b_lo, b_hi - b_est])
    plt.figure()
    plt.errorbar(xpos, b_est, yerr=yerr, fmt='o', capsize=4)
    plt.xticks(xpos, order, rotation=15)
    plt.ylabel("α_est (slope)")
    plt.title("Technique Coupling α (estimate with CI)")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "alpha_estimates.png"))
    plt.close()

    # O_* with CI
    plt.figure()
    O_est = Ostar_df.set_index("technique").loc[order, "O_star_est"].values
    O_lo = Ostar_df.set_index("technique").loc[order, "O_star_CI_low"].values
    O_hi = Ostar_df.set_index("technique").loc[order, "O_star_CI_high"].values
    yerr = np.vstack([O_est - O_lo, O_hi - O_est])
    plt.errorbar(xpos, O_est, yerr=yerr, fmt='o', capsize=4)
    plt.xticks(xpos, order, rotation=15)
    plt.ylabel("O_* (intrinsic, extrapolated)")
    plt.title("Intrinsic REST O_* by technique (after offset removal)")
    plt.tight_layout()
    plt.savefig(os.path.join(outdir, "O_star_estimates.png"))
    plt.close()

    # Ratio invariance if provided
    if ratios_path and os.path.exists(ratios_path):
        rdf = pd.read_csv(ratios_path)
        if "ratio_13_8" in rdf and "S_log_M_ratio" in rdf:
            plt.figure()
            for tname, sub in rdf.groupby("technique"):
                plt.scatter(sub["S_log_M_ratio"], sub["ratio_13_8"], s=8, label=tname)
            plt.axhline(13/8, linestyle='--')
            plt.xlabel("S")
            plt.ylabel("ratio 13:8")
            plt.title("Fibonacci ratio 13:8 vs S (invariance check)")
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(outdir, "ratio_13_8_invariance.png"))
            plt.close()

    # Write summary
    md = []
    md.append("# M-scaling Lab Run — Summary\n")
    md.append("## Per-Technique Fits (log O = a + b S)\n\n")
    md.append(fit_df.to_markdown(index=False) + "\n\n")
    md.append("## Intrinsic O_* Estimates\n\n")
    md.append(Ostar_df.to_markdown(index=False) + "\n\n")
    md.append("## Pooled Model Coefficients (first rows)\n\n")
    md.append(pooled_table.head(12).to_markdown(index=False) + "\n")
    with open(os.path.join(outdir, "RUN_SUMMARY.md"), "w") as f:
        f.write("".join(md))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--measurements", required=True, help="Path to measurements CSV")
    ap.add_argument("--ratios", default="", help="Optional path to ratios CSV")
    ap.add_argument("--dm", type=float, default=1.0, help="Scaling dimension d_M (default 1.0 for η/s)")
    ap.add_argument("--output", default="./lab_run_results", help="Output directory")
    args = ap.parse_args()
    analyze(args.measurements, args.ratios, args.dm, args.output)
