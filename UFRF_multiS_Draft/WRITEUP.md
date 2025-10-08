# Initial Results Template (fill after you run)

Paste key numbers from `report.md` and `metrics.csv` here.

- File: ...
- Sij: ...
- Split: random / interleave
- Baseline test MSE (complex): ...
- UFRF test MSE (complex): ...
- Improvement: ... %
- Notes: (coherent ripple present? any over‑smooth?)

Repeat for multiple files and summarize the average improvement.

## Batch Highlights (real vendor data)

- Top S11 improvements observed (held-out test MSE reductions):
  - ~28.55%: `LQP15MN27NG02_series.s2p`
  - ~27.02%: `LQP15MN22NG02_series.s2p`
  - ~25.22%: `LQP15MN18NG02_series.s2p`
  - ~24.64%: `LQG15HH18NH02_series.s2p` / `LQG15HH18NJ02_series.s2p` / `LQG15HH18NG02_series.s2p`
  - ~24.09%: `LQP15MN15NG02_series.s2p`
  - ~23.10%: `LQG15HH15NH02_series.s2p`

See `results/batch_s11_*/*/report.md` for per-device plots and details, and `leaderboard.csv` under each batch folder for sortable metrics. Extend similarly for S21 results as needed.
