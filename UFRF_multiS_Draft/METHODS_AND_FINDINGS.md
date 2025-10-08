## METHODS AND FINDINGS — Settings and Case Notes

### Run settings
- Package: ufrf_multiS_package (current workspace)
- Commands:
  - python CODE/run_batch.py --indir DATA --sij 11 --outdir results/batch_s11
  - python CODE/run_batch.py --indir DATA --sij 21 --outdir results/batch_s21
  - python CODE/run_batch.py --indir DATA --sij 12 --outdir results/batch_s12
  - python CODE/run_batch.py --indir DATA --sij 22 --outdir results/batch_s22
- Key params: n-cycles=13, poly-deg=3, ridge=1e-3 (Tx), default RLC grid (Rx)

### Representative cases
- LQP15MN27NG02_series.s2p, S11 — UFRF +28.93%: coherent ripple; prior helps fit reactive ripple
- NFZ32BW881HN10_series.s2p, S11 — UFRF -21.10%: coherent ripple; prior helps fit reactive ripple

### Known limitations / next experiments
- Multi-port joint fitting (shared ripple params across Sij)
- Regularization sweeps and amplitude penalty tuning
- Fixture-aware modeling for strong cable/fixture resonances