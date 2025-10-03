# OBJECTIONS & RESPONSES (Graphene Coupling Package)

## 1) "Different techniques disagree—your α just curve-fits that."
**Response:** The framework predicts *a priori* that techniques map to different α (observer–system coupling).
Empirically, α is the slope of `log(O)` vs `S~log(M1/M0)`. If α is mere curve-fitting, it won’t remain stable
across different knobs (dielectric, invasiveness, density, current). Our protocol requires **multi-knob consistency**
and pooled fixed effects. **Falsification:** α varies wildly or flips sign across knobs/replicates.

## 2) "Disorder alone explains everything."
**Response:** We model disorder explicitly as technique/device offsets (intercepts). Disorder changes `a`,
not the slope `b`. **Falsification:** When devices are cleaned/encapsulated, the intercepts may change,
but **slopes (α)** should remain within CI if the technique is unchanged.

## 3) "Your REST target (η/s ≈ (1/4π)√φ) is numerology."
**Response:** It arises from the UFRF symmetry (13-cycle, REST at 6.5/13) and Dirac-fluid minimal viscosity scaling.
**Falsification:** After α-correction and offset removal, O_* across techniques fails to converge toward ~0.101
in clean devices (within stated uncertainty).

## 4) "Fibonacci ratios in spectra are artifacts."
**Response:** Ratios (e.g., 13:8) are predicted to be **α-robust**. **Falsification:** Ratios drift systematically with S
or technique after controlling for noise and peak detection bias.

## 5) "28 K feature is cherry-picked."
**Response:** We specify a **priors-based window** (25–32 K) and require consistent replication across clean devices,
with pre-registered analysis. **Falsification:** No reproducible feature appears in the window beyond noise.

## 6) "S is ambiguous; how do you compute log(M1/M0)?"
**Response:** We use **surrogate S** assembled from lab knobs (dielectric, invasiveness, density, current) with
technique-specific weights, then check **robustness across alternative S constructions**. **Falsification:** Results
depend critically on one arbitrary S choice and collapse under alternatives.

## 7) "Multicollinearity among knobs can corrupt the slope."
**Response:** We recommend orthogonal sweeps and VIF checks; if knobs are correlated, use PCA to construct S
and report stability across components.

## 8) "Local heating confounds α."
**Response:** Include current-density in S, keep within hydrodynamic window, and monitor via nonlocal probes.
Check α stability across current-only vs dielectric-only sweeps.

## 9) "Your statistics are too optimistic."
**Response:** We report 95% CIs, use pooled fixed effects, and suggest bootstrap resampling. **Falsification:**
Bootstrap CIs balloon or estimates are unstable across resamples.

## 10) "Alternative theories explain the same data."
**Response:** That’s fine—our **differential** predictions are (i) α as a slope in log-space, (ii) post-correction
convergence to O_*, and (iii) ratio invariance. If another theory predicts these more tightly, it should outperform us
on the same preregistered datasets.
