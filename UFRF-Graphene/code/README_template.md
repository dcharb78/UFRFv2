# Graphene M-Scaling Lab Template
**Updated:** 2025-10-01 21:11 UTC

This template analyzes technique-dependent measurements using the M-scaling framework:
\[ O_{meas} = O_* \left(\tfrac{M_1}{M_0}\right)^{d_M\,\alpha} \times \text{(disorder)}. \]

It estimates:
- **α (technique coupling)** from the slope of \(\log O\) vs S (a surrogate for \(\log(M_1/M_0)\)).
- **O\_*** (intrinsic REST value) by removing technique/device offsets and extrapolating toward α→0.
- Confidence intervals for all fitted parameters.

## Input CSV Schema

### 1. Measurements CSV (`your_measurements.csv`)
Columns (header required):
- `technique` (string; e.g., NonlocalHydro, THzOptical, ARPES)
- `device` (string ID; e.g., dev1, dev2 …)
- `S_log_M_ratio` (float; surrogate for log(M1/M0), built from knobs such as dielectric, invasiveness, density, current)
- `O_meas` (float; measured observable, e.g., η/s)
- Optional knobs (for diagnostics): `dielectric`, `invasiveness`, `density`, `current`

### 2. (Optional) Ratios CSV (`your_fibonacci_ratios.csv`)
Columns:
- `technique`, `device`, `S_log_M_ratio`
- `ratio_8_5`, `ratio_13_8`, `ratio_21_13`, `ratio_34_21`

## Quickstart

```bash
python graphene_m_scaling_lab_template.py   --measurements your_measurements.csv   --ratios your_fibonacci_ratios.csv   --dm 1.0   --output ./lab_run_results
```

This produces:
- Per-technique fits with 95% CIs
- Pooled fixed-effects model (technique + device)
- O_* estimates with CIs
- Plots: α recovery, O_* recovery, and ratio invariance diagnostics
- A `RUN_SUMMARY.md` with all key tables

## Notes
- If you don’t have ratios, omit `--ratios` and ratio plots will be skipped.
- Start with `d_M=1.0` for η/s; for other observables (e.g., α_eff) use an appropriate sign/magnitude.
- Ensure techniques have meaningful S variation; otherwise slope/α cannot be identified.
