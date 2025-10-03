# DATA_SCHEMA.md — CSV Columns

## Measurements CSV (`your_measurements.csv`)
Required:
- `technique` (string)
- `device` (string)
- `S_log_M_ratio` (float) — surrogate for `log(M1/M0)` (built from knobs)
- `O_meas` (float) — measured observable, e.g., η/s

Optional (recommended diagnostics):
- `dielectric`, `invasiveness`, `density`, `current` (floats)

## Ratios CSV (`your_fibonacci_ratios.csv`)
- `technique`, `device`, `S_log_M_ratio`
- `ratio_8_5`, `ratio_13_8`, `ratio_21_13`, `ratio_34_21`
