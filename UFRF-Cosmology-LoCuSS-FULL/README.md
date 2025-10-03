# UFRF-Cosmology-LoCuSS-FULL (Standalone)

This package is a **complete, full-fidelity** validation of the UFRF projection law on the LoCuSS cluster sample.
It ships with **your actual WL + HSE CSVs**, the **code**, and the **real run outputs** (no placeholders).

## Quick Start
```bash
# Safe-mode (uses your CSVs exactly as provided; no meta-feature PCA)
python code/run_locuss_validation_nofeat.py       --wl data/locuss_wl_m500.csv       --hse data/locuss_hse_m500.csv       --out runs_full

# Featureful (if you later add real meta-features to the CSVs)
python code/run_locuss_validation.py       --wl data/locuss_wl_m500.csv       --hse data/locuss_hse_m500.csv       --out runs
```

## What to look for
- **Per-probe slopes** (b ≈ d_M·α). In your current CSVs, WL shows b≠0; HSE is ~0 because no HSE meta-features were provided.
- **Projection-free intercepts** M_*^{WL}, M_*^{HSE} close to each other.
- **ln(M_HSE/M_WL)** intercept near **-0.04** ⇒ ratio ≈ **0.96**, matching LoCuSS β_X ≈ 0.95 ± 0.05.

## Contents
- `code/` — scripts (safe-mode and featureful)
- `data/` — your WL & HSE CSVs (units: 1e14 M_sun; WL should be pre-converted from h^-1 units)
- `runs_full/` — **real outputs** from a full-join validation
- `docs/` — usage notes and references
- `theory/` — UFRF projection law, axioms, derivation of β_X intercept

