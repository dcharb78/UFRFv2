# LoCuSS Full Projection CV Package - Complete with WL, HSE, and SZ

## Overview

This is the **complete LoCuSS (Local Cluster Substructure Survey) package** with full projection cross-validation data for all three major mass measurement techniques:

1. **Weak Lensing (WL)** - Gravitational lensing mass measurements
2. **Hydrostatic Equilibrium (HSE)** - X-ray based mass estimates  
3. **Sunyaev-Zel'dovich (SZ)** - Compton scattering mass measurements

## Dataset Description

### Cluster Sample
- **50 galaxy clusters** from the LoCuSS survey
- Redshift range: z = 0.15 - 0.30
- All clusters have measurements from all three techniques

### Measurement Techniques

#### Weak Lensing (WL)
- **File**: `data/locuss_wl_m500.csv`
- **Columns**: 
  - cluster_id: Cluster identifier
  - z: Redshift
  - M500_WL: Mass within R500 (10^14 M_sun)
  - M500_WL_err: Measurement uncertainty
  - psf_over_size: PSF/galaxy size ratio (systematics indicator)
  - snr: Signal-to-noise ratio
  - photoz_width: Photometric redshift uncertainty
- **Source**: Okabe & Smith (2016)

#### Hydrostatic Equilibrium (HSE)
- **File**: `data/locuss_hse_m500.csv`
- **Columns**:
  - cluster_id: Cluster identifier
  - z: Redshift
  - M500_HSE: Mass within R500 (10^14 M_sun)
  - M500_HSE_err: Measurement uncertainty
- **Source**: Martino et al. (2014), based on Chandra/XMM observations

#### Sunyaev-Zel'dovich (SZ)
- **File**: `data/locuss_sz_m500.csv`
- **Columns**:
  - cluster_id: Cluster identifier
  - z: Redshift
  - M500_SZ: Mass within R500 (10^14 M_sun)
  - M500_SZ_err: Measurement uncertainty
  - Y500: Integrated Compton parameter
  - Y500_err: Y500 uncertainty
  - survey: Data source (Planck/ACT)
- **Sources**: Planck PSZ2 catalog, ACT observations

## Analysis Tools

### Main Analysis Script
```bash
python code/run_locuss_validation_full.py \
  --wl data/locuss_wl_m500.csv \
  --hse data/locuss_hse_m500.csv \
  --sz data/locuss_sz_m500.csv \
  --out results/
```

### Key Features
- **UFRF Projection Law Fitting**: log(M) = a + b*S for each probe
- **PCA-based Projection Scale**: Extracts systematic effects (S) from meta-features
- **Three-Probe Convergence Analysis**: Tests if M* values converge at S→0
- **Cross-Probe Calibration**: Computes mass ratios and correlations
- **Comprehensive Visualization**: 
  - Individual probe fits
  - Three-probe comparison
  - Mass ratio correlations

### Expected Results

#### Projection Law Parameters
Each probe should show:
- Different slopes (b) reflecting technique-specific systematics
- Convergent intercepts (a) leading to similar M* values

#### Mass Ratios (Typical Values)
- M_HSE/M_WL ≈ 0.95-0.97 (hydrostatic bias)
- M_SZ/M_WL ≈ 1.05-1.10 (SZ calibration offset)
- M_SZ/M_HSE ≈ 1.10-1.15

#### UFRF Validation
The convergence of projection-free masses (M*) across all three techniques validates:
1. Universal underlying mass exists
2. Technique-specific biases can be modeled and corrected
3. UFRF projection law captures systematic effects

## Installation & Requirements

```bash
# Install dependencies
pip install -r requirements.txt

# Required packages:
# - numpy >= 1.21.0
# - matplotlib >= 3.4.0
# - scikit-learn >= 1.0.0
# - pandas >= 1.3.0
```

## Output Products

Running the full analysis generates:

1. **Plots** (PNG format):
   - `FIT_WL.png`: WL mass vs projection scale
   - `FIT_HSE.png`: HSE mass vs projection scale
   - `FIT_SZ.png`: SZ mass vs projection scale
   - `THREE_PROBE_COMPARISON.png`: All probes overlaid
   - `MASS_RATIOS.png`: Cross-probe ratio analysis

2. **Data Products**:
   - `summary.json`: Numerical results in JSON format
   - `REPORT.md`: Human-readable analysis report

3. **Key Metrics**:
   - Projection slopes (b) for each probe
   - Projection-free masses (M*) 
   - Convergence statistics
   - Mass ratio calibrations

## Scientific Context

### LoCuSS Survey
The Local Cluster Substructure Survey is a systematic study of galaxy cluster masses using multiple independent techniques. It provides an ideal dataset for testing mass calibration and systematic effects.

### Mass Measurement Challenges
Different techniques probe different aspects of clusters:
- **WL**: Total mass (dark + baryonic) via gravitational deflection
- **HSE**: Gas mass profile assuming hydrostatic equilibrium
- **SZ**: Integrated gas pressure via inverse Compton scattering

### UFRF Contribution
The Universal Fractal Resonance Framework provides a unified model for:
- Understanding technique-specific biases as projection effects
- Extracting projection-free masses through S→0 extrapolation
- Validating mass convergence across independent probes

## References

1. Okabe & Smith (2016): "LoCuSS: weak-lensing mass calibration of galaxy clusters"
2. Martino et al. (2014): "LoCuSS: hydrostatic mass measurements"  
3. Smith et al. (2015): "LoCuSS: Testing hydrostatic equilibrium"
4. Planck Collaboration: "Planck 2015 results. XXVII. The second Planck catalogue of Sunyaev-Zeldovich sources"

## Contact & Usage

This package is part of the UFRF validation suite. For questions or collaboration:
- Repository: UFRFv2
- License: CC BY-NC 4.0

## Version History

- v1.0: Initial WL + HSE two-probe analysis
- v2.0: **Complete three-probe package with SZ data** (current)

---

*This complete package enables full cross-validation of the UFRF projection law using all three major cluster mass measurement techniques.*
