#!/usr/bin/env python3
"""
Enhanced LoCuSS UFRF Analysis with:
- Morphology-aware predictions
- Dynamical mass as 4th probe
- z-dependent alpha with constrained splines
- Full uncertainty propagation
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime
from scipy import interpolate
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Import base functions
from locuss_loader import load_locuss, pivot_locuss

class EnhancedUFRFAnalysis:
    """Enhanced UFRF analysis with morphology and z-dependence"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.load_all_data()
        
    def load_all_data(self):
        """Load all data including morphology and dynamical masses"""
        # Load base data
        print("Loading base mass data...")
        long_df = load_locuss(self.data_dir)
        self.pivot_df = pivot_locuss(long_df)
        
        # Load morphology data
        print("Loading morphology data...")
        self.morph_df = pd.read_csv(self.data_dir / "locuss_morphology.csv")
        
        # Load dynamical masses
        print("Loading dynamical mass data...")
        self.dyn_df = pd.read_csv(self.data_dir / "locuss_dynamical_m500.csv")
        
        # Merge all data
        self.full_df = self.pivot_df.merge(
            self.morph_df[['cluster_id', 'morphology', 'cool_core', 'centroid_shift', 
                          'concentration', 'dynamical_state']], 
            on='cluster_id'
        ).merge(
            self.dyn_df[['cluster_id', 'M500_DYN', 'M500_DYN_err', 
                        'velocity_dispersion', 'n_galaxies']], 
            on='cluster_id'
        )
        
        # Convert to lowercase for consistency
        for col in ['m500_dyn', 'm500_dyn_err']:
            if col.upper() in self.full_df.columns:
                self.full_df[col] = self.full_df[col.upper()]
        
        print(f"Loaded {len(self.full_df)} clusters with full data")
        
    def get_z_dependent_alpha(self, z, tech, base_alpha, z_params=None):
        """
        Calculate z-dependent alpha using constrained spline
        
        alpha(z) = base_alpha * (1 + f(z))
        where f(z) is a smooth function with shrinkage
        """
        if z_params is None:
            # Default: weak linear z-dependence
            z_params = {'linear': 0.1, 'quadratic': 0.0}
        
        # Normalized redshift (z - 0.2) / 0.1 for stability
        z_norm = (z - 0.2) / 0.1
        
        # Constrained polynomial (could extend to spline)
        f_z = z_params.get('linear', 0) * z_norm + \
              z_params.get('quadratic', 0) * z_norm**2
        
        # Apply shrinkage to keep variations small
        shrinkage = 0.5  # Shrink variations by 50%
        f_z = f_z * shrinkage
        
        # Ensure alpha stays positive and reasonable
        alpha_z = base_alpha * (1 + f_z)
        alpha_z = np.clip(alpha_z, 0.1, 1.5)
        
        return alpha_z
    
    def estimate_morphology_adjusted_S(self, df, tech_pairs, morph_weight=0.3):
        """
        Estimate S with morphology adjustment
        
        Relaxed clusters get lower weight on S estimation
        Disturbed clusters get higher weight
        """
        S_estimates = []
        weights = []
        
        for _, row in df.iterrows():
            # Base weight from morphology
            if row['dynamical_state'] == 'relaxed':
                morph_factor = 1 - morph_weight
            elif row['dynamical_state'] == 'merging':
                morph_factor = 1 + morph_weight
            else:  # intermediate
                morph_factor = 1.0
            
            # Also use centroid shift as continuous indicator
            cs_factor = 1 + 2 * row['centroid_shift']  # Higher shift = more weight
            
            weight = morph_factor * cs_factor
            weights.append(weight)
        
        # Compute weighted S from pairs
        for t1, t2 in tech_pairs:
            if f'm500_{t1.lower()}' in df.columns and f'm500_{t2.lower()}' in df.columns:
                m1 = df[f'm500_{t1.lower()}'].values
                m2 = df[f'm500_{t2.lower()}'].values
                
                valid = (m1 > 0) & (m2 > 0)
                if valid.sum() > 5:
                    log_ratio = np.log(m1[valid] / m2[valid])
                    # Weight by morphology
                    w = np.array(weights)[valid]
                    S_pair = np.average(log_ratio, weights=w)
                    S_estimates.append(S_pair)
        
        return np.median(S_estimates) if S_estimates else 0.0
    
    def run_enhanced_predictions(self, held_out='HSE', use_morphology=True, 
                               use_z_dependence=True, include_dynamical=True):
        """
        Run enhanced predictions with all improvements
        """
        # Base alpha values
        base_alpha = {
            'WL': 0.3,
            'SZ': 0.5,
            'HSE': 0.7,
            'DYN': 0.4  # New dynamical alpha
        }
        
        # Z-dependence parameters (fitted from data or set manually)
        z_params = {
            'WL': {'linear': 0.05, 'quadratic': 0.01},
            'SZ': {'linear': 0.08, 'quadratic': -0.02},
            'HSE': {'linear': 0.10, 'quadratic': 0.02},
            'DYN': {'linear': 0.06, 'quadratic': 0.00}
        }
        
        # Available techniques
        all_techs = ['WL', 'SZ', 'HSE']
        if include_dynamical:
            all_techs.append('DYN')
        
        using_techs = [t for t in all_techs if t != held_out]
        
        results = []
        
        for _, row in self.full_df.iterrows():
            z = row['z']
            
            # Get z-dependent alphas for ALL techniques (including held-out)
            if use_z_dependence:
                alpha = {t: self.get_z_dependent_alpha(z, t, base_alpha.get(t, 0.5), 
                                                      z_params.get(t, {'linear': 0.05, 'quadratic': 0.0})) 
                        for t in base_alpha.keys()}
            else:
                alpha = base_alpha.copy()
            
            # Estimate S with morphology weighting if enabled
            if use_morphology:
                # Create mini-df for this cluster's neighborhood in z
                z_window = 0.05
                neighbors = self.full_df[
                    (self.full_df['z'] >= z - z_window) & 
                    (self.full_df['z'] <= z + z_window)
                ]
                
                tech_pairs = [(using_techs[i], using_techs[j]) 
                             for i in range(len(using_techs)) 
                             for j in range(i+1, len(using_techs))]
                
                S = self.estimate_morphology_adjusted_S(neighbors, tech_pairs)
            else:
                # Simple S estimation
                S = 0.0  # Simplified for this example
            
            # Estimate intrinsic mass with error propagation
            log_masses = []
            weights = []
            
            for tech in using_techs:
                m_col = f'm500_{tech.lower()}'
                e_col = f'm500_{tech.lower()}_err'
                
                if m_col in row and row[m_col] > 0:
                    m = row[m_col]
                    e = row[e_col] if e_col in row else 0.2 * m
                    
                    # Convert to log space
                    log_m = np.log(m) - alpha[tech] * S
                    
                    # Weight by inverse variance
                    w = 1.0 / (e / m)**2
                    
                    log_masses.append(log_m)
                    weights.append(w)
            
            if log_masses:
                # Weighted average for intrinsic mass
                log_m_star = np.average(log_masses, weights=weights)
                
                # Predict held-out mass
                log_pred = log_m_star + alpha[held_out] * S
                pred = np.exp(log_pred)
                
                # Uncertainty propagation
                var_intrinsic = 1.0 / np.sum(weights)
                var_proj = (alpha[held_out] * 0.1)**2  # Assume 10% uncertainty in S
                log_pred_err = np.sqrt(var_intrinsic + var_proj)
                pred_err = pred * log_pred_err
            else:
                pred = np.nan
                pred_err = np.nan
            
            # Store results
            true_col = f'm500_{held_out.lower()}'
            true_val = row[true_col] if true_col in row else np.nan
            
            results.append({
                'cluster_id': row['cluster_id'],
                'z': z,
                'morphology': row['morphology'],
                'dynamical_state': row['dynamical_state'],
                'y_true': true_val,
                'y_pred': pred,
                'y_pred_err': pred_err,
                'S': S,
                'alpha_used': alpha[held_out],
                'n_probes_used': len(log_masses)
            })
        
        return pd.DataFrame(results)
    
    def analyze_results(self, results_df):
        """Analyze enhanced prediction results"""
        valid = ~results_df['y_pred'].isna() & (results_df['y_true'] > 0)
        df = results_df[valid].copy()
        
        # Overall metrics
        log_residuals = np.log(df['y_true']) - np.log(df['y_pred'])
        rmse = np.sqrt(np.mean(log_residuals**2))
        bias = np.median(log_residuals)
        
        # Metrics by morphology
        morph_metrics = {}
        for state in df['dynamical_state'].unique():
            mask = df['dynamical_state'] == state
            if mask.sum() > 0:
                state_residuals = log_residuals[mask]
                morph_metrics[state] = {
                    'n': int(mask.sum()),
                    'rmse': float(np.sqrt(np.mean(state_residuals**2))),
                    'bias': float(np.median(state_residuals)),
                    'scatter': float(np.std(state_residuals))
                }
        
        return {
            'overall': {
                'n': int(len(df)),
                'rmse': float(rmse),
                'bias': float(bias),
                'scatter': float(np.std(log_residuals))
            },
            'by_morphology': morph_metrics
        }
    
    def plot_enhanced_results(self, results_df, output_dir):
        """Create enhanced visualization plots"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        valid = ~results_df['y_pred'].isna() & (results_df['y_true'] > 0)
        df = results_df[valid]
        
        # 1. Prediction vs Truth colored by morphology
        ax = axes[0, 0]
        colors = {'relaxed': 'blue', 'intermediate': 'orange', 'merging': 'red'}
        for state, color in colors.items():
            mask = df['dynamical_state'] == state
            ax.scatter(df.loc[mask, 'y_true'], df.loc[mask, 'y_pred'], 
                      c=color, label=state, alpha=0.6)
        
        # Add 1:1 line
        lims = [df['y_true'].min(), df['y_true'].max()]
        ax.plot(lims, lims, 'k--', alpha=0.5)
        ax.set_xlabel('True M500 (10^14 M_sun)')
        ax.set_ylabel('Predicted M500 (10^14 M_sun)')
        ax.set_title('Predictions by Morphology')
        ax.legend()
        ax.set_xscale('log')
        ax.set_yscale('log')
        
        # 2. Residuals vs Redshift
        ax = axes[0, 1]
        log_residuals = np.log(df['y_pred'] / df['y_true'])
        ax.scatter(df['z'], log_residuals, c=df['S'], cmap='coolwarm', alpha=0.6)
        ax.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax.set_xlabel('Redshift')
        ax.set_ylabel('Log Residual')
        ax.set_title('Residuals vs Redshift (colored by S)')
        plt.colorbar(ax.collections[0], ax=ax, label='S')
        
        # 3. Alpha variation with z
        ax = axes[1, 0]
        z_range = np.linspace(0.15, 0.30, 100)
        for tech, color in zip(['WL', 'SZ', 'HSE', 'DYN'], 
                              ['blue', 'green', 'red', 'purple']):
            alpha_z = [self.get_z_dependent_alpha(z, tech, 
                      {'WL': 0.3, 'SZ': 0.5, 'HSE': 0.7, 'DYN': 0.4}[tech]) 
                      for z in z_range]
            ax.plot(z_range, alpha_z, label=tech, color=color)
        
        ax.set_xlabel('Redshift')
        ax.set_ylabel('Alpha(z)')
        ax.set_title('Z-dependent Alpha Values')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 4. Error distribution
        ax = axes[1, 1]
        pct_errors = 100 * (df['y_pred'] - df['y_true']) / df['y_true']
        ax.hist(pct_errors, bins=20, alpha=0.7, edgecolor='black')
        ax.axvline(x=0, color='r', linestyle='--', alpha=0.5)
        ax.set_xlabel('Percentage Error (%)')
        ax.set_ylabel('Count')
        ax.set_title(f'Error Distribution (median: {np.median(np.abs(pct_errors)):.1f}%)')
        
        plt.tight_layout()
        plt.savefig(output_dir / 'enhanced_analysis.png', dpi=150)
        plt.close()

def main():
    """Run complete enhanced analysis"""
    
    print("="*60)
    print("Enhanced LoCuSS UFRF Analysis")
    print("="*60)
    
    # Initialize analysis
    analysis = EnhancedUFRFAnalysis()
    
    # Create output directory
    output_dir = Path("results") / f"enhanced_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run for each held-out scenario
    scenarios = ['HSE', 'SZ', 'WL', 'DYN']
    all_results = {}
    
    for held_out in scenarios:
        print(f"\n{'='*40}")
        print(f"Scenario: {held_out} held-out")
        print(f"{'='*40}")
        
        # Run enhanced predictions
        results = analysis.run_enhanced_predictions(
            held_out=held_out,
            use_morphology=True,
            use_z_dependence=True,
            include_dynamical=(held_out != 'DYN')
        )
        
        # Analyze results
        metrics = analysis.analyze_results(results)
        all_results[held_out] = metrics
        
        # Save results
        results.to_csv(output_dir / f'predictions_{held_out}_enhanced.csv', index=False)
        
        # Print summary
        print(f"\nOverall: N={metrics['overall']['n']}, "
              f"RMSE={metrics['overall']['rmse']:.3f}, "
              f"Bias={metrics['overall']['bias']:.3f}")
        
        print("\nBy Morphology:")
        for state, m in metrics['by_morphology'].items():
            print(f"  {state}: N={m['n']}, RMSE={m['rmse']:.3f}, Bias={m['bias']:.3f}")
        
        # Create plots
        analysis.plot_enhanced_results(results, output_dir)
    
    # Save comprehensive report
    report = {
        'timestamp': datetime.now().isoformat(),
        'scenarios': all_results,
        'enhancements': {
            'morphology_adjustment': True,
            'z_dependent_alpha': True,
            'dynamical_mass_included': True,
            'error_propagation': True
        }
    }
    
    with open(output_dir / 'enhanced_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n{'='*60}")
    print(f"Enhanced analysis complete!")
    print(f"Results saved to: {output_dir}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
