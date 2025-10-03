# Graphene Protocol — M-Scaling Addendum (v6.1)
**Timestamp:** 2025-10-01 21:03 UTC

## Purpose
Incorporate observer–system scale coupling into the graphene/2D REST validation so that technique-dependent
measurements are modeled consistently.

## Framework
Let the observer be at scale **M₀** (apparatus/environment) and the system at **M₁** (device/material).
Define **effective measurement scale**:
\[
 M_\mathrm{eff} = M_0\left(\tfrac{M_1}{M_0}\right)^\alpha, \quad \alpha \in [0,1]
\]
- **α = 0**: No coupling (stay at M₀)
- **α = 1**: Full coupling (shift to M₁)
- **α = 0.5**: Geometric mean (√(M₀ M₁))

For any observable \(O\) with M-scaling dimension \(d_M\), the measured value obeys
\[
 O_\mathrm{meas} = O_* \left(\tfrac{M_1}{M_0}\right)^{d_M\,\alpha}
\]
where \(O_*\) is the intrinsic (REST) value we seek (α→0 limit under ideal isolation).

Taking logs gives a linear fit in \(\alpha\):
\[
 \log O_\mathrm{meas} = \log O_* + d_M\,\alpha\,\log\!\left(\tfrac{M_1}{M_0}\right).
\]

## Practical Mapping for Graphene
Choose a proxy for \(\log(M_1/M_0)\) that your lab can dial:
- **Dielectric screening**: vary \(\varepsilon_\mathrm{eff}\) using vacuum vs hBN vs high-κ caps.
- **Encapsulation & disorder**: hBN thickness; edge roughness; polymer residue (AFM/STM-confirmed).
- **Hydrodynamic knob**: contact invasiveness and channel aspect ratio (nonlocality strength).
- **Carrier density**: gate voltage; keeps device in the Dirac hydrodynamic window.
- **Current density**: sets local heating/phonon coupling (affects α via apparatus back-action).
- **Strain**: uniaxial/biaxial; modifies v_F and pseudogauge fields.

For each knob, define a monotone surrogate **S** for \(\log(M_1/M_0)\).

## Observables and d_M (first-order)
- **η/s (Dirac fluid)**: \(d_M \approx +1\). Expect trend **toward** the intrinsic REST value
  \( (1/4\pi)\sqrt\varphi \approx 0.101 \) as α ↓ (clean, decoupled limit).
- **Effective fine-structure (α_eff)** in 2D: \(d_M \approx -1\) if dominated by screening (α increases → α_eff decreases).
- **Conductance spectra**: use *ratio* features (Fibonacci 8:5, 13:8, …) that should be invariant under α;
  deviations quantify residual coupling.

> Note: \(d_M\) can be refined per observable by perturbation around REST; start with ±1
> and update via multi-parameter regression (below).

## How the “Factor of 4” Fits
Earlier we decomposed the observed factor-of-4 as
**√φ × disorder × 2D projection ≈ 4**.
With M-scaling, part of this “4” can be absorbed into \( (M_1/M_0)^{d_M\alpha} \).
Thus different techniques (different α) legitimately report different prefactors without contradiction.
Your regression should allocate variance between **intrinsic** vs **M-coupling** vs **disorder** cleanly.

## Experimental Protocol (augmenting the main graphene doc)
1. **Matrixed runs**: For each device geometry, execute a sweep over \(S\) (e.g., \(\varepsilon_\mathrm{eff}\), invasiveness, density).
2. **Measure**: η/s (via thermal & nonlocal transport), α_eff proxies, and conductance spectra.
3. **Fit**:
   - Regress \( \log O_\mathrm{meas} \) against \(S\) to estimate **slope** = \( d_M\,\alpha \).
   - Use multiple knobs to disambiguate \(d_M\) vs \(\alpha\); consistency across knobs indicates a good model.
   - The **intercept** estimates \(\log O_*\) (intrinsic REST value).
4. **Cross-checks**:
   - Fibonacci ratio invariants should be the most **α-robust** signatures.
   - Extrapolate \(\alpha \to 0\) (max isolation) to recover \(O_*\). Compare to √φ prediction for η/s and to critical REST angles (≈137.5°) in vortex patterns.
5. **Report**:
   - \(O_*\) with CI, \(d_M\) with CI, and \(\alpha\) per technique.
   - Partition of the “4×” between M-shift, disorder, and 2D projection.

## Suggested Technique-α Heuristics (initial priors)
- **ARPES / near-field probes**: higher α (more system-coupled).
- **Four-probe nonlocal hydrodynamics**: lower α (more observer-framed, less invasive).
- **STM/STS contact-local**: medium–high α (local back-action).
- **Far-field optical (ellipsometry, THz)**: medium α (field penetration depth sets effective coupling).

## Deliverables to Add
- A small notebook template that reads a CSV of sweeps, performs the log-linear fits, and outputs
  (O_*, d_M, α) with error bars.
- Update the graphene results section to show before/after **α-correction** (extrapolation to α→0).

## Acceptance Criteria
- Recover \(\eta/s\to (1/4\pi)\sqrt\varphi\) within uncertainty after α-correction on at least one clean device.
- Demonstrate that between-technique discrepancies shrink markedly once α is modeled.
