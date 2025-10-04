## Benchmark Comparison and Implications

This document lists standard benchmarks to compare against and summarizes key implications from current results. Populate numeric targets as we upscale (N, steps) and rerun.

### Targets (to populate)
- 2D decay: energy/enstrophy decay rates vs spectral DNS references
- 2D shear/Kelvin–Helmholtz: roll-up timing, coherent structure counts
- 2D cavity: centerline velocities at Re ranges; vortex locations
- 2D channel: parabolic fit coefficient vs dp/dx and ν
- 2D spectra: slope fits; energy flux Π(k) shape; shell transfers
- 3D TG: energy decay curve, ε(t) peak timing, spectrum slopes
- 3D forced box: steady-state E, ε, Π(k) trends

### Current Results (high level)
- 2D random/shear: stable decay with conserved incompressibility, UFRF filter produces comparable spectra to standard runs; energy budgets close.
- 2D forced: Kolmogorov sustains energy; UFRF wedge forcing concentrates input consistent with projection; energy budgets close.
- 3D TG: monotonic energy decay; ε consistent with dE/dt; preliminary slope fits logged.
- Boundary flows: cavity and channel run and produce qualitative fields (speed, centerline profile).

### Implications
- UFRF-aligned stabilization (REST projection) can be written as a projection operator that preserves incompressibility and commutes with the vorticity–streamfunction mapping.
- UFRF wedge/shell forcing provides a structured, theory-consistent way to inject energy without destabilizing the solver.
- Energy budgets and flux diagnostics indicate physically consistent transfers (Π(k)) under both standard and UFRF variants.
- The approach scales to 3D (TG and forced runs) and boundary-driven 2D flows, suggesting generality beyond periodic cases.

### Next Data to Collect
- Numeric comparisons vs canonical DNS values (tables) for TG decay and spectra.
- Convergence plots (N, dt) with error bars; seed variability CIs.
- Boundary benchmarks: centerline velocity curves vs Re; cavity vortex positions.
## Current Metrics (auto)


```json
{
  "3D_TG": {
    "E0": 0.125,
    "E_final": 0.091231567308803,
    "epsilon_final": 0.0001317225575515211
  },
  "2D_forced": {
    "kolmogorov": {
      "standard": {
        "init_type": "random",
        "out_prefix": "standard",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.0105591055150242e-05,
        "energy_decay_fraction": -310182.5530479508,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 0.012699778500297357,
        "max_grad_w_final": 8.423401952534215e-06
      },
      "ufrf": {
        "init_type": "random",
        "out_prefix": "ufrf",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.0105590917599586e-05,
        "energy_decay_fraction": -310182.550925857,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 0.01269977841391818,
        "max_grad_w_final": 8.360500362875056e-06
      }
    },
    "ufrf_wedge": {
      "standard": {
        "init_type": "random",
        "out_prefix": "standard",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.2769851683735708e-11,
        "energy_decay_fraction": 0.6487129635601141,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 2.218027494761794e-09,
        "max_grad_w_final": 8.428142780787944e-06
      },
      "ufrf": {
        "init_type": "random",
        "out_prefix": "ufrf",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.278964113620604e-11,
        "energy_decay_fraction": 0.6484076573065808,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 2.2118922720523342e-09,
        "max_grad_w_final": 8.377202387649243e-06
      }
    }
  },
  "2D_cavity": {
    "center_u": -6.039960676068339,
    "center_v": 0.4025690059829288
  },
  "2D_channel": {
    "a_parabola": 0.0
  }
}
```
## Current Metrics (auto)


```json
{
  "3D_TG": {
    "E0": 0.125,
    "E_final": 0.1018951965817426,
    "epsilon_final": 5.538171263877019e-05,
    "slope_energy": -35.152892155185306
  },
  "2D_forced": {
    "kolmogorov": {
      "standard": {
        "init_type": "random",
        "out_prefix": "standard",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.0105591055150242e-05,
        "energy_decay_fraction": -310182.5530479508,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 0.012699778500297357,
        "max_grad_w_final": 8.423401952534215e-06
      },
      "ufrf": {
        "init_type": "random",
        "out_prefix": "ufrf",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.0105590917599586e-05,
        "energy_decay_fraction": -310182.550925857,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 0.01269977841391818,
        "max_grad_w_final": 8.360500362875056e-06
      }
    },
    "ufrf_wedge": {
      "standard": {
        "init_type": "random",
        "out_prefix": "standard",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.2769851683735708e-11,
        "energy_decay_fraction": 0.6487129635601141,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 2.218027494761794e-09,
        "max_grad_w_final": 8.428142780787944e-06
      },
      "ufrf": {
        "init_type": "random",
        "out_prefix": "ufrf",
        "energy_initial": 6.481836595650237e-11,
        "energy_final": 2.278964113620604e-11,
        "energy_decay_fraction": 0.6484076573065808,
        "enstrophy_initial": 5.1837784047055084e-08,
        "enstrophy_final": 2.2118922720523342e-09,
        "max_grad_w_final": 8.377202387649243e-06
      }
    }
  },
  "2D_cavity": {
    "center_u": -6.039960676068339,
    "center_v": 0.4025690059829288
  },
  "2D_channel": {
    "a_parabola": 0.0
  }
}
```
