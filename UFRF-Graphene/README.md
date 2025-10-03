# UFRF–Graphene (Coupling-First Package)
**Build:** 2025-10-01 21:25 UTC

This package isolates the graphene/2D Dirac materials portion of the UFRF work—clean, self-contained, and ready for lab validation.

## Why constants seem to "shift"
Different measurement techniques couple differently to the system. We model this with **M-scaling**:
\[ O_{meas} = O_* \left(\tfrac{M_1}{M_0}\right)^{d_M \alpha} \times \text{(disorder)}. \]
- **α**: coupling between observer scale \(M_0\) and system scale \(M_1\).
- **d_M**: scaling dimension for the observable (for η/s, start with \(d_M\approx +1\)).
- Technique disagreements become predictable slopes in \(\log O\) vs \(S \approx \log(M_1/M_0)\).

## Predictions to test
- **REST (intrinsic) η/s** tends toward **\((1/4\pi)\sqrt{\varphi} \approx 0.101\)** as \(\alpha\to 0\) (clean, decoupled limit).
- The oft-reported **“factor of 4”** decomposes into **M-shift × disorder × 2D projection** (see docs).
- **Fibonacci ratio invariance** (e.g., 13:8) in conductance spectra remains stable under M-scaling.
- A subtle thermal/transport feature near **28 K** may appear in clean devices.

## How to run your data
```bash
python code/graphene_m_scaling_lab_template.py   --measurements your_measurements.csv   --ratios your_fibonacci_ratios.csv   --dm 1.0   --output ./lab_results
```
- See `docs/DATA_SCHEMA.md` for CSV columns.
- The script outputs α estimates (with CIs), intrinsic \(O_*\) per technique (with CIs), and diagnostic plots.

## What's included
- **docs/**: THEORY_AXIOMS, protocol, M-scaling addendum, data schema, summary, changelog, call for data.
- **code/**: lightweight analysis script + sample CSVs + requirements.
- **results/plots/**: α recovery, \(O_*\) recovery, and ratio invariance figures from a full test run.

## License
Creative Commons Attribution–NonCommercial 4.0 International (**CC BY-NC 4.0**). See `LICENSE`.
