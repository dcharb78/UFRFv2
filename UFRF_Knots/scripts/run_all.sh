#!/usr/bin/env bash
set -euo pipefail

MODE=${1:-phase}
FEAT=${2:-multiscale}
GEOM=${3:-pd}
KNOTS=${4:-data/real_knots.csv}
COMPS=${5:-data/real_composites.csv}
OUT=${6:-results/real_pd_ms}

python scripts/run_joint_pipeline.py --mode "$MODE" --feature_mode "$FEAT" --geometry_mode "$GEOM" --knots "$KNOTS" --composites "$COMPS" --out "$OUT"

python scripts/analyze_subadditivity.py --results "$OUT/phase_results.json" --out "${OUT}_plots"
