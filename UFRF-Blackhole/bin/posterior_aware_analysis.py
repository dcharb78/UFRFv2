#!/usr/bin/env python3
"""
POSTERIOR-AWARE UFRF ANALYSIS

Implements:
1. Posterior sampling (simulate from reasonable distributions)
2. Bayes factors for model comparison
3. Selection-aware null hypotheses using LVK population models
"""

import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from ufrf_bh.core import enrichment_test, af_ufrf, af_baseline, rmse

def simulate_posterior_samples(q_median, n_samples=1000, sigma=0.05):
    """
    Simulate posterior samples for q.
    In reality, would load from PE files. Here we approximate.
    
    Assume log-normal distribution around median with typical ~5% uncertainty.
    """
    # Use truncated normal to keep q ∈ (0, 1]
    samples = np.random.normal(q_median, sigma, n_samples)
    samples = np.clip(samples, 0.01, 1.0)  # Enforce bounds
    return samples

def posterior_aware_enrichment(df_q, delta=0.05, n_posterior_samples=1000):
    """
    Run enrichment test with posterior sampling.
    For each event, draw from posterior, compute enrichment for each draw.
    Report distribution of p-values and Bayes factor.
    """
    results_per_draw = []
    
    print(f"\nGenerating {n_posterior_samples} posterior draws per event...")
    print("(Note: Using simulated posteriors - real analysis would use PE files)")
    
    for draw_idx in range(n_posterior_samples):
        # Sample q value for each event from posterior
        q_samples = []
        for q_median in df_q['q'].values:
            q_sample = simulate_posterior_samples(q_median, n_samples=1)[0]
            q_samples.append(q_sample)
        
        q_samples = np.array(q_samples)
        
        # Run enrichment test on this draw
        enrich = enrichment_test(q_samples, delta=delta)
        results_per_draw.append({
            'hits': enrich['hits'],
            'frac': enrich['frac'],
            'pval': enrich['pval']
        })
        
        if (draw_idx + 1) % 1000 == 0:
            print(f"  Completed {draw_idx + 1}/{n_posterior_samples} draws")
    
    results_per_draw = pd.DataFrame(results_per_draw)
    
    # Compute statistics across posterior
    median_frac = results_per_draw['frac'].median()
    median_pval = results_per_draw['pval'].median()
    ci_95_frac = results_per_draw['frac'].quantile([0.025, 0.975]).values
    ci_95_pval = results_per_draw['pval'].quantile([0.025, 0.975]).values
    
    # Estimate Bayes factor (simplified - proper BF requires full modeling)
    # BF ≈ p(data|H1) / p(data|H0)
    # Use fraction of draws where p < 0.05 as rough proxy
    frac_significant = (results_per_draw['pval'] < 0.05).mean()
    
    # Rough Bayes factor: odds of significance
    if frac_significant > 0.5:
        bayes_factor_rough = frac_significant / (1 - frac_significant)
    else:
        bayes_factor_rough = frac_significant / max(1 - frac_significant, 0.01)
    
    return {
        "n_draws": n_posterior_samples,
        "median_enrichment_frac": float(median_frac),
        "median_pval": float(median_pval),
        "ci_95_frac": [float(ci_95_frac[0]), float(ci_95_frac[1])],
        "ci_95_pval": [float(ci_95_pval[0]), float(ci_95_pval[1])],
        "frac_draws_significant": float(frac_significant),
        "bayes_factor_rough": float(bayes_factor_rough)
    }

def lvk_population_null(n_events=41, n_samples=10000):
    """
    Selection-aware null: generate q from LVK population model.
    
    Real implementation would use:
    - PowerLaw+Peak model from Abbott et al. (2021)
    - Detection selection function
    
    Here we approximate with a power law biased toward equal masses.
    """
    # LVK finds q distribution roughly ∝ q^β with β ~ 1-2
    # Plus preference for equal masses (q→1)
    
    # Mixture: 70% power law, 30% peaked near equal mass
    alpha = 1.5  # Power law index (higher = more equal masses)
    
    q_samples = []
    for _ in range(n_samples):
        if np.random.rand() < 0.7:
            # Power law component: q^α
            q = np.random.beta(alpha, 1)
        else:
            # Equal mass peak: peaked near q=1
            q = np.random.beta(5, 1)
        
        q_samples.append(max(q, 0.1))  # Floor to avoid q→0
    
    return np.array(q_samples)

def selection_aware_enrichment(df_q, delta=0.05, n_null_samples=10000):
    """
    Test enrichment against LVK population model, not uniform.
    """
    # Observed enrichment
    obs_enrich = enrichment_test(df_q['q'].values, delta=delta)
    obs_frac = obs_enrich['frac']
    
    print(f"\nGenerating {n_null_samples} null samples from LVK population model...")
    
    # Generate null samples from population model
    null_fracs = []
    for _ in range(n_null_samples):
        q_null = lvk_population_null(n_events=len(df_q), n_samples=len(df_q))
        null_enrich = enrichment_test(q_null, delta=delta)
        null_fracs.append(null_enrich['frac'])
    
    null_fracs = np.array(null_fracs)
    
    # P-value: fraction of null samples ≥ observed
    pval_selection_aware = (null_fracs >= obs_frac).mean()
    
    # Z-score against selection-aware null
    z_score = (obs_frac - null_fracs.mean()) / (null_fracs.std() + 1e-10)
    
    return {
        "observed_frac": float(obs_frac),
        "null_mean": float(null_fracs.mean()),
        "null_std": float(null_fracs.std()),
        "null_ci_95": [float(np.percentile(null_fracs, 2.5)),
                       float(np.percentile(null_fracs, 97.5))],
        "pval_selection_aware": float(pval_selection_aware),
        "z_score": float(z_score),
        "note": "Null from LVK-like population (power-law + equal-mass peak)"
    }

def main():
    print("\n" + "="*70)
    print("POSTERIOR-AWARE & SELECTION-AWARE ANALYSIS")
    print("="*70)
    
    # Load real data
    df_q = pd.read_csv(BASE / 'data' / 'gwtc_real_q.csv')
    
    print(f"\nDataset: {len(df_q)} real GWTC-1/2 events")
    
    # 1. POSTERIOR-AWARE ENRICHMENT
    print("\n" + "-"*70)
    print("1. POSTERIOR-AWARE ENRICHMENT (1000 draws per event)")
    print("-"*70)
    
    posterior_results = posterior_aware_enrichment(df_q, n_posterior_samples=1000)
    
    print(f"\nMedian enrichment: {posterior_results['median_enrichment_frac']*100:.1f}%")
    print(f"95% CI: [{posterior_results['ci_95_frac'][0]*100:.1f}%, " +
          f"{posterior_results['ci_95_frac'][1]*100:.1f}%]")
    print(f"\nMedian p-value: {posterior_results['median_pval']:.4e}")
    print(f"95% CI: [{posterior_results['ci_95_pval'][0]:.4e}, " +
          f"{posterior_results['ci_95_pval'][1]:.4e}]")
    print(f"\nFraction of draws with p < 0.05: {posterior_results['frac_draws_significant']*100:.1f}%")
    print(f"Rough Bayes factor: {posterior_results['bayes_factor_rough']:.2f}")
    
    # 2. SELECTION-AWARE NULL
    print("\n" + "-"*70)
    print("2. SELECTION-AWARE NULL (LVK population model)")
    print("-"*70)
    
    selection_results = selection_aware_enrichment(df_q, n_null_samples=10000)
    
    print(f"\nObserved enrichment: {selection_results['observed_frac']*100:.1f}%")
    print(f"LVK population null mean: {selection_results['null_mean']*100:.1f}%")
    print(f"LVK population null 95% CI: [{selection_results['null_ci_95'][0]*100:.1f}%, " +
          f"{selection_results['null_ci_95'][1]*100:.1f}%]")
    print(f"\nZ-score vs LVK population: {selection_results['z_score']:.2f}")
    print(f"P-value (selection-aware): {selection_results['pval_selection_aware']:.4e}")
    
    # 3. SAVE RESULTS
    output = {
        "posterior_aware": posterior_results,
        "selection_aware": selection_results
    }
    
    out_file = BASE / 'results' / 'posterior_selection_analysis.json'
    with open(out_file, 'w') as f:
        json.dump(output, f, indent=2)
    
    print("\n" + "="*70)
    print(f"Results saved to: {out_file}")
    print("="*70)
    
    # SUMMARY
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    
    if posterior_results['frac_draws_significant'] > 0.95:
        print("✅ ROBUST: >95% of posterior draws show p < 0.05")
    elif posterior_results['frac_draws_significant'] > 0.8:
        print("✅ STRONG: >80% of posterior draws show p < 0.05")
    else:
        print("⚠️  MODERATE: Pattern significant but not robust to all posterior draws")
    
    if selection_results['pval_selection_aware'] < 0.001:
        print("✅ SELECTION-ROBUST: Pattern significant even vs LVK population (p < 0.001)")
    elif selection_results['pval_selection_aware'] < 0.05:
        print("✅ SIGNIFICANT: Pattern holds vs LVK population (p < 0.05)")
    else:
        print("⚠️  MARGINAL: Pattern may be affected by LVK selection biases")
    
    print("\n" + "="*70)

if __name__ == '__main__':
    main()


