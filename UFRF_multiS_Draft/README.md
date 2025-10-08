# UFRF Predictive-Prior Package (Multi‑S Parameters)

A complete, **turn‑key** package to test a **UFRF-inspired prior** on **any S‑parameter** trace:
- Reflections (**S11, S22**): also shows Smith‑chart overlays.
- Transmission/Isolation (**S21, S12**): complex‑plane overlays and |S| in dB.

**Goal:** show whether a small, coherent, log‑periodic ripple prior (≈13 cycles across your log‑frequency span)
yields **lower held‑out error** on complex S‑parameters than standard smooth baselines.

## Quickstart

```bash
unzip ufrf_multiS_package.zip && cd ufrf_multiS_package
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1) Demo on synthetic (creates TESTS/demo_twoport.s2p)
python CODE/run_prior_test.py --input TESTS/demo_twoport.s2p --sij 11 --outdir results/demo_s11
python CODE/run_prior_test.py --input TESTS/demo_twoport.s2p --sij 21 --outdir results/demo_s21

# 2) Your files (Touchstone .s1p/.s2p)
python CODE/run_prior_test.py --input path/to/your.s2p --sij 21 --outdir results/your_s21

# 3) Batch a folder (runs all .snp in DATA/ for chosen Sij)
python CODE/run_batch.py --indir DATA --sij 11 --outdir results/batch_s11
python CODE/run_batch.py --indir DATA --sij 21 --outdir results/batch_s21

# (Optional) Turn UFRF prior OFF to see baseline only
python CODE/run_prior_test.py --input path/to/file.s2p --sij 21 --prior off --outdir results/baseline_only
```

Artifacts in each `--outdir`:
- `report.md` — human‑readable summary, params, and metrics
- `metrics.csv` — train/test complex‑Γ (or complex Sij) MSE
- `*_overlay.png` — plots (Smith for S11/S22; complex + |S|dB for S21/S12)
- `params.json` — all fit details

## What’s inside
- `CODE/` — Python modules (no SciPy; just numpy/pandas/matplotlib)
- `TESTS/` — scripts to generate synthetic `.s1p` and `.s2p` demos
- `DATA/` — put your downloaded datasets here
- `TEMPLATES/` — optional CSV template; not required if you use Touchstone

See **DATASETS.md** for **10–50+** public sources and tips to grab example files fast.
