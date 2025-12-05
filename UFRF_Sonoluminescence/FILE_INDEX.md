# File Index

Complete index of files in the UFRF v9.1 Pattern of Patterns repository.

## Root Directory

| File | Description |
|------|-------------|
| `README.md` | Main project documentation and quick start guide |
| `RESULTS.md` | Complete validation results and findings |
| `EXECUTIVE_SUMMARY.md` | High-level overview of validation |
| `PROJECT_STATUS.md` | Current project status and phase completion |
| `CHANGELOG.md` | Version history and notable changes |
| `CONTRIBUTING.md` | Contribution guidelines |
| `LICENSE` | CC0 1.0 Public Domain |
| `FILE_INDEX.md` | This file - complete file listing |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git ignore patterns |
| `run_all.py` | Main script to generate UFRF predictions |

## Analysis Scripts

| File | Lines | Description |
|------|------:|-------------|
| `experimental_validation.py` | 855 | Initial 5-test validation suite |
| `detailed_analysis.py` | 600+ | Deep cross-validation analysis |
| `hierarchical_analysis.py` | 700+ | Pattern-of-patterns validation |

## Core Code (`code/`)

| File | Description |
|------|-------------|
| `__init__.py` | Package initialization |
| `v9_1_core.py` | Main runner and CSV output |
| `scheduler.py` | 13-pulse temporal generator |
| `utils/__init__.py` | Utilities package init |
| `utils/ratios.py` | Exact rational arithmetic |

## Configuration (`configs/`)

| File | Description |
|------|-------------|
| `default.yaml` | Default parameters (160 ps, 13 pulses, 72 subpeaks) |

## Theory (`theory/`)

| File | Description |
|------|-------------|
| `AXIOMS.md` | Geometric axioms |
| `THEORY.md` | Full theoretical framework |
| `CONJECTURES.md` | Theoretical predictions |
| `LEARNING_NOTES.md` | Development notes |
| `APPROACH.md` | Methodological approach |

## Generated Predictions (`results_v9_1/`)

### CSV Files
| File | Rows | Description |
|------|-----:|-------------|
| `main_pulses.csv` | 13 | Main emission pulses with timing |
| `subpeaks.csv` | 72 | Preparation oscillations |
| `commutation_defects.csv` | 13 | Phase corrections |
| `invariants.csv` | 13 | REST invariance measures |

### JSON Files
| File | Description |
|------|-------------|
| `pattern_schedule.json` | Segment boundaries and timing |
| `scale_lattice.json` | Denominators and LCM (196,560) |

## Validation Results (`validation_results/`)

### Documentation
| File | Description |
|------|-------------|
| `HIERARCHICAL_ANALYSIS.md` | Pattern-of-patterns findings |
| `DETAILED_ANALYSIS_SUMMARY.md` | Cross-validation deep-dive |
| `COMPREHENSIVE_ANALYSIS.md` | Theory-code-measurement chain |
| `MEASUREMENT_UNDERSTANDING.md` | Detailed test explanations |
| `VALIDATION_REPORT.md` | Initial technical summary |

### Experimental Data (CSV)
| File | Description |
|------|-------------|
| `experimental_time_resolved.csv` | Flash intensity vs time (1000 points) |
| `experimental_bubble_dynamics.csv` | R(t) and Ṙ(t) (1000 points) |
| `experimental_spectrum.csv` | Wavelength vs intensity (450 points) |

### Metrics (JSON)
| File | Description |
|------|-------------|
| `validation_metrics.json` | Initial validation metrics |
| `detailed_metrics.json` | Deep-dive analysis metrics |
| `hierarchical_metrics.json` | Pattern-of-patterns metrics |

### Visualizations (PNG)
| File | Panels | Description |
|------|-------:|-------------|
| `validation_plots.png` | 9 | Initial validation suite |
| `detailed_analysis_plots.png` | 9 | Cross-validation analysis |
| `hierarchical_analysis.png` | 12 | Pattern-of-patterns validation |

## Key Metrics Summary

### Predictions
- Main pulses: 13 (6 + 7 dual-burst)
- Subpeaks: 72 (36 per prep segment)
- Total duration: 160 ps
- Scale lattice LCM: 196,560

### Validation Results
- Logarithmic compression: R² = 0.874
- Noble gas scaling: R² = 0.845
- Flash timing: Ṙ < 0 confirmed
- 26 half-turn correlation: r = 0.779
- Phase alignment: 13/13 in contraction (100%)

### Data Sources
- 6 published experimental studies (1992-2022)
- Representative data for time-resolved, bubble dynamics, and spectral analysis
- Total experimental points: ~2500

## Usage Guide

### Generate Predictions
```bash
python run_all.py
# Output: results_v9_1/
```

### Run Validation
```bash
python experimental_validation.py
# Output: validation_results/validation_*
```

### Run Deep Analysis
```bash
python detailed_analysis.py
# Output: validation_results/detailed_*
```

### Run Hierarchical Analysis
```bash
python hierarchical_analysis.py
# Output: validation_results/hierarchical_*
```

## Documentation Reading Order

1. `README.md` - Start here
2. `EXECUTIVE_SUMMARY.md` - High-level overview
3. `RESULTS.md` - Complete findings
4. `validation_results/HIERARCHICAL_ANALYSIS.md` - Key discovery
5. `validation_results/COMPREHENSIVE_ANALYSIS.md` - Deep theory
6. `PROJECT_STATUS.md` - Current status
7. `CHANGELOG.md` - Version history

## Total Project Size

- Python code: ~2200 lines (3 analysis scripts)
- Documentation: ~15,000 words (8 main documents)
- Data files: 11 CSV/JSON files
- Visualizations: 3 PNG files (30 total panels)
- Configuration: 1 YAML file
- Total files: ~50

---

**Last Updated**: 2025-10-07  
**Framework Version**: v9.1

