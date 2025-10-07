#!/usr/bin/env python3
import sys, json
from pathlib import Path
import pandas as pd
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ufrf_bh.core import PHI, phi_ladder, nearest_phi_distance, enrichment_test
if len(sys.argv)<2:
    print('Usage: python bin/run_phi_on_csv.py <csv_with_q>'); sys.exit(1)
csv_path = Path(sys.argv[1])
df = pd.read_csv(csv_path)
ladder = phi_ladder(20)
dists, nearest = nearest_phi_distance(df['q'].values, ladder)
df['nearest_ratio'] = nearest
df['dist_to_nearest'] = dists
df['dist_to_phi_inv'] = (df['q'] - 1/PHI).abs()
summary = enrichment_test(df['q'].values, delta=0.05, ladder=ladder)
outdir = csv_path.parent.parent/'results'
outdir.mkdir(parents=True, exist_ok=True)
(outdir/'phi_analysis_from_csv.csv').write_text(df.to_csv(index=False))
(outdir/'phi_analysis_summary.json').write_text(json.dumps({'phi_enrichment':summary,'phi_inv':float(1/PHI)}, indent=2))
print(json.dumps({'phi_enrichment':summary,'phi_inv':float(1/PHI)}, indent=2))
