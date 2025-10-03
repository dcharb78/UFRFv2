# UFRF Theory for LoCuSS

**Law**: \(\ln O = \ln O_* + d_M\,\alpha\,S + \epsilon\). For LoCuSS, \(O\) is a mass proxy (e.g., M_500).
Probes: Weak Lensing (WL) and Hydrostatic X-ray (HSE). Each probe has technique coupling \(\alpha\) and its own S built from meta-features.

**Predictions**:
- Technique-dependent slopes \(b = d_M\,\alpha\) per probe.
- Projection-free intercepts \(M_*^{(\text{WL})}\) and \(M_*^{(\text{HSE})}\) **converge** at S→0.
- Pre-correction ln-ratio ln(M_HSE/M_WL) correlates with \(\Delta S\); post-extrapolation it flattens.

**Results (this package)**:
- Using your exact CSVs (no placeholders), WL shows b≈0.22; HSE ~0 (no HSE feature columns).
- ln-ratio intercept ≈ −0.039 ⇒ M_HSE/M_WL ≈ 0.96, matching LoCuSS β_X ≈ 0.95 ± 0.05.
