# UFRF Knot Subadditivity — Publish Package (v2, full)

This archive contains the **full manuscript** and figures generated from your uploaded `phase_results.json`.

## Contents
- `docs/UFRF_Knot_Subadditivity_v2.md` — complete paper (v2)
- `figures/delta_hist.png` — histogram of Δu
- `figures/delta_vs_cosine.png` — Δu vs cosine scatter
- `results/phase_results.json` — copy of your results
- (optional) `results/composite_metrics.csv` — included if you uploaded it
- (optional) `results/observer_run_summaries.csv` — add to make stability plot
- (optional) `results/permutation_summary.json` — add to make permutation plot
- `environment.yml`
- `CITATION.cff`

## How to regenerate (step-by-step)

1) **Create a conda env**
```bash
conda env create -f environment.yml
conda activate ufrf-knots
```

2) **Generate core figures (already included)**
```python
import json, pandas as pd, matplotlib.pyplot as plt
data = json.load(open("results/phase_results.json"))
df = pd.DataFrame(data["composites"])

# Δu histogram
plt.figure(figsize=(7,5))
plt.hist(df["delta"].dropna(), bins=50, edgecolor="black")
plt.xlabel("Δu"); plt.ylabel("Count"); plt.title("Histogram of Δu"); plt.tight_layout()
plt.savefig("figures/delta_hist.png"); plt.close()

# Δu vs cosine
plt.figure(figsize=(7,5))
plt.scatter(df["cosine"], df["delta"], s=8, alpha=0.5)
plt.axhline(0, linewidth=1)
plt.xlabel("cosine(phase)"); plt.ylabel("Δu"); plt.title("Δu vs cosine"); plt.tight_layout()
plt.savefig("figures/delta_vs_cosine.png"); plt.close()
```

3) **(Optional) Add stability plot**
- Place your `observer_run_summaries.csv` into `results/`.
```python
import pandas as pd, matplotlib.pyplot as plt
s = pd.read_csv("results/observer_run_summaries.csv")
plt.figure(figsize=(8,4))
plt.bar(range(len(s)), s["frac_subadd"])
plt.xlabel("Run index"); plt.ylabel("Fraction Δu < 0"); plt.title("Observer stability")
plt.tight_layout(); plt.savefig("figures/stability_bar.png"); plt.close()
```

4) **(Optional) Add permutation null plot**
- Place your `permutation_summary.json` into `results/`.
```python
import json, matplotlib.pyplot as plt
perm = json.load(open("results/permutation_summary.json"))
obs = perm["observed_fraction"]; nulls = perm["null_fractions"]
plt.figure(figsize=(7,5))
plt.hist(nulls, bins=40, edgecolor="black")
plt.axvline(obs, linewidth=2)
plt.xlabel("Null fraction Δu < 0"); plt.ylabel("Count"); plt.title("Pairing-permutation null vs observed")
plt.tight_layout(); plt.savefig("figures/permutation_null.png"); plt.close()
```

## Notes / Guarantees
- No synthetic diagrams were generated.
- All figures use matplotlib (no seaborn) and no custom color themes.
- The paper links figures by relative paths so it renders correctly in GitHub or JupyterBook.

