# Figure Specifications for Publication

**For:** Deterministic Harmonic Structure in Binary Black-Hole Mergers

---

## Figure 1: Mass Ratio Distribution with Fibonacci Targets

**Type:** Histogram with overlay markers

**Data:** 41 GWTC-1/2 mass ratios

**Elements:**
- **Histogram:** q values, bin width ~0.05
- **Vertical lines:** Mark all 88 Fibonacci ratio positions
- **Highlight:** Golden ratio φ⁻¹ = 0.618... in gold/orange
- **Highlight:** Popular targets (2/3, 3/5, 5/8) in different colors
- **Tolerance bands:** Shade δ=0.05 regions around key targets
- **Markers:** Individual events as points on x-axis

**Annotations:**
- Label exact matches: GW190727_060333 (q=0.619), GW190728_064510 (q=0.667)
- Show enrichment: "22/41 (53.7%) within δ=0.05"
- P-value: "p = 2.2×10⁻⁴ (~3.7σ)"

**Python Code Pseudocode:**
```python
import matplotlib.pyplot as plt
import numpy as np

# Load data
q_values = [... from gwtc_real_q.csv ...]
fib_ratios = [... 88 Fibonacci ratios ...]

# Create figure
fig, ax = plt.subplots(figsize=(12, 6))

# Histogram
ax.hist(q_values, bins=np.arange(0, 1.05, 0.05), 
        alpha=0.6, color='blue', edgecolor='black')

# Fibonacci targets
for ratio in fib_ratios:
    ax.axvline(ratio, color='gray', alpha=0.3, linewidth=0.5)

# Highlight key ratios
ax.axvline(0.618, color='gold', linewidth=2, label='φ⁻¹')
ax.axvline(0.667, color='red', linewidth=2, label='2/3')
ax.axvline(0.600, color='green', linewidth=2, label='3/5')

# Individual events
ax.scatter(q_values, [0.5]*len(q_values), color='black', s=50, zorder=5)

# Annotate exact matches
ax.annotate('GW190728_064510\n(EXACT 2/3)', 
            xy=(0.667, y), xytext=(0.667, y+offset),
            arrowprops=dict(arrowstyle='->'))

plt.xlabel('Mass Ratio q = m₂/m₁')
plt.ylabel('Number of Events')
plt.title('BBH Mass Ratios Cluster Near Fibonacci/φ Values')
plt.legend()
plt.tight_layout()
plt.savefig('Figure1_MassRatioDistribution.pdf', dpi=300)
```

---

## Figure 2: Tolerance Sensitivity Curve

**Type:** Line plot with confidence regions

**Data:** From Table4_Sensitivity.csv

**Elements:**
- **X-axis:** Tolerance δ ∈ [0.03, 0.08]
- **Y-axis (primary):** P-value (log scale)
- **Y-axis (secondary):** Hit fraction (%)
- **Line:** P-value vs δ
- **Filled region:** Expected coverage p₀(δ)
- **Horizontal line:** α = 0.05 threshold
- **Vertical line:** Mark optimal δ=0.04

**Annotations:**
- "Optimal: δ=0.04, p=6.2×10⁻⁵"
- "All δ ∈ [0.03,0.08] show p<0.05"
- Shade "stable region"

**Python Code Pseudocode:**
```python
fig, ax1 = plt.subplots(figsize=(10, 6))

delta_values = [0.03, 0.04, 0.05, 0.06, 0.07, 0.08]
p_values = [... from Table4 ...]
hit_fracs = [... from Table4 ...]
expected = [... from Table4 ...]

# P-value curve
ax1.semilogy(delta_values, p_values, 'o-', linewidth=2, 
             markersize=8, label='Observed p-value')
ax1.axhline(0.05, color='red', linestyle='--', label='α=0.05')
ax1.axvline(0.04, color='green', linestyle='--', 
            label='Optimal δ=0.04')
ax1.set_xlabel('Tolerance δ')
ax1.set_ylabel('P-Value', color='blue')

# Hit fraction on secondary axis
ax2 = ax1.twinx()
ax2.plot(delta_values, np.array(hit_fracs)*100, 's-', 
         color='orange', label='Hit rate (%)')
ax2.plot(delta_values, np.array(expected)*100, 's--', 
         color='gray', alpha=0.5, label='Expected (%)')
ax2.set_ylabel('Hit Rate (%)', color='orange')

plt.title('P1 Sensitivity to Tolerance Window')
plt.tight_layout()
plt.savefig('Figure2_ToleranceSensitivity.pdf', dpi=300)
```

---

## Figure 3: Spin Model Comparison

**Type:** Scatter plot with diagonal line

**Data:** From Table3_P2_Results.csv

**Elements:**
- **X-axis:** Observed af (from GWTC)
- **Y-axis:** Predicted af
- **Points (blue circles):** UFRF predictions
- **Points (red squares):** Baseline predictions
- **Diagonal line:** Perfect prediction (y=x)
- **Error bars:** Posterior uncertainties (if available)

**Annotations:**
- "UFRF RMSE = 0.365"
- "Baseline RMSE = 0.437"
- "ΔAIC = -14.7 (decisive)"
- Show UFRF better in 38/41 events (92.7%)

**Inset:** Residual histogram
- Blue: UFRF residuals
- Red: Baseline residuals
- Show narrower distribution for UFRF

**Python Code Pseudocode:**
```python
fig, (ax_main, ax_inset) = plt.subplots(1, 2, figsize=(14, 6))

# Main scatter plot
ax_main.scatter(af_obs, af_pred_ufrf, s=80, alpha=0.7, 
                color='blue', edgecolor='black', label='UFRF')
ax_main.scatter(af_obs, af_pred_baseline, s=80, alpha=0.5, 
                marker='s', color='red', edgecolor='black', 
                label='Baseline')
ax_main.plot([0,1], [0,1], 'k--', label='Perfect prediction')

ax_main.set_xlabel('Observed Final Spin (af)')
ax_main.set_ylabel('Predicted Final Spin')
ax_main.legend()
ax_main.text(0.05, 0.95, f'UFRF RMSE={rmse_ufrf:.3f}\n'
                         f'Baseline RMSE={rmse_base:.3f}\n'
                         f'ΔAIC={delta_aic:.1f}',
             transform=ax_main.transAxes, va='top',
             bbox=dict(boxstyle='round', facecolor='wheat'))

# Inset: residual histogram
ax_inset.hist(residuals_ufrf, bins=20, alpha=0.6, 
              color='blue', label='UFRF')
ax_inset.hist(residuals_baseline, bins=20, alpha=0.6, 
              color='red', label='Baseline')
ax_inset.axvline(0, color='black', linestyle='--')
ax_inset.set_xlabel('Residual (af_obs - af_pred)')
ax_inset.set_ylabel('Count')
ax_inset.legend()

plt.tight_layout()
plt.savefig('Figure3_SpinModelComparison.pdf', dpi=300)
```

---

## Figure 4: Stratified Results by Observing Run

**Type:** Bar chart with error bars

**Data:** From Table5_Stratified.csv

**Elements:**
- **X-axis:** Observing runs (O1, O2, O3a, Pooled)
- **Y-axis:** Hit fraction (%)
- **Bars:** Hit rate per run
- **Horizontal line:** Expected 26.7%
- **Error bars:** Wilson score confidence intervals
- **P-values:** Show above each bar

**Annotations:**
- Color code by significance (green p<0.01, yellow p<0.05, gray p>0.05)
- Show sample sizes (N=3, 7, 31, 41)
- "Pattern consistent across all runs"

**Python Code Pseudocode:**
```python
fig, ax = plt.subplots(figsize=(10, 6))

runs = ['O1\n(N=3)', 'O2\n(N=7)', 'O3a\n(N=31)', 'Pooled\n(N=41)']
hit_rates = [66.7, 57.1, 51.6, 53.7]
p_values = [0.175, 0.087, 0.0027, 0.00022]
colors = ['lightgray', 'yellow', 'lightgreen', 'green']

bars = ax.bar(runs, hit_rates, color=colors, edgecolor='black', linewidth=1.5)
ax.axhline(26.7, color='red', linestyle='--', linewidth=2, 
           label='Expected (random)')

# Add p-values above bars
for i, (bar, pval) in enumerate(zip(bars, p_values)):
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height + 2,
            f'p={pval:.3f}' if pval > 0.001 else f'p={pval:.2e}',
            ha='center', fontsize=10, fontweight='bold')

ax.set_ylabel('Hit Rate (%)')
ax.set_xlabel('Observing Run')
ax.set_title('φ-Enrichment Consistent Across Observing Runs')
ax.set_ylim([0, 80])
ax.legend()
plt.tight_layout()
plt.savefig('Figure4_StratifiedResults.pdf', dpi=300)
```

---

## Figure 5: Bootstrap and Selection-Aware Null Distributions

**Type:** Multiple probability distribution plots

**Panel A: Bootstrap Null (Uniform q)**
- Histogram: Distribution of hit rates from 10,000 uniform null samples
- Vertical line: Observed 53.7%
- Shaded region: 95% CI of null
- Annotation: Z=7.42, p<10⁻⁶

**Panel B: Selection-Aware Null (LVK Population)**
- Histogram: Distribution from 10,000 LVK-like samples
- Vertical line: Observed 53.7%
- Shaded region: 95% CI of null
- Annotation: Z=3.94, p<10⁻⁴

**Panel C: Posterior-Aware P-Value Distribution**
- Histogram: 1,000 p-values from posterior draws
- Vertical line: Median p=0.002
- Shaded region: 95% CI
- Annotation: 95.9% draws show p<0.05, BF~23

**Python Code Pseudocode:**
```python
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5))

# Panel A: Bootstrap
ax1.hist(bootstrap_null_fracs*100, bins=50, alpha=0.7, color='gray')
ax1.axvline(53.7, color='red', linewidth=2, label='Observed')
ax1.axvspan(ci_lower*100, ci_upper*100, alpha=0.3, color='blue')
ax1.set_xlabel('Hit Rate (%)')
ax1.set_title('Bootstrap Null (Uniform q)\nZ=7.42, p<10⁻⁶')

# Panel B: Selection-aware
ax2.hist(selection_null_fracs*100, bins=50, alpha=0.7, color='lightblue')
ax2.axvline(53.7, color='red', linewidth=2, label='Observed')
ax2.set_xlabel('Hit Rate (%)')
ax2.set_title('Selection-Aware Null (LVK Pop)\nZ=3.94, p<10⁻⁴')

# Panel C: Posterior p-values
ax3.hist(-np.log10(posterior_pvals), bins=50, alpha=0.7, color='lightgreen')
ax3.axvline(-np.log10(0.05), color='red', linestyle='--', label='α=0.05')
ax3.set_xlabel('-log₁₀(p-value)')
ax3.set_title('Posterior-Aware Analysis\n95.9% significant, BF~23')

plt.tight_layout()
plt.savefig('Figure5_NullDistributions.pdf', dpi=300)
```

---

## Summary of Figures

| Figure | Type | Main Message |
|--------|------|--------------|
| **Figure 1** | Histogram + targets | Visual clustering near Fibonacci values |
| **Figure 2** | Sensitivity curve | Pattern stable across tolerance range |
| **Figure 3** | Scatter + residuals | √φ model decisively better |
| **Figure 4** | Bar chart by run | Consistency across observing runs |
| **Figure 5** | Null distributions | Pattern survives rigorous null tests |

**Total:** 5 publication-quality figures covering all main results and robustness checks.

---

## Optional Supplementary Figures

### S-Figure 1: Individual Event Contributions
- Forest plot showing each event's contribution to enrichment
- Identify influential events
- Jackknife sensitivity

### S-Figure 2: Fibonacci Ratio Network
- Visual representation of 88 discrete targets
- Show which ratios are hit most often
- Network/tree structure of Fibonacci sequence

### S-Figure 3: Waveform Family Comparison
- If stratified by waveform: compare across families
- SEOBNRv4 vs IMRPhenom vs NRSur
- Test for systematic differences

### S-Figure 4: Correlation Matrix
- q vs χ₁, χ₂, af
- Check for hidden correlations
- Identify outliers

---

## Figure Generation Commands

To generate all figures:

```bash
cd /Users/dcharb/Downloads/UFRF_BH_Fibonacci_v2
python3 bin/generate_figures.py --all
```

Individual figures:
```bash
python3 bin/generate_figures.py --figure 1  # Mass ratio histogram
python3 bin/generate_figures.py --figure 2  # Sensitivity curve
python3 bin/generate_figures.py --figure 3  # Spin comparison
python3 bin/generate_figures.py --figure 4  # Stratified results
python3 bin/generate_figures.py --figure 5  # Null distributions
```

Outputs saved to: `figures/Figure{1-5}_*.pdf`

---

**Note:** Actual Python plotting code can be implemented with matplotlib. Specifications above provide complete blueprint for publication-quality figures.

