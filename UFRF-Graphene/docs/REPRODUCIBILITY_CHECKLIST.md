# REPRODUCIBILITY CHECKLIST

- [ ] Provide raw CSVs following `docs/DATA_SCHEMA.md` (technique, device, S, O_meas, optional knobs).
- [ ] Include independent repeats for each technique and at least two devices.
- [ ] Sweep **multiple knobs** to construct S; avoid perfect collinearity.
- [ ] Run the lab script and archive `per_technique_fits.csv`, `O_star_estimates.csv`, and plots.
- [ ] Report 95% CIs; consider bootstrap resampling.
- [ ] Provide a short methods note on how S was constructed (weights or PCA).

**Acceptance targets:**
- α estimates are stable across knobs (within CI).
- O_* estimates converge across techniques and trend to ~0.101 for η/s after α-correction.
- Fibonacci ratios remain stable within uncertainty vs S.
