
import pandas as pd
from pathlib import Path

TECH_MAP = {
    "hse": {"file": "locuss_hse_m500.csv", "m_col": "m500_hse", "e_col": "m500_hse_err"},
    "sz":  {"file": "locuss_sz_m500.csv",  "m_col": "m500_sz",  "e_col": "m500_sz_err"},
    "wl":  {"file": "locuss_wl_m500.csv",  "m_col": "m500_wl",  "e_col": "m500_wl_err"},
}

def load_locuss(data_dir: str = "data") -> pd.DataFrame:
    """
    Return a tidy (long-form) DataFrame with unified columns:
      cluster_id | z | technique | m500 | m500_err
    The function expects the three LoCuSS CSVs to be present in `data_dir` under their default names.
    """
    data_dir = Path(data_dir)
    frames = []
    for tech, meta in TECH_MAP.items():
        fp = data_dir / meta["file"]
        df = pd.read_csv(fp)
        df.columns = [c.strip().lower() for c in df.columns]
        cols = ["cluster_id", "z", meta["m_col"], meta["e_col"]]
        df = df[cols].copy()
        df = df.rename(columns={meta["m_col"]: "m500", meta["e_col"]: "m500_err"})
        df["technique"] = tech.upper()
        frames.append(df)
    long_df = pd.concat(frames, ignore_index=True, sort=False)
    # ensure dtypes
    long_df["cluster_id"] = long_df["cluster_id"].astype(str)
    long_df["technique"] = long_df["technique"].astype("category")
    return long_df

def pivot_locuss(long_df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert the long-form DataFrame into one row per cluster with columns:
      m500_HSE, m500_HSE_err, m500_SZ, m500_SZ_err, m500_WL, m500_WL_err
    """
    # pivot values and errors separately, then merge
    v = long_df.pivot_table(index=["cluster_id","z"], columns="technique", values="m500")
    e = long_df.pivot_table(index=["cluster_id","z"], columns="technique", values="m500_err")
    v.columns = [f"m500_{t.lower()}" for t in v.columns]
    e.columns = [f"m500_{t.lower()}_err" for t in e.columns]
    merged = pd.concat([v, e], axis=1).reset_index()
    return merged

# Example α dictionary; tune as needed
ALPHA = {"WL": 0.3, "SZ": 0.5, "HSE": 0.7}

def fit_S_from_pairs(pivot_df: pd.DataFrame, t1: str, t2: str, alpha: dict = ALPHA) -> float:
    import numpy as np
    r = np.log(pivot_df[f"m500_{t1.lower()}"] / pivot_df[f"m500_{t2.lower()}"])
    d = alpha[t1] - alpha[t2]
    return float(np.nanmedian(r) / d)

def estimate_intrinsic_mass(row, alpha: dict, S: float, using=("WL","SZ")) -> float:
    """
    Estimate intrinsic log mass log(M*) from two techniques using inverse-variance weighting in log space.
    Returns log(M*). Use exp(logM* + alpha[target]*S) to predict a target technique.
    """
    import numpy as np
    logs, weights = [], []
    for t in using:
        m = row[f"m500_{t.lower()}"]
        e = row.get(f"m500_{t.lower()}_err", None)
        if pd.isna(m) or m <= 0: 
            continue
        log_m = np.log(m) - alpha[t] * S
        w = 1.0 / ((e / m)**2) if (e is not None and e>0) else 1.0
        logs.append(log_m); weights.append(w)
    if not logs:
        return float('nan')
    return float(np.average(logs, weights=weights))
