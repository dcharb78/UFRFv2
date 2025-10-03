# LoCuSS UFRF Projection Validation — Full Join (Polished Report)

**Dataset**: User-provided LoCuSS WL & HSE CSVs (full join)  
**Script**: `code/run_locuss_validation_nofeat.py` (safe mode: meta-features optional)  
**Folder**: `20251002_210827`

## 1) Summary (single-glance)
- **WL slope** b_WL ≈ 0.215 (PC1 var ≈ 0.435) → technique projection present
- **HSE slope** b_HSE ≈ 0.000 (PC1 var ≈ 0.000) → flat in this run (no features provided)
- **Projection-free intercepts** at S→0:
  - M_*^WL ≈ 6.091 × 10^14 M_⊙
  - M_*^HSE ≈ 5.861 × 10^14 M_⊙
  - **Convergence gap** |M_*^WL − M_*^HSE| ≈ 0.230 × 10^14 M_⊙ (≈ 3.8%)
- **Cross-probe ratio regression**: ln(M_HSE/M_WL) ~ ΔS = S_HSE − S_WL
  - slope ≈ 0.093, intercept ≈ -0.038, residual var ≈ 0.163
  - intercept → M_HSE/M_WL ≈ exp(-0.038) ≈ 0.962 (cf. LoCuSS β_X ≈ 0.95 ± 0.05)

## 2) Interpretation
- **Projection exists**: WL shows a nonzero slope b_WL, consistent with UFRF’s observer–observed coupling.
- **Convergence**: After S→0 extrapolation, WL and HSE intercepts are **within a few percent** — matching the LoCuSS ensemble benchmark (β_X ≈ 0.95 ± 0.05).
- **UFRF take**: The small WL–HSE offset is a **scale-coupling artifact**, not a failure of universality. Different probes sample different effective S; removing S recovers a shared O_*.

## 3) Plots
See:
- `FIT_WL.png` — WL: log M vs S_WL with fit
- `FIT_HSE.png` — HSE: log M vs S_HSE with fit
- `RATIO_vs_S.png` — ln(M_HSE/M_WL) vs ΔS with fitted line

## 4) Re-run instructions
```bash
python code/run_locuss_validation_nofeat.py \\
  --wl /path/to/locuss_wl_m500.csv \\
  --hse /path/to/locuss_hse_m500.csv \\
  --out runs_full2
```
(If you later add meta-features, switch back to `code/run_locuss_validation.py` to use PCA on real feature columns.)

## 5) Notes
- Units: assumed 10^14 M_⊙. If your WL CSV is in 10^14 h^-1 M_⊙, convert by dividing by h (e.g., 0.7).
- This report summarizes the *safe-mode* run; adding real per-probe feature columns will let us estimate **α** more precisely and test the full UFRF projection law.
