# Full M-scaling Test Run — Summary

**Timestamp:** 2025-10-01 21:07 UTC

## Ground Truth
- O_* (true): 0.101
- d_M (true): 1.0
- α (true) by technique: NonlocalHydro=0.18, THzOptical=0.47, ARPES=0.78

## Per-Technique Fit Results (log O = a + b S)

| technique     |   alpha_true |    b_est |   b_ci_low |   b_ci_high |    a_est |   a_ci_low |   a_ci_high |       r2 |
|:--------------|-------------:|---------:|-----------:|------------:|---------:|-----------:|------------:|---------:|
| ARPES         |         0.78 | 0.783001 |  0.648923  |    0.917079 | -2.39244 |   -2.50247 |    -2.28242 | 0.549072 |
| NonlocalHydro |         0.18 | 0.179384 |  0.0828987 |    0.27587  | -2.2309  |   -2.32575 |    -2.13604 | 0.109854 |
| THzOptical    |         0.47 | 0.46997  |  0.34605   |    0.59389  | -2.2612  |   -2.37674 |    -2.14565 | 0.339295 |

## Intrinsic REST Estimates O_*

| technique     |   O_star_est |   O_star_CI_low |   O_star_CI_high |
|:--------------|-------------:|----------------:|-----------------:|
| ARPES         |   0.091406   |      0.0818826  |       0.102037   |
| NonlocalHydro |   0.0307921  |      0.0280056  |       0.0338559  |
| THzOptical    |   0.00125519 |      0.00111822 |       0.00140893 |

## Pooled Model (Technique & Device Fixed Effects)

| term                   |      beta |       ci_low |      ci_high |            se |
|:-----------------------|----------:|-------------:|-------------:|--------------:|
| intercept              | -5.37392  |  -8.24468    |  -2.50316    |   1.45918     |
| S                      |  2.35698  |   0.144054   |   4.56991    |   1.12481     |
| tech_NonlocalHydro     |  1.2496   | nan          | nan          | nan           |
| tech_THzOptical        |  4.41927  |  -2.0215e+08 |   2.0215e+08 |   1.02751e+08 |
| dev_ARPES_dev2         | -0.140433 |  -3.36069    |   3.07983    |   1.63682     |
| dev_ARPES_dev3         | -0.417387 |  -3.63765    |   2.80287    |   1.63682     |
| dev_ARPES_dev4         | -0.285128 |  -3.50539    |   2.93513    |   1.63682     |
| dev_NonlocalHydro_dev1 | -9.88049  | nan          | nan          | nan           |
| dev_NonlocalHydro_dev2 | -2.99843  | nan          | nan          | nan           |
| dev_NonlocalHydro_dev3 | -6.56635  | nan          | nan          | nan           |

## Fibonacci Ratio Robustness (mean ± std)

| technique     |   ratio_8_5_mean |   ratio_8_5_std |   ratio_13_8_mean |   ratio_13_8_std |   ratio_21_13_mean |   ratio_21_13_std |   ratio_34_21_mean |   ratio_34_21_std |
|:--------------|-----------------:|----------------:|------------------:|-----------------:|-------------------:|------------------:|-------------------:|------------------:|
| ARPES         |          1.60372 |       0.0662972 |           1.61854 |        0.0734004 |            1.62447 |         0.0801882 |            1.62436 |         0.0747202 |
| NonlocalHydro |          1.60075 |       0.0643726 |           1.62985 |        0.067293  |            1.62214 |         0.0733361 |            1.62081 |         0.0690133 |
| THzOptical    |          1.6031  |       0.0692706 |           1.62934 |        0.0694499 |            1.61671 |         0.0652653 |            1.6185  |         0.0702112 |