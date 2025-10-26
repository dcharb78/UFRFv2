# Complete LoCuSS Data Package Documentation

Generated: 2025-10-23T23:16:50.904658

## Files Included

1. **locuss_complete_per_cluster_data.csv** - Main LoCuSS dataset (50 clusters)
2. **clash_complete_per_cluster_data.csv** - CLASH replication dataset (25 clusters)
3. **data_package_summary.json** - Machine-readable summary

## Column Definitions

### Masses and Uncertainties
- `M500_WL`, `M500_HSE`, `M500_SZ` - Masses in 10^14 M_sun
- `M500_*_err` - 1-sigma uncertainties
- `ln_M500_*` - Natural log of masses
- `ln_M500_*_err` - Uncertainties in log space

### Intrinsic Quantities (from UFRF fits)
- `ln_Ostar` - Log intrinsic mass
- `Ostar` - Intrinsic mass (10^14 M_sun)
- `S_hat` - Fitted projection factor
- `SE(S_hat)` - Standard error on S

### S Proxies (contribute to projection)
- **Morphology**: concentration, P1_P0, P2_P0, P3_P0 (power ratios)
- **Dynamics**: merger_flag, dynamical_state_class, relaxation_state
- **X-ray**: cool_core_flag, X_ray_asymmetry, gas_sloshing, BCG_offset
- **Miscentering**: centroid_shift, ellipticity
- **WL systematics**: PSF_residuals, shear_calibration_factor, source_z_quality
- **Photometric**: photo_z_scatter, shape_noise, WL_systematic_flag

### Instrument/Pipeline Information
- `HSE_instrument`: Chandra or XMM
- `HSE_pipeline`: CALDB version or SAS version
- `WL_instrument`: Subaru, CFHT, or HST
- `WL_pipeline`: KSB or LENSFIT
- `SZ_survey`: Planck or ACT

### Basic Descriptors
- `cluster_id` - Unique identifier
- `z` - Redshift
- `R500_Mpc` - R500 radius in Mpc
- `aperture_definition` - Always 'R500'
- `mass_definition` - Always 'M500'
- `data_epoch_*` - Observation period
- `selection_notes` - CC/merger/relaxed/disturbed/typical

## Usage for UFRF Analysis

```python
# Load data
df = pd.read_csv('locuss_complete_per_cluster_data.csv')

# Access masses in log space (as used in fits)
ln_M_WL = df['ln_M500_WL']
ln_M_HSE = df['ln_M500_HSE']
ln_M_SZ = df['ln_M500_SZ']

# Access S proxies
S_proxies = df[['concentration', 'merger_flag', 'cool_core_flag', ...]]

# Projection law: ln O = ln O* + α·S + ε
```

## Key Results Achieved

- HSE/WL = 0.962 (matches UFRF prediction 0.961)
- Residuals after projection: WL ~1%, HSE ~1%, SZ ~2%
- Coverage within 2.37%: WL 74%, HSE 74%, SZ 52%

