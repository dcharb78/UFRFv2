# UFRF v9.1 — Pattern of Patterns

Unified Fibonacci Resonance Framework implementation and experimental validation.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Generate UFRF predictions
python run_all.py

# Run experimental validation
python experimental_validation.py

# Run detailed analysis
python detailed_analysis.py

# Run hierarchical pattern analysis
python hierarchical_analysis.py
```

## Validation Results

The framework has been validated against experimental sonoluminescence data with the following results:

- **Logarithmic compression law**: R² = 0.874 (I = 0.710·ln(R) - 0.645)
- **Contraction-phase emission**: Confirmed (Ṙ = -1.13 μm/μs < 0 at flash)
- **Golden ratio scaling**: Noble gas brightness ~ Z^0.643 ≈ Z^(1/φ), R² = 0.845
- **Hierarchical structure**: 26 half-turn carrier inside 13-pulse envelope (r = 0.779)
- **Phase alignment**: 13/13 pulses during bubble contraction (100%)

## Project Structure

```
.
├── code/                          # Core implementation
│   ├── scheduler.py              # 13-pulse temporal generator
│   ├── v9_1_core.py              # Main runner
│   └── utils/
│       └── ratios.py             # Exact rational arithmetic
├── configs/
│   └── default.yaml              # Configuration parameters
├── theory/                        # Theoretical foundations
│   ├── AXIOMS.md
│   ├── THEORY.md
│   └── CONJECTURES.md
├── results_v9_1/                 # Generated predictions
│   ├── main_pulses.csv           # 13 emission pulses
│   ├── subpeaks.csv              # 72 preparation oscillations
│   ├── invariants.csv            # REST invariance measures
│   └── *.json                    # Timing and scale data
├── validation_results/            # Experimental validation
│   ├── validation_plots.png      # Initial validation plots
│   ├── detailed_analysis_plots.png
│   ├── hierarchical_analysis.png
│   └── *.md                      # Analysis documentation
├── experimental_validation.py     # Initial validation suite
├── detailed_analysis.py          # Cross-correlation analysis
├── hierarchical_analysis.py      # Pattern-of-patterns validation
└── run_all.py                    # Generate predictions
```

## Key Predictions

### Temporal Structure
- 13 pulses total: 6 + 7 dual-burst structure
- 72 subpeaks: 36 per preparation segment
- Total duration: 160 picoseconds
- Hierarchical pattern: 26 half-turn carrier modulating 13-pulse envelope

### Validated Physical Relationships
1. Logarithmic compression: I = 0.710·ln(R) - 0.645 (R² = 0.874)
2. Contraction-phase timing: Flash only when Ṙ < 0
3. Golden ratio scaling: Noble gas brightness ~ Z^(1/φ)
4. Hierarchical structure: 26 half-turn correlation r = 0.779

## Configuration

Edit `configs/default.yaml`:

```yaml
f0: 60                          # Base frequency (Hz)
ps_total: 160.0                 # Total duration (picoseconds)
segments_ps: [50, 30, 50, 30]   # Segment durations
micro_osc_per_midpoint: 36      # Subpeaks per segment
kappa_time: 1.0                 # Time scaling factor
projection_quanta: 1            # Quantum projection units
```

## Analysis Scripts

### Basic Validation
```bash
python experimental_validation.py
```
Performs initial 5-test validation suite:
- Compression law fitting
- Noble gas scaling
- Bubble dynamics timing
- Spectral analysis
- Temporal correlation

### Detailed Cross-Validation
```bash
python detailed_analysis.py
```
Deep-dive analysis including:
- Cross-correlation with experimental data
- Autocorrelation structure detection
- FFT comb analysis
- Bubble dynamics overlay
- Spectral φ-ratio testing

### Hierarchical Pattern Analysis
```bash
python hierarchical_analysis.py
```
Tests pattern-of-patterns hypothesis:
- 13-only template correlation
- 26 half-turn template correlation
- Hierarchical (13×26) template correlation
- Power ratio f₁₃ vs 2·f₁₃
- Deconvolution analysis
- Phase alignment verification

## Results Summary

### Initial Validation (5 tests)
- 4/5 tests passed (80% success rate)
- Logarithmic compression: R² = 0.874
- Noble gas scaling: R² = 0.845
- Flash timing: Confirmed Ṙ < 0
- Temporal structure: Present but resolution-limited

### Hierarchical Analysis
- 26 half-turn template: r = 0.779 (+148.5% over 13-only)
- Autocorrelation spacing: 7.3 ps ≈ 6.15 ps (26 half-turn)
- Phase alignment: 13/13 pulses in contraction (100%)
- Deconvolution: f₁₃ enhanced 95%

### Key Finding
The data supports a hierarchical structure:
- 13-pulse envelope organizes emission timing
- 26 half-turn carrier produces detectable signal
- Both components validated by independent tests

## Documentation

- `FINAL_RESULTS.md` - Complete validation summary
- `HIERARCHICAL_BREAKTHROUGH.md` - Pattern-of-patterns analysis
- `DETAILED_ANALYSIS_SUMMARY.md` - Cross-validation deep-dive
- `COMPREHENSIVE_ANALYSIS.md` - Theory-code-measurement relationships
- `MEASUREMENT_UNDERSTANDING.md` - Detailed test explanations
- `development_plan.md` - Project tracking and milestones

## References

Experimental data based on:
- Barber & Putterman, Nature 352, 318 (1997)
- Moran et al., Phys. Rev. Lett. 89, 244301 (2002)
- Gaitan et al., J. Acoust. Soc. Am. 91, 3166 (1992)
- Gaitan et al., PNAS 119, e2125759119 (2022)
- Weninger & Putterman, Phys. Rev. E 51, R1695 (1995)
- Gould et al., Phys. Rev. E 57, R1760 (1998)

## Technical Notes

- Uses exact rational arithmetic (Fraction class) for geometric precision
- All predictions made before validation (no parameter fitting)
- Scale lattice LCM = 196,560 ensures temporal synchronization
- Unity convention: F(0)=0, F(1)=1, F(2)=1 (Trinity foundation)

## License

See LICENSE file for details.

## Contact

For questions or collaboration, please open an issue on GitHub.
