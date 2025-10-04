# UFRF vs Standard 2D Navier–Stokes (Minimal Testbed)

This package provides a reproducible 2D incompressible Navier–Stokes testbed on a periodic square, comparing:
- Standard pseudo-spectral integration, and
- UFRF-inspired 13-wedge angular filtering of the nonlinear term (with optional half-offset wedges), plus UFRF-aligned forcing and REST projection stabilization.

Outputs include vorticity snapshots, energy/enstrophy spectra, and JSON/CSV metrics.

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Quick Run
```bash
# Minimal comparison (random init)
python3 ufrf_ns_min.py --grid 128 --steps 800 --dt 5e-3 --eta_over_s_proj 1e-3 --seed 1717 --wedge-halfwidth 6 --wedge-half --outdir results
```
Artifacts in `results/`:
- `snapshot_vorticity_standard_random.png`, `snapshot_vorticity_ufrf13_random.png`
- `spectrum_compare_random.png`
- `enstrophy_spectrum_standard_random.png`, `enstrophy_spectrum_ufrf_random.png`

## Full Suite (recommended)
```bash
./make_results.sh
```
Generates outputs in:
- `results/`, `results_sweep/`, `results_grid/`, `results_inviscid/`, `results_tg/`, `results_forced/`

## Additional Commands
- Halfwidth sweep:
  ```bash
  python3 sweep_halfwidth.py
  ```
- Grid sweep:
  ```bash
  python3 sweep_grid.py
  ```
- Inviscid conservation check:
  ```bash
  python3 check_inviscid.py
  ```
- Taylor–Green validation:
  ```bash
  python3 check_taylor_green.py
  ```
- Forced turbulence (Kolmogorov vs UFRF wedge forcing):
  ```bash
  python3 run_forced_turbulence.py
  ```

## 3D Quick Start
- 3D Taylor–Green + forced runs:
  ```bash
  python3 run_3d_tests.py
  ```
Artifacts in `results3d/` include `tg_timeseries.csv`, `tg_spectrum.png`, and summaries.

## Boundary Flow Quick Start (2D)
```bash
python3 run_boundary_tests.py
```
Artifacts in `results_boundary/`: `cavity_speed.png`, `cavity_summary.json`, `channel_centerline.png`, `channel_summary.json`.

## Repository Structure
- `docs/` — theory and planning documents:
  - `StartSummary.md`, `ufrf-nse-proof.md`, `ResultsLetter.md`, `BenchmarkComparison.md`, `development_plan.md`
- Root — code and runners:
  - 2D: `ufrf_ns_min.py`, `run_full_tests.py`, `run_ablation.py`
  - 3D: `ufrf_ns3d.py`, `run_3d_tests.py`
  - Boundary: `cavity2d.py`, `channel2d.py`, `run_boundary_tests.py`
  - Automation: `make_results.sh`, `update_benchmarks.py`
- Outputs: `results/`, `results_forced/`, `results_sweep/`, `results_grid/`, `results_inviscid/`, `results3d/`, `results_boundary/`

## UFRF References
This repository is designed to live within the consolidated UFRF repo. Cite and reference theory from the root docs in that repo, e.g. `ufrf-core-theory-corrected.md`, `ufrf-mathematical-framework.md`, `UFRF.Prime.md`, and others available here:
- UFRF consolidated repository: `https://github.com/dcharb78/UFRFv2`

## License and Citation
- License: CC BY-NC 4.0 (see `CITATION.cff` for citation info).