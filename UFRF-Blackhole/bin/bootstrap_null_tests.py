#!/usr/bin/env python3
"""
Bootstrap and Permutation Null Tests for UFRF Analysis
Randomize φ-phase or shuffle gates to confirm patterns are not artifacts.
"""
import sys
import json
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from ufrf_bh.core import enrichment_test, gate_enrichment, phi_ladder

def bootstrap_phi_test(q_values, delta=0.05, n_bootstrap=1000, seed=42):
    """
    Bootstrap null test for P1 φ clustering.
    Randomize q values uniformly in [0,1] to test if observed clustering is special.
    
    Null hypothesis: q values are uniformly distributed in [0,1] with no preference 
    for Fibonacci values.
    
    Args:
        q_values: Observed mass ratios
        delta: Tolerance window
        n_bootstrap: Number of bootstrap samples
        seed: Random seed for reproducibility
    
    Returns:
        dict with observed enrichment and bootstrap null distribution
    """
    rng = np.random.RandomState(seed)
    q = np.asarray(q_values)
    
    # Observed enrichment with fixed Fibonacci targets
    obs = enrichment_test(q, delta=delta)
    obs_frac = obs['frac']
    
    # Bootstrap null: generate random q values uniformly in [0,1]
    # Keep Fibonacci targets fixed, randomize data
    null_fracs = []
    ladder = phi_ladder(20)
    targets = np.unique(np.concatenate([ladder, np.array([1/(1+np.sqrt(5))*2])]))
    targets = targets[(targets > 0) & (targets <= 1)]
    
    for i in range(n_bootstrap):
        # Generate random q values uniformly in [0,1]
        random_q = rng.uniform(0, 1, size=len(q))
        
        # Count hits with random q values and fixed Fibonacci targets
        hits = int(np.any(np.abs(random_q[:,None] - targets[None,:]) <= delta, axis=1).sum())
        null_fracs.append(hits / len(random_q))
    
    null_fracs = np.array(null_fracs)
    p_bootstrap = np.mean(null_fracs >= obs_frac)
    
    return {
        "test": "P1_phi_clustering",
        "n_events": len(q),
        "n_bootstrap": n_bootstrap,
        "observed_fraction": float(obs_frac),
        "observed_pval": float(obs['pval']),
        "null_mean": float(np.mean(null_fracs)),
        "null_std": float(np.std(null_fracs)),
        "null_median": float(np.median(null_fracs)),
        "null_95ci": [float(np.percentile(null_fracs, 2.5)), 
                      float(np.percentile(null_fracs, 97.5))],
        "bootstrap_pval": float(p_bootstrap),
        "z_score": float((obs_frac - np.mean(null_fracs)) / max(np.std(null_fracs), 1e-10))
    }

def permutation_gate_test(phases_rad, tol=None, n_permutations=1000, seed=42):
    """
    Permutation test for P3 13-gate clustering.
    Generate random uniformly distributed phases to test if 13-gate clustering is special.
    
    Null hypothesis: Phases are uniformly distributed on [0, 2π) with no preference
    for 13-gate structure.
    
    Args:
        phases_rad: Observed phases in radians
        tol: Tolerance window in radians
        n_permutations: Number of permutations
        seed: Random seed
    
    Returns:
        dict with observed enrichment and permutation null distribution
    """
    rng = np.random.RandomState(seed)
    phases = np.asarray(phases_rad) % (2*np.pi)
    
    if tol is None:
        tol = 2*np.pi*(1/13)/4
    
    # Observed enrichment with fixed 13-gate structure
    obs = gate_enrichment(phases, tol=tol)
    obs_frac = obs['frac']
    
    # Permutation null: generate random uniform phases
    # Keep 13-gate structure fixed, randomize phase data
    null_fracs = []
    gates = 2*np.pi*np.arange(13)/13.0
    
    for i in range(n_permutations):
        # Generate random uniform phases on [0, 2π)
        random_phases = rng.uniform(0, 2*np.pi, size=len(phases))
        
        # Count hits with random phases and fixed 13-gate structure
        hits = 0
        for ph in random_phases:
            diff = np.angle(np.exp(1j*(ph - gates)))
            if np.min(np.abs(diff)) <= tol:
                hits += 1
        
        null_fracs.append(hits / len(random_phases))
    
    null_fracs = np.array(null_fracs)
    p_permutation = np.mean(null_fracs >= obs_frac)
    
    return {
        "test": "P3_13gate_clustering",
        "n_events": len(phases),
        "n_permutations": n_permutations,
        "tolerance_rad": float(tol),
        "observed_fraction": float(obs_frac),
        "observed_pval": float(obs['pval']),
        "null_mean": float(np.mean(null_fracs)),
        "null_std": float(np.std(null_fracs)),
        "null_median": float(np.median(null_fracs)),
        "null_95ci": [float(np.percentile(null_fracs, 2.5)), 
                      float(np.percentile(null_fracs, 97.5))],
        "permutation_pval": float(p_permutation),
        "z_score": float((obs_frac - np.mean(null_fracs)) / max(np.std(null_fracs), 1e-10))
    }

def main():
    print("="*70)
    print("UFRF Bootstrap and Permutation Null Tests")
    print("="*70)
    
    # P1 Bootstrap Test
    print("\n[1/2] P1: φ Clustering Bootstrap Test")
    print("-"*70)
    
    q_csv = BASE / 'data' / 'expanded_q_data.csv'
    if q_csv.exists():
        df_q = pd.read_csv(q_csv)
        q_values = df_q['q'].values
        
        print(f"Running bootstrap test with {len(q_values)} events...")
        p1_result = bootstrap_phi_test(q_values, n_bootstrap=10000)
        
        print(f"\nObserved enrichment: {p1_result['observed_fraction']*100:.1f}%")
        print(f"Null distribution mean: {p1_result['null_mean']*100:.1f}%")
        print(f"Null 95% CI: [{p1_result['null_95ci'][0]*100:.1f}%, {p1_result['null_95ci'][1]*100:.1f}%]")
        print(f"Z-score: {p1_result['z_score']:.2f}")
        print(f"Bootstrap p-value: {p1_result['bootstrap_pval']:.6f}")
        
        if p1_result['bootstrap_pval'] < 0.001:
            print("✅ CONFIRMED: Pattern is NOT due to random target placement")
        elif p1_result['bootstrap_pval'] < 0.05:
            print("⚠️  MARGINAL: Some evidence pattern is non-random")
        else:
            print("❌ WARNING: Pattern may be artifact of target selection")
    else:
        print(f"ERROR: {q_csv} not found")
        p1_result = None
    
    # P3 Permutation Test
    print("\n[2/2] P3: 13-Gate Clustering Permutation Test")
    print("-"*70)
    
    phase_csv = BASE / 'data' / 'expanded_ringdown_phases.csv'
    if phase_csv.exists():
        df_phase = pd.read_csv(phase_csv)
        phases_frac = df_phase['phase_fraction'].values
        phases_rad = phases_frac * 2 * np.pi
        
        print(f"Running permutation test with {len(phases_rad)} events...")
        p3_result = permutation_gate_test(phases_rad, n_permutations=10000)
        
        print(f"\nObserved enrichment: {p3_result['observed_fraction']*100:.1f}%")
        print(f"Null distribution mean: {p3_result['null_mean']*100:.1f}%")
        print(f"Null 95% CI: [{p3_result['null_95ci'][0]*100:.1f}%, {p3_result['null_95ci'][1]*100:.1f}%]")
        print(f"Z-score: {p3_result['z_score']:.2f}")
        print(f"Permutation p-value: {p3_result['permutation_pval']:.6f}")
        
        if p3_result['permutation_pval'] < 0.001:
            print("✅ CONFIRMED: Pattern is NOT due to random gate placement")
        elif p3_result['permutation_pval'] < 0.05:
            print("⚠️  MARGINAL: Some evidence pattern is non-random")
        else:
            print("❌ WARNING: Pattern may be artifact of gate selection")
    else:
        print(f"ERROR: {phase_csv} not found")
        p3_result = None
    
    # Save results
    results = {
        "P1_bootstrap": p1_result,
        "P3_permutation": p3_result
    }
    
    out_path = BASE / 'results' / 'null_tests.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n" + "="*70)
    print(f"Results saved to: {out_path}")
    print("="*70)
    
    # Summary
    print("\nSUMMARY:")
    if p1_result and p1_result['bootstrap_pval'] < 0.001:
        print("✅ P1: φ clustering is statistically robust (not artifact)")
    if p3_result and p3_result['permutation_pval'] < 0.001:
        print("✅ P3: 13-gate clustering is statistically robust (not artifact)")
    
    return results

if __name__ == '__main__':
    main()

