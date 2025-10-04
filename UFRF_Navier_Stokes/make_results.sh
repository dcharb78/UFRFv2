#!/bin/bash
set -euo pipefail

# Run core suites
python3 run_full_tests.py

# Sweeps and checks
python3 sweep_halfwidth.py
python3 sweep_grid.py || true
python3 check_inviscid.py
python3 check_taylor_green.py
python3 run_forced_turbulence.py

# 3D suite
python3 run_3d_tests.py

# Boundary flows
python3 run_boundary_tests.py

echo "All runs completed. See results/*, results_sweep/*, results_grid/*, results_inviscid/*, results_tg/*, results_forced/*"
