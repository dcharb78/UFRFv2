import numpy as np
import pandas as pd

def permutation_test_subadditivity(df: pd.DataFrame, n_perm: int = 2000, seed: int = 144000) -> float:
    """
    Break pairing by permuting right_id; recompute delta under random re-pairings
    using group-level summary statistics (approximation).
    Return p-value = Pr(null >= observed subadditivity fraction).
    """
    rng = np.random.default_rng(seed)
    obs_frac = (df["delta"] < 0).mean()

    # Approximate null by shuffling 'delta' signs relative to (cosine, overlap)
    signs = (df["delta"] < 0).astype(int).values.copy()
    cnt = 0
    for _ in range(n_perm):
        rng.shuffle(signs)
        frac = signs.mean()
        if frac >= obs_frac:
            cnt += 1
    p = (cnt + 1) / (n_perm + 1)
    return float(p)

def simple_regression_delta(df: pd.DataFrame):
    """
    Δu = b0 + b1*cosine + b2*overlap + eps
    Returns coefficients, std errs, t-stats (OLS closed form).
    """
    x1 = df["cosine"].values.astype(float)
    x2 = df["oppose_overlap"].values.astype(float)
    y  = df["delta"].values.astype(float)
    X  = np.column_stack([np.ones_like(x1), x1, x2])
    # OLS
    beta = np.linalg.pinv(X) @ y
    yhat = X @ beta
    resid = y - yhat
    n, k = X.shape
    sigma2 = (resid @ resid) / (n - k)
    cov = sigma2 * np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    tstats = beta / se
    return {
        "coeffs": beta.tolist(),
        "stderr": se.tolist(),
        "tstats": tstats.tolist(),
        "n": int(n)
    }

def stability_check(df_list):
    """
    Given a list of composite DataFrames from re-diagramming runs,
    compute mean/median Δu and subadditivity fraction stability.
    """
    fracs = [ (df["delta"] < 0).mean() for df in df_list ]
    means = [ df["delta"].mean() for df in df_list ]
    meds  = [ df["delta"].median() for df in df_list ]
    return {
        "frac_mean": float(np.mean(fracs)),
        "frac_std":  float(np.std(fracs)),
        "mean_mean": float(np.mean(means)),
        "mean_std":  float(np.std(means)),
        "med_mean":  float(np.mean(meds)),
        "med_std":   float(np.std(meds)),
        "runs": len(df_list)
    }
