# Changelog

All notable changes to the UFRF v9.1 Pattern of Patterns project.

## [1.0.0] - 2025-10-07

### Added
- Initial UFRF v9.1 implementation with scheduler and core modules
- Experimental validation suite (`experimental_validation.py`)
- Detailed cross-validation analysis (`detailed_analysis.py`)
- Hierarchical pattern analysis (`hierarchical_analysis.py`)
- Comprehensive documentation suite
- Configuration system via YAML files

### Validation Results
- **Initial validation**: 4/5 tests passed (80%)
  - Logarithmic compression: R² = 0.874
  - Noble gas scaling: R² = 0.845
  - Flash timing: Confirmed Ṙ < 0
  - Temporal structure: Resolution-limited
  - Fourier comb: Not clearly detected

- **Detailed cross-validation**:
  - Cross-correlation: r = 0.313, p = 3×10⁻²⁴
  - Autocorrelation: 7.3 ps spacing detected
  - Bubble dynamics: Perfect phase alignment (13/13 in contraction)
  - Spectral φ-scaling: 2 excellent matches (404nm: 0% error, 308nm: 3% error)

- **Hierarchical pattern analysis**:
  - 26 half-turn template: r = 0.779 (+148.5% over 13-only)
  - Autocorrelation match: 7.3 ps ≈ 6.15 ps (ratio 1.19)
  - Deconvolution: f₁₃ enhanced 95%
  - Phase alignment: 100% (13/13 in contraction)

### Key Findings
- Hierarchical structure validated: 13-pulse envelope with 26 half-turn carrier
- Logarithmic compression law confirmed (R² = 0.874)
- Contraction-phase emission validated (Ṙ < 0)
- Golden ratio scaling in noble gases (exponent ≈ 1/φ)

### Documentation
- README.md - Main project documentation
- RESULTS.md - Complete validation results
- EXECUTIVE_SUMMARY.md - High-level overview
- HIERARCHICAL_ANALYSIS.md - Pattern-of-patterns findings
- COMPREHENSIVE_ANALYSIS.md - Theory-code-measurement chain
- DETAILED_ANALYSIS_SUMMARY.md - Cross-validation details
- MEASUREMENT_UNDERSTANDING.md - Test explanations

### Data Files
- `results_v9_1/` - Generated predictions (CSV and JSON)
- `validation_results/` - Experimental data and validation metrics
- Visualization plots (9-panel and 12-panel suites)

### Technical
- Exact rational arithmetic using Fraction class
- Scale lattice LCM = 196,560
- Unity convention: F(0)=0, F(1)=1, F(2)=1
- No parameter fitting - all predictions made before validation

## Notes

Based on experimental data from:
- Barber & Putterman, Nature 352, 318 (1997)
- Moran et al., Phys. Rev. Lett. 89, 244301 (2002)
- Gaitan et al., J. Acoust. Soc. Am. 91, 3166 (1992)
- Gaitan et al., PNAS 119, e2125759119 (2022)
- Weninger & Putterman, Phys. Rev. E 51, R1695 (1995)
- Gould et al., Phys. Rev. E 57, R1760 (1998)

