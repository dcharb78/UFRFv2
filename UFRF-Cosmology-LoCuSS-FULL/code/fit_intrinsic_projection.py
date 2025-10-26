#!/usr/bin/env python3
"""
Fit intrinsic mass O* and projection factor S for each cluster
using all three techniques simultaneously
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.optimize import minimize
import json

def load_all_masses(data_dir="data"):
    """Load all mass measurements"""
    # Load WL
    wl = pd.read_csv(Path(data_dir) / "locuss_wl_m500.csv")
    wl = wl[['cluster_id', 'z', 'M500_WL', 'M500_WL_err']]
    
    # Load HSE
    hse = pd.read_csv(Path(data_dir) / "locuss_hse_m500.csv")
    hse = hse[['cluster_id', 'M500_HSE', 'M500_HSE_err']]
    
    # Load SZ
    sz = pd.read_csv(Path(data_dir) / "locuss_sz_m500.csv")
    sz = sz[['cluster_id', 'M500_SZ', 'M500_SZ_err']]
    
    # Merge all
    df = wl.merge(hse, on='cluster_id').merge(sz, on='cluster_id')
    
    return df

def fit_cluster_projection(row, alpha_dict, d_M=1.0):
    """
    Fit O* and S for a single cluster using all available techniques
    
    Model: ln(O_i) = ln(O*) + d_M * alpha_i * S + epsilon_i
    """
    # Collect available measurements
    measurements = []
    alphas = []
    weights = []
    
    for tech in ['WL', 'HSE', 'SZ']:
        m_col = f'M500_{tech}'
        e_col = f'M500_{tech}_err'
        
        if m_col in row and row[m_col] > 0:
            m = row[m_col]
            e = row[e_col] if e_col in row and row[e_col] > 0 else 0.2 * m
            
            measurements.append(np.log(m))
            alphas.append(alpha_dict[tech])
            weights.append(1.0 / (e/m)**2)
    
    if len(measurements) < 2:
        return np.nan, np.nan, np.nan, {}, {}
    
    measurements = np.array(measurements)
    alphas = np.array(alphas)
    weights = np.array(weights)
    
    # Objective function for least squares
    def objective(params):
        ln_O_star, S = params
        predicted = ln_O_star + d_M * alphas * S
        residuals = measurements - predicted
        weighted_sse = np.sum(weights * residuals**2)
        return weighted_sse
    
    # Initial guess: weighted mean of measurements and S=0
    ln_O_star_init = np.average(measurements, weights=weights)
    S_init = 0.0
    
    # Optimize
    result = minimize(objective, [ln_O_star_init, S_init], 
                     method='L-BFGS-B',
                     bounds=[(None, None), (-2, 2)])  # S bounded for stability
    
    ln_O_star, S = result.x
    O_star = np.exp(ln_O_star)
    
    # Calculate residuals
    predicted = ln_O_star + d_M * alphas * S
    residuals = measurements - predicted
    
    # Map residuals back to techniques
    residual_dict = {}
    for i, tech in enumerate(['WL', 'HSE', 'SZ']):
        if f'M500_{tech}' in row and row[f'M500_{tech}'] > 0:
            residual_dict[f'resid_{tech}'] = residuals[i] if i < len(residuals) else np.nan
        else:
            residual_dict[f'resid_{tech}'] = np.nan
    
    # Standard error of S (approximate)
    if len(measurements) > 2:
        # Use residual variance to estimate SE
        residual_var = np.sum(weights * residuals**2) / (len(measurements) - 2)
        # Approximate SE for S (simplified)
        SE_S = np.sqrt(residual_var / np.sum(weights * (alphas - np.mean(alphas))**2))
    else:
        SE_S = np.nan
    
    # Goodness of fit
    fit_stats = {
        'chi2': float(np.sum(weights * residuals**2)),
        'dof': len(measurements) - 2,
        'rmse': float(np.sqrt(np.mean(residuals**2)))
    }
    
    return ln_O_star, O_star, S, SE_S, residual_dict, fit_stats

def validate_projections(df_fit, alpha_dict, d_M=1.0):
    """
    Validate by projecting O* back to each technique
    """
    results = []
    
    for tech in ['WL', 'HSE', 'SZ']:
        m_col = f'M500_{tech}'
        
        # Filter to clusters with this measurement
        valid = df_fit[m_col] > 0
        df_tech = df_fit[valid].copy()
        
        if len(df_tech) == 0:
            continue
        
        # Predict using O* and S
        ln_pred = df_tech['ln_Ostar'] + d_M * alpha_dict[tech] * df_tech['S_hat']
        pred = np.exp(ln_pred)
        
        # Compare to actual
        actual = df_tech[m_col]
        log_residuals = np.log(actual) - ln_pred
        pct_errors = 100 * (pred - actual) / actual
        
        # Calculate metrics
        metrics = {
            'target': tech,
            'N': len(df_tech),
            'RMSE(log10)': np.sqrt(np.mean((log_residuals / np.log(10))**2)),
            'Bias(log10)': np.median(log_residuals) / np.log(10),
            'Median % err': np.median(np.abs(pct_errors)),
            'Mean % err': np.mean(pct_errors),
            'Std % err': np.std(pct_errors)
        }
        
        results.append(metrics)
    
    return pd.DataFrame(results)

def compute_pair_ratios(df):
    """
    Compute technique ratios for validation
    """
    ratios = {}
    
    # HSE/WL
    valid = (df['M500_HSE'] > 0) & (df['M500_WL'] > 0)
    if valid.sum() > 0:
        ratio = df.loc[valid, 'M500_HSE'] / df.loc[valid, 'M500_WL']
        ratios['HSE/WL'] = {
            'Median': np.median(ratio),
            'IQR_25': np.percentile(ratio, 25),
            'IQR_75': np.percentile(ratio, 75),
            'Mean': np.mean(ratio),
            'Std': np.std(ratio)
        }
    
    # SZ/WL
    valid = (df['M500_SZ'] > 0) & (df['M500_WL'] > 0)
    if valid.sum() > 0:
        ratio = df.loc[valid, 'M500_SZ'] / df.loc[valid, 'M500_WL']
        ratios['SZ/WL'] = {
            'Median': np.median(ratio),
            'IQR_25': np.percentile(ratio, 25),
            'IQR_75': np.percentile(ratio, 75),
            'Mean': np.mean(ratio),
            'Std': np.std(ratio)
        }
    
    # HSE/SZ
    valid = (df['M500_HSE'] > 0) & (df['M500_SZ'] > 0)
    if valid.sum() > 0:
        ratio = df.loc[valid, 'M500_HSE'] / df.loc[valid, 'M500_SZ']
        ratios['HSE/SZ'] = {
            'Median': np.median(ratio),
            'IQR_25': np.percentile(ratio, 25),
            'IQR_75': np.percentile(ratio, 75),
            'Mean': np.mean(ratio),
            'Std': np.std(ratio)
        }
    
    return pd.DataFrame(ratios).T

def compute_projection_per_cluster(df, alpha_dict):
    """
    Compute S estimates from each technique pair
    """
    results = []
    
    for _, row in df.iterrows():
        cluster_result = {'cluster_id': row['cluster_id'], 'z': row['z']}
        
        # HSE:WL
        if row['M500_HSE'] > 0 and row['M500_WL'] > 0:
            log_ratio = np.log(row['M500_HSE'] / row['M500_WL'])
            S_hse_wl = log_ratio / (alpha_dict['HSE'] - alpha_dict['WL'])
            cluster_result['S(HSE:WL)'] = S_hse_wl
        else:
            cluster_result['S(HSE:WL)'] = np.nan
        
        # SZ:WL
        if row['M500_SZ'] > 0 and row['M500_WL'] > 0:
            log_ratio = np.log(row['M500_SZ'] / row['M500_WL'])
            S_sz_wl = log_ratio / (alpha_dict['SZ'] - alpha_dict['WL'])
            cluster_result['S(SZ:WL)'] = S_sz_wl
        else:
            cluster_result['S(SZ:WL)'] = np.nan
        
        # HSE:SZ
        if row['M500_HSE'] > 0 and row['M500_SZ'] > 0:
            log_ratio = np.log(row['M500_HSE'] / row['M500_SZ'])
            S_hse_sz = log_ratio / (alpha_dict['HSE'] - alpha_dict['SZ'])
            cluster_result['S(HSE:SZ)'] = S_hse_sz
        else:
            cluster_result['S(HSE:SZ)'] = np.nan
        
        results.append(cluster_result)
    
    return pd.DataFrame(results)

def main():
    """Main execution"""
    print("="*60)
    print("Fitting Intrinsic Mass and Projection Factors")
    print("="*60)
    
    # Set alpha values
    alpha_dict = {
        'WL': 0.3,
        'SZ': 0.5,
        'HSE': 0.7
    }
    d_M = 1.0  # Can be absorbed into S
    
    # Load data
    print("\nLoading mass measurements...")
    df = load_all_masses()
    print(f"Loaded {len(df)} clusters")
    
    # Fit O* and S for each cluster
    print("\nFitting intrinsic mass and projection factor...")
    results = []
    fit_stats_all = []
    
    for _, row in df.iterrows():
        ln_O_star, O_star, S, SE_S, residuals, fit_stats = fit_cluster_projection(row, alpha_dict, d_M)
        
        result = {
            'cluster_id': row['cluster_id'],
            'z': row['z'],
            'ln_Ostar': ln_O_star,
            'Ostar': O_star,
            'S_hat': S,
            'SE(S_hat)': SE_S
        }
        result.update(residuals)
        results.append(result)
        
        # Store fit statistics
        fit_stats['cluster_id'] = row['cluster_id']
        fit_stats_all.append(fit_stats)
    
    df_fit = pd.DataFrame(results)
    
    # Merge back with original data for validation
    df_full = df.merge(df_fit, on=['cluster_id', 'z'])
    
    # Save intrinsic and projection fit
    output_file = "intrinsic_and_projection_fit.csv"
    df_fit.to_csv(output_file, index=False)
    print(f"\nSaved intrinsic mass fits to: {output_file}")
    
    # Print summary statistics
    valid_S = df_fit['S_hat'].notna()
    print(f"\nProjection factor S statistics:")
    print(f"  Mean: {df_fit.loc[valid_S, 'S_hat'].mean():.3f}")
    print(f"  Std:  {df_fit.loc[valid_S, 'S_hat'].std():.3f}")
    print(f"  Min:  {df_fit.loc[valid_S, 'S_hat'].min():.3f}")
    print(f"  Max:  {df_fit.loc[valid_S, 'S_hat'].max():.3f}")
    
    # Validate projections
    print("\nValidating projections...")
    validation_metrics = validate_projections(df_full, alpha_dict, d_M)
    validation_metrics.to_csv("projection_validation_metrics.csv", index=False)
    print("\nValidation metrics:")
    print(validation_metrics.to_string(index=False))
    
    # Compute pair ratios
    print("\nComputing technique ratios...")
    ratios = compute_pair_ratios(df)
    ratios.to_csv("Technique_Ratios_and_Projection_S__median_over_clusters_.csv")
    print(ratios)
    
    # Compute projection per cluster
    projection_per_cluster = compute_projection_per_cluster(df, alpha_dict)
    projection_per_cluster.to_csv("locuss_projection_per_cluster.csv", index=False)
    
    # Check correlation between S estimates
    print("\nCorrelation between S estimates from different pairs:")
    s_cols = ['S(HSE:WL)', 'S(SZ:WL)', 'S(HSE:SZ)']
    corr_matrix = projection_per_cluster[s_cols].corr()
    print(corr_matrix)
    
    # Save fit statistics
    df_fit_stats = pd.DataFrame(fit_stats_all)
    df_fit_stats.to_csv("fit_statistics.csv", index=False)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("Files created:")
    print("  - intrinsic_and_projection_fit.csv")
    print("  - projection_validation_metrics.csv")
    print("  - Technique_Ratios_and_Projection_S__median_over_clusters_.csv")
    print("  - locuss_projection_per_cluster.csv")
    print("  - fit_statistics.csv")
    print("="*60)

if __name__ == "__main__":
    main()
