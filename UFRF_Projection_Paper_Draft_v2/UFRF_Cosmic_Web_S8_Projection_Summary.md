# UFRF Projection Test on Cosmic Web Clumpiness (S8)

**Prediction:** for well-separated scale probes, the cosmic/local amplitude ratio should be near **13/12 ≈ 1.083333**.

**Data used (cosmic vs local):**
- Planck 2018 (CMB): S8 = 0.832 ± 0.013
- DES Y3 (3×2pt): S8 = 0.776 ± 0.017
- KiDS-1000 (3×2pt): S8 = 0.766 ± 0.020
- KiDS-1000 (shear-only): S8 = 0.759 ± 0.024
- HSC-Y3 (3×2pt): S8 = 0.776 ± 0.033

**Results (cosmic/local ratios):**
   cosmic_dataset          local_dataset  S8_cosmic  S8_cosmic_sigma  S8_local  S8_local_sigma  ratio_cosmic_over_local  ratio_sigma  predicted_13_over_12  delta_to_pred  z_to_pred
Planck 2018 (CMB)         DES Y3 (3x2pt)      0.832            0.013     0.776           0.017                   1.0722       0.0289                1.0833        -0.0112    -0.3871
Planck 2018 (CMB)      KiDS-1000 (3x2pt)      0.832            0.013     0.766           0.020                   1.0862       0.0330                1.0833         0.0028     0.0856
Planck 2018 (CMB) KiDS-1000 (shear-only)      0.832            0.013     0.759           0.024                   1.0962       0.0387                1.0833         0.0128     0.3323
Planck 2018 (CMB)         HSC-Y3 (3x2pt)      0.832            0.013     0.776           0.033                   1.0722       0.0486                1.0833        -0.0112    -0.2299

**Summary:**
- n_pairs = 4
- mean ratio = 1.0817, std = 0.0117
- fraction within 5% of 13/12 = 1.00
- fraction consistent with 13/12 within 1σ = 1.00

**Interpretation:** Ratios cluster around 13/12, with small deviations and uncertainties usually bringing them into 1σ agreement. This mirrors the H0 result but with **cosmic/local** instead of **local/cosmic** due to opposite projection coupling sign.
