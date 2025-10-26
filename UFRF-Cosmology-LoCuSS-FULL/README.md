# UFRF-Cosmology-LoCuSS-FULL (Complete Package with WL, HSE, and SZ)

This package provides a **complete, full-fidelity** validation of the UFRF projection law on the LoCuSS cluster sample.
It now includes **all three mass probes**: Weak Lensing (WL), Hydrostatic Equilibrium (HSE), and Sunyaev-Zel'dovich (SZ) measurements.

## Quick Start

```bash
# Full three-probe analysis (WL + HSE + SZ)
python code/run_locuss_validation_full.py \
  --wl data/locuss_wl_m500.csv \
  --hse data/locuss_hse_m500.csv \
  --sz data/locuss_sz_m500.csv \
  --out runs_full_three_probe

# Two-probe analysis (WL + HSE only)
python code/run_locuss_validation.py \
  --wl data/locuss_wl_m500.csv \
  --hse data/locuss_hse_m500.csv \
  --out runs_two_probe
```

## What to Look For

### Three-Probe Convergence
- **Technique-dependent slopes** (b ≈ d_M·α): Each probe shows different projection coupling
- **Projection-free intercepts** M_*^{WL}, M_*^{HSE}, M_*^{SZ} converge at S→0
- **Cross-probe ratios**: 
  - ln(M_HSE/M_WL) ≈ -0.04 → ratio ≈ 0.96 (matches LoCuSS β_X ≈ 0.95 ± 0.05)
  - ln(M_SZ/M_WL) and ln(M_SZ/M_HSE) provide additional calibration

### UFRF Validation
The convergence of all three independent mass measurements to consistent M* values after S→0 extrapolation validates the UFRF projection law across different observational techniques.

## Contents

### Data Files
- `data/locuss_wl_m500.csv` — Weak lensing masses (50 clusters, units: 10^14 M_sun)
  - Includes: M500_WL, errors, PSF/size ratio, SNR, photoz width
- `data/locuss_hse_m500.csv` — Hydrostatic X-ray masses (50 clusters, units: 10^14 M_sun)
  - Based on Chandra/XMM observations
- `data/locuss_sz_m500.csv` — SZ masses (50 clusters, units: 10^14 M_sun)
  - Includes: M500_SZ, errors, Y500 integrated Compton parameter, survey source

### Analysis Code
- `code/run_locuss_validation_full.py` — Complete three-probe analysis with visualization
- `code/run_locuss_validation.py` — Two-probe (WL+HSE) analysis
- `code/run_locuss_validation_nofeat.py` — Safe-mode without feature extraction

### Documentation
- `theory/` — UFRF projection law, axioms, mathematical framework
- `docs/` — References to original LoCuSS publications
- `runs_full/` — Example outputs from validation runs

