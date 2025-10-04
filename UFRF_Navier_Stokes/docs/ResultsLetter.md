## UFRF–Projected Navier–Stokes: Results and Replication Guide

### Summary
We present a reproducible UFRF-aligned Navier–Stokes suite demonstrating:
- 2D periodic: random decay, shear, forced turbulence with UFRF wedge filtering/forcing and REST projection stabilization.
- 3D periodic: Taylor–Green decay and low-Re forced runs with budgets and energy spectra.
- Boundary flows: 2D lid-driven cavity and channel/Poiseuille.

All runs include energy budgets (E, ε, dE/dt, P_in, residual) and diagnostics (spectra, flux Π(k), shell transfers). REST is formalized as a projection operator that preserves incompressibility and commutes with vorticity–streamfunction.

### Key Findings (current artifact)
- Energy budgets close (small residuals) across standard and UFRF runs.
- UFRF wedge/shell forcing injects energy in a controlled, theory-consistent manner.
- 3D Taylor–Green decays smoothly; spectra logged with preliminary slope fits.
- Boundary-driven flows run stably with qualitative fields, indicating generality beyond periodic boxes.

### Replication Steps
1) Install
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
2) Full 2D suite
```bash
./make_results.sh
```
3) 3D suite
```bash
python3 run_3d_tests.py
```
4) Boundary flows
```bash
python3 run_boundary_tests.py
```
5) Update benchmark summary
```bash
python3 update_benchmarks.py
```

### Artifacts of Interest
- 2D: `results/`, `results_forced/`, `results_sweep/`, `results_grid/`
- 3D: `results3d/` (e.g., `tg_timeseries.csv`, `tg_spectrum.png`, `tg_summary.json`)
- Boundary: `results_boundary/` (e.g., `cavity_speed.png`, `channel_centerline.png`)
- Proof: `ufrf-nse-proof.md` (mapping, REST operator, appendix, 3D and boundary sections)
- Benchmarks: `BenchmarkComparison.md` (targets and current metrics)

### Scope & Limitations
This is a computational evidence suite aligned with UFRF, not a formal existence/smoothness proof. For broader acceptance, we plan to upscale 3D runs, add literature comparisons, and extend boundary validations.

### Citation
Please cite `CITATION.cff` and the consolidated UFRF repository.
