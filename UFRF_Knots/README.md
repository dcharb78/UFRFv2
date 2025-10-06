# UFRF–Knots: Phase-Projection Analysis of Unknotting Subadditivity

This package provides a **reproducible pipeline** to analyze subadditivity of an
unknotting-cost proxy in composite knots using the **UFRF 13‑phase** interference model,
with optional hooks to validate on *actual diagrams* if you have **SnapPy** installed.

## Two modes

1. **Phase-only (default, no external deps)**  
   Uses provided 13‑d phase vectors to compute:
   - single-knot cost proxy \(u(K)=\|v\|_1\),
   - composite cost with two-for-one surgeries when phases oppose,
   - statistics/plots of subadditivity \(\Delta u\).

2. **Snap mode (optional)**  
   If [SnapPy](https://snappy.computop.org/) is installed, you can:
   - parse Dowker–Thistlethwaite (DT) codes (or provide PD codes),
   - run a bounded-depth crossing-change search,
   - confirm unknot recognition via SnapPy (fallbacks included).

> **Note:** The included data are small *examples*. Replace with your own datasets
  (DT/PD codes, or your measured phase features) to stress-test our predictions
  (phase anti-alignment ⇒ subadditivity; overlap ⇒ larger deficits).

## Quickstart (Phase-only)

```bash
pip install -r requirements.txt
python scripts/run_joint_pipeline.py --mode phase --knots data/sample_knots.csv --composites data/sample_composites.csv --out results/phase_run
python scripts/analyze_subadditivity.py --results results/phase_run/phase_results.json --out results/phase_plots
```

Outputs:
- `results/phase_run/phase_results.json` (per-knot costs, per-composite Δu)
- `results/phase_plots/plot_delta_hist.png`
- `results/phase_plots/plot_delta_vs_cosine.png`
- `results/phase_plots/plot_delta_vs_overlap.png`

## Optional: Snap mode

Ensure SnapPy is installed (system dependent). Then:

```bash
python scripts/run_joint_pipeline.py --mode snap --knots data/sample_knots.csv --composites data/sample_composites.csv --out results/snap_run --max_depth 2
```

This will:
- attempt small-depth crossing-change searches on DT codes,
- use SnapPy (if available) to test for the unknot after each sequence,
- write a summary (note: this is a *bounded* search; it’s a demo, not a proof engine).

## Data formats

**Knots CSV** (`data/sample_knots.csv`):
```
knot_id,dt_code,phase_vector
K_2_7,"", "[-1,0,2,0,0,1,0,0,0,-1,0,0,1]"
K_2_7_mirror,"", "[1,0,-2,0,0,-1,0,0,0,1,0,0,-1]"
K_3_5,"", "[0,1,0,0,2,0,0,-1,0,0,0,1,0]"
U,"", "[0,0,0,0,0,0,0,0,0,0,0,0,0]"
```
- `dt_code` may be empty for phase-only mode.
- `phase_vector` must be a JSON list of 13 integers.

**Composites CSV** (`data/sample_composites.csv`):
```
composite_id,left_id,right_id
C1,K_2_7,K_2_7_mirror
C2,K_2_7,K_3_5
C3,K_3_5,K_2_7_mirror
```

## Theory summary

- Each knot diagram yields a 13‑d **phase obstruction vector** \(v\).
- **Single cost proxy:** \(u(K)=\|v\|_1\).
- **Composite cost:** allow a “two-for-one” surgery when component phases oppose:
  \[
    u(K_1\#K_2) = \|v_1\|_1 + \|v_2\|_1
    - \sum_i \min(|v_{1i}|,|v_{2i}|)\,[\mathrm{sign}(v_{1i})\neq\mathrm{sign}(v_{2i})].
  \]
- Predictions:
  - **Subadditivity** common when phases anti-align.
  - **Deficit size** \(\Delta u\) grows with **opposed-phase overlap**.
  - **Alignment proxy:** cosine similarity of \(v_1,v_2\) (more negative ⇒ larger savings).

## License

MIT


---

## macOS (Apple Silicon) notes for SnapPy

You have two main options:

**Option A: Conda (recommended)**
```bash
# install miniconda if needed, then:
conda create -n snappy-env python=3.11 -y
conda activate snappy-env
conda install -c conda-forge snappy -y  # pulls SnapPy + deps
pip install numpy pandas matplotlib
```

**Option B: pip wheels**
```bash
python -m pip install --upgrade pip
pip install snappy  # if a native wheel is available for your OS/Python
pip install numpy pandas matplotlib
```

> If `pip install snappy` fails on Apple Silicon, prefer Option A (conda-forge).
> Verify installation inside Python:
> ```python
> import snappy; print(snappy.__version__)
> ```

---

## Real-knot workflow (checklist)

1. **Prepare data**
   - Copy `data/templates/real_knots_template.csv` → `data/real_knots.csv`
   - Fill `knot_id` and `dt_code` for each knot you want (phase_vector optional)
   - Generate composites:
     ```bash
     python scripts/make_composites.py --knots data/real_knots.csv --out data/real_composites.csv --pairs all
     ```

2. **Run (phase-only first)**
   ```bash
   ./scripts/run_real_knots.sh phase data/real_knots.csv data/real_composites.csv results/real_phase
   ```

3. **Run with SnapPy (verification)**
   ```bash
   ./scripts/run_real_knots.sh snap data/real_knots.csv data/real_composites.csv results/real_snap
   ```

4. **Review**
   - `*_plots/plot_delta_hist.png` (how often composites are subadditive)
   - `*_plots/plot_delta_vs_cosine.png` (anti-alignment ⇒ larger saving)
   - `*_plots/plot_delta_vs_overlap.png` (overlap ⇒ larger saving)
   - `*_plots/composite_metrics.csv` (per-composite table)

5. **Share / reproduce**
   - Commit `data/real_knots.csv` and `data/real_composites.csv`
   - Share the `results/` folder or re-run with the provided commands.


---

## v0.4 — Geometry modes & What to return to me

### Geometry modes
- `--geometry_mode dt` (default): uses DT sequences (with multiscale writhe-like features).
- `--geometry_mode pd`: uses PD diagrams (preferred). If `pd_code` is missing, a **toy dt→pd** is used (replace with a real converter when available).

### EXACT COMMANDS TO RUN

**A) Phase-only, PD mode (recommended if you have PDs)**
```bash
python scripts/run_joint_pipeline.py   --mode phase   --feature_mode multiscale   --geometry_mode pd   --knots data/real_knots.csv   --composites data/real_composites.csv   --out results/real_pd_ms

python scripts/analyze_subadditivity.py   --results results/real_pd_ms/phase_results.json   --out results/real_pd_ms_plots
```

**B) Verification on your machine (SnapPy)**
```bash
python scripts/run_joint_pipeline.py   --mode snap   --feature_mode multiscale   --geometry_mode pd   --knots data/real_knots.csv   --composites data/real_composites.csv   --out results/real_pd_snap --max_depth 2
```

### WHAT TO RETURN (copy/paste these blocks)

When any script finishes, it prints a block like:

```
===== UFRF_KNOTS_RETURN_BLOCK =====
results_json: results/real_pd_ms/phase_results.json
plots_dir: results/real_pd_ms_plots
top_metrics_csv: results/real_pd_ms_plots/composite_metrics.csv
summary:
  N_composites: <int>
  fraction_subadditive: <float>
  mean_delta: <float>
  median_delta: <float>
  min_delta: <int>
  max_delta: <int>
===================================
```

Please paste that entire block back to me. If you ran SnapPy mode, also send:
`results/real_pd_snap/phase_results.json` (it will include verification fields).


---

## v0.5 — Rigorous analyses: permutation, regression, re-diagramming, real verifier

### Quick path (phase-only, PD mode)
```bash
./scripts/run_all.sh phase multiscale pd data/real_knots.csv data/real_composites.csv results/real_pd_ms
```

### Permutation test + regression are printed at the end of analyze_subadditivity.py output.

### Re-diagramming robustness (10 runs)
```bash
python scripts/re_diagramming.py --knots data/real_knots.csv --composites data/real_composites.csv --out results/real_pd_ms/rediag_runs --runs 10
python scripts/analyze_subadditivity.py --results results/real_pd_ms/phase_results.json --out results/real_pd_ms_plots
```

If `results/real_pd_ms/rediag_runs/rediag_*.csv` exist, the stability summary will be printed.

### SnapPy verification (bounded BFS)
```bash
# Requires: conda install -c conda-forge snappy spherogram
python scripts/run_joint_pipeline.py --mode snap --feature_mode multiscale --geometry_mode pd \
  --knots data/real_knots.csv --composites data/real_composites.csv --out results/real_pd_snap --max_depth 2

python scripts/analyze_subadditivity.py --results results/real_pd_snap/phase_results.json --out results/real_pd_snap_plots
```

Return the printed **UFRF_KNOTS_RETURN_BLOCK** and the extra stats section.
