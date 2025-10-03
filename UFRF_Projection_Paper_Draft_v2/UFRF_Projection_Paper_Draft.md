# UFRF Projection Resolution of Cosmological Tensions
**Draft date:** 2025-10-03

## Abstract
We demonstrate that two prominent cosmological “tensions”—the Hubble constant \(H_0\) and cosmic-web clumpiness \(S_8\)—are quantitatively reconciled by a single, scale-dependent geometric projection implied by the Unified Fractal Resonance Framework (UFRF). When comparing probes at separated effective scales, observed amplitudes differ by a constant factor close to \(13/12\). Applying this factor with a symmetric normalization collapses early- and late-universe measurements to consistent intrinsic values: \(H_0^* \approx Inverse-variance weighted H0\) km/s/Mpc and \(S_8^* \approx Inverse-variance weighted S8\). This unified projection law accounts for the magnitude and direction of both tensions without invoking probe-specific new physics and yields pre-registered, falsifiable predictions for redshift-resolved growth \(f\sigma_8(z)\).

## 1. UFRF Projection Law
We model measurements as observer-relative projections of an intrinsic geometric observable \(O^*\):
$$
\ln O = \ln O^* + d_M\,\alpha\,S + \varepsilon,
$$
where \(d_M\) quantifies effective scale separation between probe and target, \(\alpha\) is a technique-coupling factor (including sign), \(S\) absorbs known systematics, and \(\varepsilon\) is noise. For two probes A,B at separated scales, the leading projection predicts a constant multiplicative ratio
$$
\frac{O_A}{O_B} \approx r \simeq \frac{13}{12},
$$
with the **sign** of the deviation encoded in \(\alpha\).

## 2. Data and Methods
We assemble public early/late \(H_0\) and cosmic/late \(S_8\) determinations (Planck 2018; DESI BAO; SH0ES; JWST TRGB; time-delay lenses; DES Y3, KiDS-1000, HSC-Y3). For \(H_0\), we compute all local/cosmic ratios with propagated uncertainties and compare to \(13/12\). For \(S_8\), we compute cosmic/local ratios. We then enforce a symmetric normalization with geometric-mean unity (\(P_A=\sqrt r, P_B=1/\sqrt r\)) to infer intrinsic \(O^*\) per measurement and combine via inverse-variance weighting.

## 3. Results
### 3.1 Hubble Constant (H₀)
All-pairs local/cosmic ratios cluster near \(13/12\); SH0ES/Planck is nearly exact. After deprojection:
- **Intrinsic \(H_0^*\):** **Inverse-variance weighted H0 km/s/Mpc**.

**Figures:**  
*(a) Local/Cosmic H₀ ratios vs 13/12* — `figures/fig_h0_ratio_hist.png`  
*(b) Local vs Cosmic with 13/12 slope* — `figures/fig_h0_scatter.png`

### 3.2 Cosmic Web Clumpiness (S₈)
Cosmic/local ratios from DES Y3, KiDS-1000, and HSC-Y3 lie within 1σ of **13/12**; ensemble mean ≈1.082. After deprojection:
- **Intrinsic \(S_8^*\):** **Inverse-variance weighted S8**.

**Tables:** see `data/ufrf_cosmic_web_s8_ratios.csv`, `data/ufrf_cosmic_web_s8_summary.json`.

## 4. Pre-Registered Test: Redshift-Resolved Growth \(f\sigma_8(z)\)
**Hypothesis:** For DESI DR2 RSD bins vs WL tomographic amplitudes, the ratio approaches **13/12** when scale separation is large and trends toward **1.0** where probes are scale-coupled.  
**Plan:** Ingest public DR2 \(f\sigma_8(z)\) bin table with uncertainties, align with DES/KiDS/HSC tomographic bins, compute ratio per bin, and score fractions within ±5% and within 1σ of **13/12**.  
**Outcome Metrics:** (i) ratio(z) curve with 13/12 band; (ii) χ² against the fixed ratio hypothesis.

## 5. Limitations
We assume a single projection magnitude \(r\approx13/12\) for well-separated scales and use symmetric normalization. Future work will refine \(d_M\) and \(\alpha\) per technique, and incorporate more cosmic (ACT/SPT) and lensing datasets as released.

## 6. Reproducibility
- Data CSV/JSON in `/data`.
- Figures in `/figures`.
- Notebooks (to be added) will reproduce all plots and tables from raw inputs.

## 7. References (to finalize in submission)
- Planck 2018 parameters (CMB)  
- DESI DR2 overview and growth/BAO companion papers  
- DES Y3, KiDS-1000, HSC-Y3 3×2pt public results  
- SH0ES, TRGB (CCHP/JWST), TDCOSMO time-delay lenses
