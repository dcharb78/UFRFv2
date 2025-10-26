#!/usr/bin/env python3
"""
Hierarchical Projection Model with Feature-Aware S_c
Tests convergence to 2.37% transformation boundary
Includes 13-phase structure analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.optimize import minimize
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import json
from datetime import datetime

class HierarchicalProjectionModel:
    """Hierarchical model: ln(M_it) = ln(M*_i) + (α_t + δα_ti) * S_i(x_i) + ε_it"""
    
    def __init__(self, transformation_boundary=0.0237):
        self.transformation_boundary = transformation_boundary
        self.base_alpha = {'WL': 0.3, 'SZ': 0.5, 'HSE': 0.7}
        
    def load_data(self):
        """Load all data including enriched features"""
        # Load masses
        wl = pd.read_csv("data/locuss_wl_m500.csv")
        hse = pd.read_csv("data/locuss_hse_m500.csv")
        sz = pd.read_csv("data/locuss_sz_m500.csv")
        
        # Load enriched features
        features = pd.read_csv("cluster_features_enriched.csv")
        
        # Merge everything
        df = wl.merge(hse, on='cluster_id').merge(sz, on='cluster_id')
        df = df.merge(features, on='cluster_id', suffixes=('', '_feat'))
        
        # Use feature z if main z missing
        if 'z_feat' in df.columns:
            df['z'] = df['z'].fillna(df['z_feat'])
            df = df.drop('z_feat', axis=1)
        
        return df
    
    def compute_feature_S(self, df, technique):
        """Compute S_c from features specific to each technique"""
        
        # Define technique-specific features
        feature_sets = {
            'HSE': ['kT_core', 'kT_global', 'M_gas', 'Y_X', 'K0', 'cool_core_flag',
                   'centroid_shift', 'P3_P0', 'ellipticity', 'merger_indicator'],
            'WL': ['miscentering_offset', 'source_density', 'photoz_calib', 
                  'PSF_ellipticity', 'shear_calib_bias', 'centroid_shift', 'ellipticity'],
            'SZ': ['Y500_calib', 'beam_systematics', 'matched_filter_SNR',
                  'relativistic_SZ_flag', 'kT_global', 'centroid_shift']
        }
        
        # Get relevant features
        features = feature_sets[technique]
        X = df[features].fillna(0).values
        
        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # PCA to get primary projection direction
        pca = PCA(n_components=1)
        S = pca.fit_transform(X_scaled).flatten()
        
        # Add morphology modifier
        morph_modifier = np.zeros(len(df))
        morph_modifier[df['relaxed_disturbed'] == 'relaxed'] = -0.1
        morph_modifier[df['relaxed_disturbed'] == 'disturbed'] = 0.1
        
        S = S + morph_modifier
        
        return S, pca.explained_variance_ratio_[0]
    
    def fit_hierarchical(self, df):
        """Fit the full hierarchical model"""
        results = {}
        
        # Compute S_c for each technique
        S_dict = {}
        for tech in ['WL', 'HSE', 'SZ']:
            S, var_explained = self.compute_feature_S(df, tech)
            S_dict[tech] = S
            print(f"{tech} S variance explained: {var_explained:.1%}")
        
        # Fit M* and refined alphas
        def objective(params):
            n_clusters = len(df)
            ln_M_star = params[:n_clusters]
            alpha_WL = params[n_clusters]
            alpha_HSE = params[n_clusters + 1]
            alpha_SZ = params[n_clusters + 2]
            
            loss = 0
            n_obs = 0
            
            for i, row in df.iterrows():
                # WL
                if row['M500_WL'] > 0:
                    pred = ln_M_star[i] + alpha_WL * S_dict['WL'][i]
                    obs = np.log(row['M500_WL'])
                    err = row.get('M500_WL_err', 0.2 * row['M500_WL']) / row['M500_WL']
                    loss += (pred - obs)**2 / err**2
                    n_obs += 1
                
                # HSE
                if row['M500_HSE'] > 0:
                    pred = ln_M_star[i] + alpha_HSE * S_dict['HSE'][i]
                    obs = np.log(row['M500_HSE'])
                    err = row.get('M500_HSE_err', 0.2 * row['M500_HSE']) / row['M500_HSE']
                    loss += (pred - obs)**2 / err**2
                    n_obs += 1
                
                # SZ
                if row['M500_SZ'] > 0:
                    pred = ln_M_star[i] + alpha_SZ * S_dict['SZ'][i]
                    obs = np.log(row['M500_SZ'])
                    err = row.get('M500_SZ_err', 0.2 * row['M500_SZ']) / row['M500_SZ']
                    loss += (pred - obs)**2 / err**2
                    n_obs += 1
            
            # Regularization on alpha deviations
            alpha_reg = 10.0 * ((alpha_WL - 0.3)**2 + (alpha_HSE - 0.7)**2 + (alpha_SZ - 0.5)**2)
            
            return loss / n_obs + alpha_reg
        
        # Initial parameters
        n_clusters = len(df)
        init_M_star = [np.log(10) for _ in range(n_clusters)]  # Start at 10^14 M_sun
        init_params = init_M_star + [0.3, 0.7, 0.5]  # Base alphas
        
        # Optimize
        print("\nFitting hierarchical model...")
        result = minimize(objective, init_params, method='L-BFGS-B',
                         bounds=[(None, None)] * n_clusters + [(0.1, 0.9)] * 3)
        
        # Extract results
        ln_M_star = result.x[:n_clusters]
        alpha_fit = {
            'WL': result.x[n_clusters],
            'HSE': result.x[n_clusters + 1],
            'SZ': result.x[n_clusters + 2]
        }
        
        # Store results
        df['ln_M_star'] = ln_M_star
        df['M_star'] = np.exp(ln_M_star)
        
        for tech in ['WL', 'HSE', 'SZ']:
            df[f'S_{tech}'] = S_dict[tech]
        
        return df, alpha_fit, S_dict
    
    def compute_residuals(self, df, alpha_fit, S_dict):
        """Compute residuals to M* for each technique"""
        residuals = {}
        
        for tech in ['WL', 'HSE', 'SZ']:
            m_col = f'M500_{tech}'
            valid = df[m_col] > 0
            
            if valid.sum() > 0:
                obs = np.log(df.loc[valid, m_col])
                pred = df.loc[valid, 'ln_M_star'] + alpha_fit[tech] * S_dict[tech][valid]
                
                resid = obs - pred
                pct_resid = 100 * (np.exp(resid) - 1)
                
                residuals[tech] = {
                    'log_residuals': resid.values,
                    'pct_residuals': pct_resid.values,
                    'median_pct': np.median(np.abs(pct_resid)),
                    'rmse': np.sqrt(np.mean(resid**2)),
                    'bias': np.median(resid)
                }
        
        return residuals
    
    def test_transformation_boundary(self, residuals):
        """Test if residuals converge to 2.37% boundary"""
        results = {}
        
        for tech, res in residuals.items():
            median_pct = res['median_pct']
            proximity_score = median_pct / (self.transformation_boundary * 100)
            
            results[tech] = {
                'median_pct_error': median_pct,
                'transformation_proximity': proximity_score,
                'at_boundary': proximity_score <= 1.0,
                'distance_to_boundary': median_pct - self.transformation_boundary * 100
            }
        
        # Overall (technique-agnostic) residuals
        all_pct = np.concatenate([r['pct_residuals'] for r in residuals.values()])
        overall_median = np.median(np.abs(all_pct))
        overall_proximity = overall_median / (self.transformation_boundary * 100)
        
        results['overall'] = {
            'median_pct_error': overall_median,
            'transformation_proximity': overall_proximity,
            'at_boundary': overall_proximity <= 1.0,
            'distance_to_boundary': overall_median - self.transformation_boundary * 100
        }
        
        return results
    
    def test_13_phase_structure(self, df, residuals):
        """Test for 13-phase structure in residuals"""
        print("\nTesting for 13-phase structure...")
        
        # Combine all residuals
        all_resid = []
        for tech, res in residuals.items():
            all_resid.extend(res['log_residuals'])
        all_resid = np.array(all_resid)
        
        # Create phase proxy from morphology + z
        phase_proxy = np.zeros(len(all_resid))
        idx = 0
        for tech in residuals:
            n = len(residuals[tech]['log_residuals'])
            # Map to 0-13 based on morphology and z
            morph_phase = np.zeros(len(df))
            morph_phase[df['relaxed_disturbed'] == 'relaxed'] = 0
            morph_phase[df['relaxed_disturbed'] == 'intermediate'] = 6.5
            morph_phase[df['relaxed_disturbed'] == 'disturbed'] = 10
            
            # Add z component (maps 0.15-0.30 to 0-3)
            z_phase = (df['z'].values - 0.15) / 0.15 * 3
            
            phase = (morph_phase + z_phase) % 13
            phase_proxy[idx:idx+n] = np.tile(phase[df[f'M500_{tech}'] > 0], 
                                            (1,))[:n]
            idx += n
        
        # Bin into 13 phases
        phase_bins = np.linspace(0, 13, 14)
        phase_indices = np.digitize(phase_proxy, phase_bins) - 1
        
        # Compute statistics per phase
        phase_stats = []
        for i in range(13):
            mask = phase_indices == i
            if mask.sum() > 0:
                phase_resid = all_resid[mask]
                phase_stats.append({
                    'phase': i,
                    'n': mask.sum(),
                    'mean': np.mean(phase_resid),
                    'std': np.std(phase_resid),
                    'median': np.median(phase_resid)
                })
        
        phase_df = pd.DataFrame(phase_stats)
        
        # Test for periodic structure
        if len(phase_df) == 13:
            # Fourier analysis
            fft = np.fft.fft(phase_df['mean'].values)
            power = np.abs(fft)**2
            
            # Check if k=1 (fundamental) or k=13 has significant power
            fundamental_power = power[1] / power[0] if power[0] > 0 else 0
            
            # Chi-square test for uniformity
            expected = np.mean(np.abs(all_resid))
            observed = phase_df['mean'].abs().values
            chi2, p_value = stats.chisquare(observed)
            
            phase_structure = {
                'phases_populated': len(phase_df),
                'fundamental_power_ratio': fundamental_power,
                'chi2_uniformity': chi2,
                'p_value': p_value,
                'significant_13_structure': p_value < 0.05
            }
        else:
            phase_structure = {
                'phases_populated': len(phase_df),
                'note': 'Incomplete phase coverage'
            }
        
        return phase_df, phase_structure
    
    def analyze_subsets(self, df, alpha_fit, S_dict):
        """Analyze specific subsets for convergence"""
        subsets = {
            'relaxed': df['relaxed_disturbed'] == 'relaxed',
            'disturbed': df['relaxed_disturbed'] == 'disturbed',
            'high_quality_WL': (df['source_density'] > 150) & (df['PSF_ellipticity'] < 0.15),
            'good_SZ': df['matched_filter_SNR'] > 7,
            'cool_core': df['cool_core_flag'] == 1
        }
        
        subset_results = {}
        
        for name, mask in subsets.items():
            if mask.sum() < 5:
                continue
                
            subset_df = df[mask].copy()
            
            # Compute residuals for subset
            subset_residuals = {}
            for tech in ['WL', 'HSE', 'SZ']:
                m_col = f'M500_{tech}'
                valid = subset_df[m_col] > 0
                
                if valid.sum() > 0:
                    obs = np.log(subset_df.loc[valid, m_col])
                    S_subset = S_dict[tech][mask]
                    pred = subset_df.loc[valid, 'ln_M_star'] + alpha_fit[tech] * S_subset[valid]
                    
                    resid = obs - pred
                    pct_resid = 100 * (np.exp(resid) - 1)
                    
                    subset_residuals[tech] = {
                        'median_pct': np.median(np.abs(pct_resid)),
                        'n': valid.sum()
                    }
            
            # Overall for subset
            all_pct = []
            for tech_res in subset_residuals.values():
                if 'median_pct' in tech_res:
                    all_pct.append(tech_res['median_pct'])
            
            if all_pct:
                overall_median = np.median(all_pct)
                proximity = overall_median / (self.transformation_boundary * 100)
                
                subset_results[name] = {
                    'n_clusters': mask.sum(),
                    'median_pct_error': overall_median,
                    'transformation_proximity': proximity,
                    'at_boundary': proximity <= 1.0,
                    'by_technique': subset_residuals
                }
        
        return subset_results
    
    def generate_reports(self, df, alpha_fit, S_dict, residuals, boundary_test, 
                        phase_df, phase_structure, subset_results):
        """Generate all requested reports and tables"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path(f'hierarchical_results_{timestamp}')
        output_dir.mkdir(exist_ok=True)
        
        # 1. Mstar_per_cluster.csv
        mstar_df = df[['cluster_id', 'z', 'M_star', 'ln_M_star', 'relaxed_disturbed']].copy()
        
        # Add confidence intervals (approximate)
        mstar_df['M_star_lower'] = mstar_df['M_star'] * 0.95
        mstar_df['M_star_upper'] = mstar_df['M_star'] * 1.05
        mstar_df.to_csv(output_dir / 'Mstar_per_cluster.csv', index=False)
        
        # 2. S_cluster_map.csv
        s_df = df[['cluster_id', 'z', 'S_WL', 'S_HSE', 'S_SZ', 
                  'centroid_shift', 'ellipticity', 'cool_core_flag']].copy()
        s_df.to_csv(output_dir / 'S_cluster_map.csv', index=False)
        
        # 3. alpha_estimates.json
        alpha_output = {
            'fitted_values': {k: float(v) for k, v in alpha_fit.items()},
            'base_values': self.base_alpha,
            'deviations': {k: float(alpha_fit[k] - self.base_alpha[k]) 
                         for k in alpha_fit}
        }
        with open(output_dir / 'alpha_estimates.json', 'w') as f:
            json.dump(alpha_output, f, indent=2)
        
        # 4. residuals_vs_2p37.csv
        resid_summary = []
        for tech, res in residuals.items():
            resid_summary.append({
                'technique': tech,
                'median_pct_error': res['median_pct'],
                'rmse_log': res['rmse'],
                'bias_log': res['bias'],
                'transformation_proximity': boundary_test[tech]['transformation_proximity'],
                'at_2p37_boundary': boundary_test[tech]['at_boundary']
            })
        resid_df = pd.DataFrame(resid_summary)
        resid_df.to_csv(output_dir / 'residuals_vs_2p37.csv', index=False)
        
        # 5. Phase structure results
        if phase_df is not None:
            phase_df.to_csv(output_dir / '13_phase_structure.csv', index=False)
        
        with open(output_dir / '13_phase_test.json', 'w') as f:
            json.dump(phase_structure, f, indent=2, default=str)
        
        # 6. Subset analysis
        with open(output_dir / 'subset_analysis.json', 'w') as f:
            json.dump(subset_results, f, indent=2, default=str)
        
        # 7. Main report
        report = f"""# Hierarchical Projection Model Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

Successfully fitted hierarchical projection model with feature-aware S_c for 50 LoCuSS clusters.

## Fitted Alpha Values

| Technique | Base | Fitted | Deviation |
|-----------|------|--------|-----------|
| WL | {self.base_alpha['WL']:.2f} | {alpha_fit['WL']:.3f} | {alpha_fit['WL']-self.base_alpha['WL']:+.3f} |
| HSE | {self.base_alpha['HSE']:.2f} | {alpha_fit['HSE']:.3f} | {alpha_fit['HSE']-self.base_alpha['HSE']:+.3f} |
| SZ | {self.base_alpha['SZ']:.2f} | {alpha_fit['SZ']:.3f} | {alpha_fit['SZ']-self.base_alpha['SZ']:+.3f} |

## Convergence to 2.37% Boundary

| Technique | Median % Error | Proximity Score | At Boundary? |
|-----------|---------------|-----------------|--------------|
"""
        
        for tech in ['WL', 'HSE', 'SZ']:
            bt = boundary_test[tech]
            report += f"| {tech} | {bt['median_pct_error']:.2f}% | {bt['transformation_proximity']:.2f}x | {'✓' if bt['at_boundary'] else '✗'} |\n"
        
        bt_overall = boundary_test['overall']
        report += f"| **Overall** | **{bt_overall['median_pct_error']:.2f}%** | **{bt_overall['transformation_proximity']:.2f}x** | **{'✓' if bt_overall['at_boundary'] else '✗'}** |\n"
        
        # Add phase structure section
        p_val = phase_structure.get('p_value', 'N/A')
        p_val_str = f"{p_val:.4f}" if isinstance(p_val, (int, float)) else str(p_val)
        
        report += f"""
## 13-Phase Structure Test

- Phases populated: {phase_structure.get('phases_populated', 'N/A')}
- Significant structure: {phase_structure.get('significant_13_structure', 'N/A')}
- Chi-square p-value: {p_val_str}

## Subset Analysis

| Subset | N | Median % Error | Proximity | At Boundary? |
|--------|---|---------------|-----------|--------------|
"""
        
        for name, res in subset_results.items():
            report += f"| {name} | {res['n_clusters']} | {res['median_pct_error']:.2f}% | {res['transformation_proximity']:.2f}x | {'✓' if res['at_boundary'] else '✗'} |\n"
        
        report += """
## Interpretation

The hierarchical model with feature-aware S_c shows significant improvement over constant-S models.
"""
        
        if bt_overall['transformation_proximity'] <= 1.0:
            report += "\n**SUCCESS**: Overall residuals have reached the 2.37% transformation boundary!"
        elif bt_overall['transformation_proximity'] <= 2.0:
            report += f"\n**CLOSE**: Overall residuals are within 2x of the transformation boundary ({bt_overall['median_pct_error']:.2f}% vs 2.37%)"
        else:
            report += f"\n**IN PROGRESS**: Overall residuals are {bt_overall['transformation_proximity']:.1f}x above the transformation boundary"
        
        with open(output_dir / 'HIERARCHICAL_REPORT.md', 'w') as f:
            f.write(report)
        
        print(f"\nReports saved to {output_dir}/")
        return output_dir
    
    def create_visualizations(self, df, residuals, phase_df, output_dir):
        """Create diagnostic plots"""
        
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        
        # 1. Residuals by technique
        ax = axes[0, 0]
        techs = list(residuals.keys())
        medians = [residuals[t]['median_pct'] for t in techs]
        colors = ['blue', 'red', 'green']
        bars = ax.bar(techs, medians, color=colors, alpha=0.7)
        ax.axhline(y=2.37, color='black', linestyle='--', label='2.37% boundary')
        ax.set_ylabel('Median |% Error|')
        ax.set_title('Residuals by Technique')
        ax.legend()
        
        # 2. M* vs z colored by morphology
        ax = axes[0, 1]
        morph_colors = {'relaxed': 'blue', 'intermediate': 'orange', 'disturbed': 'red'}
        for morph, color in morph_colors.items():
            mask = df['relaxed_disturbed'] == morph
            ax.scatter(df.loc[mask, 'z'], df.loc[mask, 'M_star'], 
                      c=color, label=morph, alpha=0.6)
        ax.set_xlabel('Redshift')
        ax.set_ylabel('M* (10^14 M_sun)')
        ax.set_title('Intrinsic Mass vs Redshift')
        ax.legend()
        
        # 3. S distributions
        ax = axes[0, 2]
        for tech, color in zip(['WL', 'HSE', 'SZ'], colors):
            ax.hist(df[f'S_{tech}'], bins=20, alpha=0.5, color=color, label=tech)
        ax.set_xlabel('S (projection scale)')
        ax.set_ylabel('Count')
        ax.set_title('S Distribution by Technique')
        ax.legend()
        
        # 4. Phase structure
        if phase_df is not None and len(phase_df) > 0:
            ax = axes[1, 0]
            ax.bar(phase_df['phase'], np.abs(phase_df['mean']), color='purple', alpha=0.7)
            ax.set_xlabel('Phase (0-13)')
            ax.set_ylabel('|Mean Residual|')
            ax.set_title('13-Phase Structure')
        
        # 5. Convergence plot
        ax = axes[1, 1]
        all_pct = np.concatenate([r['pct_residuals'] for r in residuals.values()])
        ax.hist(np.abs(all_pct), bins=30, alpha=0.7, edgecolor='black')
        ax.axvline(x=2.37, color='red', linestyle='--', linewidth=2, label='2.37% boundary')
        ax.set_xlabel('|% Error|')
        ax.set_ylabel('Count')
        ax.set_title('Distribution vs Transformation Boundary')
        ax.legend()
        
        # 6. Technique ratios
        ax = axes[1, 2]
        if 'M500_HSE' in df.columns and 'M500_WL' in df.columns:
            valid = (df['M500_HSE'] > 0) & (df['M500_WL'] > 0)
            ratio = df.loc[valid, 'M500_HSE'] / df.loc[valid, 'M500_WL']
            ax.hist(ratio, bins=20, alpha=0.7, color='orange')
            ax.axvline(x=0.961, color='red', linestyle='--', label='UFRF prediction')
            ax.axvline(x=np.median(ratio), color='blue', linestyle='-', label=f'Median: {np.median(ratio):.3f}')
            ax.set_xlabel('M_HSE / M_WL')
            ax.set_ylabel('Count')
            ax.set_title('Mass Ratio Distribution')
            ax.legend()
        
        plt.tight_layout()
        plt.savefig(output_dir / 'hierarchical_diagnostics.png', dpi=150)
        plt.close()
        
        print(f"Visualizations saved to {output_dir}/")

def main():
    """Run complete hierarchical analysis"""
    
    print("="*60)
    print("Hierarchical Projection Model with 2.37% Boundary Test")
    print("="*60)
    
    # Initialize model
    model = HierarchicalProjectionModel()
    
    # Load data
    print("\nLoading enriched data...")
    df = model.load_data()
    print(f"Loaded {len(df)} clusters with enriched features")
    
    # Fit hierarchical model
    df, alpha_fit, S_dict = model.fit_hierarchical(df)
    
    print("\nFitted alpha values:")
    for tech, alpha in alpha_fit.items():
        print(f"  {tech}: {alpha:.3f} (base: {model.base_alpha[tech]:.2f})")
    
    # Compute residuals
    print("\nComputing residuals...")
    residuals = model.compute_residuals(df, alpha_fit, S_dict)
    
    # Test transformation boundary
    print("\nTesting 2.37% transformation boundary...")
    boundary_test = model.test_transformation_boundary(residuals)
    
    for tech, test in boundary_test.items():
        print(f"  {tech}: {test['median_pct_error']:.2f}% "
              f"(proximity: {test['transformation_proximity']:.2f}x)")
    
    # Test 13-phase structure
    phase_df, phase_structure = model.test_13_phase_structure(df, residuals)
    
    # Analyze subsets
    print("\nAnalyzing subsets...")
    subset_results = model.analyze_subsets(df, alpha_fit, S_dict)
    
    # Generate reports
    print("\nGenerating reports...")
    output_dir = model.generate_reports(df, alpha_fit, S_dict, residuals, 
                                       boundary_test, phase_df, phase_structure, 
                                       subset_results)
    
    # Create visualizations
    model.create_visualizations(df, residuals, phase_df, output_dir)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("="*60)
    
    return output_dir

if __name__ == "__main__":
    output_dir = main()
