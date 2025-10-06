#!/usr/bin/env bash
set -euo pipefail

MODE=${1:-phase}
KNOTS=${2:-data/sample_knots.csv}
COMPS=${3:-data/sample_composites.csv}
OUT=${4:-results/run_$(date +%Y%m%d_%H%M%S)}

python scripts/run_joint_pipeline.py --mode "$MODE" --knots "$KNOTS" --composites "$COMPS" --out "$OUT"

python scripts/analyze_subadditivity.py --results "$OUT/phase_results.json" --out "${OUT}_plots"
