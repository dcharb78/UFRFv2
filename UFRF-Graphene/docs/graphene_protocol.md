# Graphene / 2D Dirac Materials — Protocol

## Goals
- Estimate technique coupling **α** and recover **O\_*** at REST.
- Partition observed prefactor differences into **M-shift**, **disorder**, and **2D projection**.
- Check Fibonacci ratio invariance; scan for a **~28 K** feature in clean devices.

## Steps
1. **Matrixed sweeps** across lab knobs (dielectric, invasiveness, density, current) to span **S ≈ log(M1/M0)**.
2. **Measure** η/s and conductance spectra per technique.
3. **Fit per technique**: `log(O_meas) = a + b S` → `b ≈ d_M α` (η/s: `d_M ≈ +1`).
4. **Pooled model** with technique/device fixed effects to remove offsets.
5. **Recover O_*:** `exp(a - offset)` at `S=0`; compare across techniques and to the **0.101** prediction.
6. **Ratios:** verify that 13:8 (and others) remain invariant vs S.
7. **28 K scan:** high-resolution thermal sweep around 25–32 K in the cleanest devices.
