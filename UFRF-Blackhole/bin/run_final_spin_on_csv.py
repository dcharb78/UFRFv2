#!/usr/bin/env python3
import sys, json
from pathlib import Path
import pandas as pd
import numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ufrf_bh.core import af_ufrf, af_baseline, rmse, aic, bic
if len(sys.argv)<2:
    print('Usage: python bin/run_final_spin_on_csv.py <csv_with_q_chi1_chi2_af>'); sys.exit(1)
csv_path = Path(sys.argv[1])
outdir = csv_path.parent.parent/'results'
outdir.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(csv_path)
pred_ufrf = af_ufrf(df['q'].values, df['chi1'].values, df['chi2'].values)
pred_base = af_baseline(df['q'].values, df['chi1'].values, df['chi2'].values)
df_out = df.copy(); df_out['af_pred_ufrf']=pred_ufrf; df_out['af_pred_baseline']=pred_base
summary = {}
af_col = 'af_true' if 'af_true' in df.columns else ('af' if 'af' in df.columns else None)
if af_col is not None:
    y = df[af_col].values
    rss_u = float(((y - pred_ufrf)**2).sum()); rss_b = float(((y - pred_base)**2).sum())
    n = len(df)
    summary = {'rmse_ufrf':float(rmse(y,pred_ufrf)),'rmse_baseline':float(rmse(y,pred_base)),
               'aic_ufrf':float(aic(n,rss_u,3)),'aic_baseline':float(aic(n,rss_b,3)),
               'bic_ufrf':float(bic(n,rss_u,3)),'bic_baseline':float(bic(n,rss_b,3))}
(outdir/'final_spin_predictions.csv').write_text(df_out.to_csv(index=False))
(outdir/'final_spin_summary.json').write_text(json.dumps(summary if summary else {'note':'no af provided'}, indent=2))
print(json.dumps(summary if summary else {'note':'no af provided'}, indent=2))
