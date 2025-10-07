#!/usr/bin/env python3
"""
Generate publication-ready tables for Extended Data.
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))

from ufrf_bh.core import phi_ladder, nearest_phi_distance, af_ufrf, af_baseline

def generate_table1_event_list():
    """Table 1: Complete event list with all parameters."""
    df_q = pd.read_csv(BASE / 'data' / 'gwtc_real_q.csv')
    df_spins = pd.read_csv(BASE / 'data' / 'gwtc_real_spins.csv')
    
    # Merge
    df = pd.merge(df_q, df_spins[['event', 'chi1', 'chi2', 'af']], on='event')
    
    # Add observing run
    def get_run(event):
        if event.startswith('GW15'): return 'O1'
        elif event.startswith('GW17'): return 'O2'
        elif event.startswith('GW19'): return 'O3a'
        else: return 'O3b'
    
    df['run'] = df['event'].apply(get_run)
    
    # Save
    out_path = BASE / 'results' / 'Table1_EventList.csv'
    df.to_csv(out_path, index=False)
    
    print(f"✅ Table 1 created: {out_path}")
    print(f"   {len(df)} events with m₁, m₂, q, χ₁, χ₂, af, observing run")
    
    return df

def generate_table2_p1_results():
    """Table 2: P1 results - which events hit Fibonacci targets."""
    df = pd.read_csv(BASE / 'results' / 'phi_analysis_from_csv.csv')
    
    # Add hit/miss indicator
    df['hit_delta_0.05'] = df['dist_to_nearest'] <= 0.05
    df['hit_delta_0.04'] = df['dist_to_nearest'] <= 0.04
    
    # Add which Fibonacci ratio they're near
    df['fibonacci_ratio_label'] = df['nearest_ratio'].apply(lambda x: f"{x:.6f}")
    
    # Sort by distance to nearest (closest first)
    df_sorted = df.sort_values('dist_to_nearest')
    
    out_path = BASE / 'results' / 'Table2_P1_Results.csv'
    df_sorted.to_csv(out_path, index=False)
    
    print(f"✅ Table 2 created: {out_path}")
    print(f"   P1 results per event with nearest Fibonacci ratio")
    print(f"   Hits at δ=0.05: {df['hit_delta_0.05'].sum()}/{len(df)}")
    print(f"   Hits at δ=0.04: {df['hit_delta_0.04'].sum()}/{len(df)}")
    
    # Print top 10 closest
    print("\n   Top 10 closest to Fibonacci ratios:")
    for idx, row in df_sorted.head(10).iterrows():
        print(f"     {row['event']}: q={row['q']:.4f} → {row['nearest_ratio']:.4f} (Δ={row['dist_to_nearest']:.4f})")
    
    return df_sorted

def generate_table3_p2_results():
    """Table 3: P2 results - model predictions and residuals."""
    df = pd.read_csv(BASE / 'results' / 'final_spin_predictions.csv')
    
    # Calculate residuals
    df['residual_ufrf'] = df['af'] - df['af_pred_ufrf']
    df['residual_baseline'] = df['af'] - df['af_pred_baseline']
    df['abs_error_ufrf'] = np.abs(df['residual_ufrf'])
    df['abs_error_baseline'] = np.abs(df['residual_baseline'])
    
    # Sort by UFRF performance (best predictions first)
    df_sorted = df.sort_values('abs_error_ufrf')
    
    out_path = BASE / 'results' / 'Table3_P2_Results.csv'
    df_sorted.to_csv(out_path, index=False)
    
    print(f"✅ Table 3 created: {out_path}")
    print(f"   P2 model predictions and residuals per event")
    print(f"   Mean |error| UFRF: {df['abs_error_ufrf'].mean():.4f}")
    print(f"   Mean |error| Baseline: {df['abs_error_baseline'].mean():.4f}")
    
    # Count where UFRF is better
    ufrf_better = (df['abs_error_ufrf'] < df['abs_error_baseline']).sum()
    print(f"   UFRF better: {ufrf_better}/{len(df)} events ({ufrf_better/len(df)*100:.1f}%)")
    
    return df_sorted

def generate_table4_sensitivity():
    """Table 4: Complete sensitivity analysis grid."""
    import json
    with open(BASE / 'results' / 'rigorous_analysis.json') as f:
        data = json.load(f)
    
    sensitivity = data['sensitivity_grid']
    
    rows = []
    for key, val in sensitivity.items():
        rows.append({
            'tolerance_delta': val['delta'],
            'hits': val['hits'],
            'hit_fraction': val['frac'],
            'expected_coverage': val['p0'],
            'enrichment_factor': val['frac'] / val['p0'] if val['p0'] > 0 else 0,
            'p_value': val['pval'],
            'neg_log10_p': -np.log10(val['pval']) if val['pval'] > 0 else np.inf
        })
    
    df = pd.DataFrame(rows).sort_values('tolerance_delta')
    
    out_path = BASE / 'results' / 'Table4_Sensitivity.csv'
    df.to_csv(out_path, index=False)
    
    print(f"✅ Table 4 created: {out_path}")
    print(f"   Sensitivity grid: δ ∈ [0.03, 0.08]")
    print(f"   All p-values < 0.05: {(df['p_value'] < 0.05).all()}")
    print(f"   Best δ={df.loc[df['p_value'].idxmin(), 'tolerance_delta']:.2f} with p={df['p_value'].min():.2e}")
    
    return df

def generate_table5_stratified():
    """Table 5: Stratified results by observing run."""
    import json
    with open(BASE / 'results' / 'rigorous_analysis.json') as f:
        data = json.load(f)
    
    strat = data['stratified_analysis']['by_run']
    
    rows = []
    for run in ['O1', 'O2', 'O3a']:
        if run in strat:
            val = strat[run]
            rows.append({
                'observing_run': run,
                'n_events': val['n_events'],
                'hits': val['hits'],
                'hit_fraction': val['frac'],
                'p_value': val['pval'],
                'neg_log10_p': -np.log10(val['pval']) if val['pval'] > 0 else np.inf
            })
    
    # Add pooled
    pooled = data['stratified_analysis']['pooled']
    rows.append({
        'observing_run': 'Pooled',
        'n_events': pooled['total_events'],
        'hits': pooled['total_hits'],
        'hit_fraction': pooled['pooled_frac'],
        'p_value': pooled['pooled_pval'],
        'neg_log10_p': -np.log10(pooled['pooled_pval']) if pooled['pooled_pval'] > 0 else np.inf
    })
    
    df = pd.DataFrame(rows)
    
    out_path = BASE / 'results' / 'Table5_Stratified.csv'
    df.to_csv(out_path, index=False)
    
    print(f"✅ Table 5 created: {out_path}")
    print(f"   Stratified analysis by observing run")
    print("\n   Results:")
    for _, row in df.iterrows():
        print(f"     {row['observing_run']:6s}: {row['hits']:2.0f}/{row['n_events']:2.0f} " +
              f"({row['hit_fraction']*100:4.1f}%) p={row['p_value']:.2e}")
    
    return df

def main():
    print("="*70)
    print("GENERATING PUBLICATION TABLES")
    print("="*70)
    print()
    
    # Generate all tables
    table1 = generate_table1_event_list()
    print()
    
    table2 = generate_table2_p1_results()
    print()
    
    table3 = generate_table3_p2_results()
    print()
    
    table4 = generate_table4_sensitivity()
    print()
    
    table5 = generate_table5_stratified()
    
    print()
    print("="*70)
    print("ALL TABLES CREATED")
    print("="*70)
    print("\nExtended Data Tables:")
    print("  • Table1_EventList.csv - All 41 events with parameters")
    print("  • Table2_P1_Results.csv - P1 Fibonacci clustering per event")
    print("  • Table3_P2_Results.csv - P2 model predictions & residuals")
    print("  • Table4_Sensitivity.csv - P1 tolerance sensitivity grid")
    print("  • Table5_Stratified.csv - Results by observing run")
    print("="*70)

if __name__ == '__main__':
    main()

