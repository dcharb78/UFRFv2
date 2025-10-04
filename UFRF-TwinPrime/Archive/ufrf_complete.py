#!/usr/bin/env python3
"""
================================================================================
COMPLETE UFRF PRIME GAP ANALYSIS WITH FIBONACCI CONNECTIONS
================================================================================

INSTRUCTIONS TO RUN:
--------------------
1. Save this file as: ufrf_complete.py
2. Install requirements: pip install numpy scipy matplotlib
3. Run it: python ufrf_complete.py
4. Wait: ~2 min for 10M, ~20 min for 100M primes
5. Check output files and report results back

CONFIGURATION (EDIT THIS):
--------------------------
"""
PRIME_LIMIT = 10_000_000  # Start with 10M, can increase to 100_000_000 or 1_000_000_000
SAVE_PLOTS = True          # Set False if matplotlib issues
VERBOSE = True             # Set False for less output

"""
WHAT THIS DOES:
--------------
1. Generates primes and analyzes gaps (2, 6, 26, etc.)
2. Finds Fibonacci primes and their relationships  
3. Analyzes 13-cycle patterns
4. Tests hyperdimensional phase agreements
5. Computes the 2/3 ratio manifestations
6. Generates comprehensive report

EXPECTED OUTPUT FILES:
---------------------
- complete_analysis_report.txt (Main results)
- results_for_claude.txt (Copy this content back)
- analysis_plots.png (If matplotlib works)

================================================================================
"""

import numpy as np
import math
import json
import time
from collections import defaultdict
from datetime import datetime
import sys

# Check if matplotlib available
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except:
    MATPLOTLIB_AVAILABLE = False
    print("Note: matplotlib not available, skipping plots")

class CompleteUFRFAnalysis:
    """Complete UFRF Analysis in single class"""
    
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.phi = (1 + np.sqrt(5)) / 2
        self.primes = []
        self.gap_data = {}
        self.fibonacci_numbers = []
        self.fibonacci_primes = []
        self.results_summary = {}
        
    def log(self, msg):
        if self.verbose:
            print(msg)
    
    # ========== PRIME GENERATION ==========
    
    def generate_primes(self, limit):
        """Efficient segmented sieve"""
        self.log(f"\nGenerating primes up to {limit:,}...")
        start_time = time.time()
        
        # For smaller limits, use simple sieve
        if limit <= 10_000_000:
            sieve = np.ones(limit + 1, dtype=bool)
            sieve[0] = sieve[1] = False
            
            for i in range(2, int(np.sqrt(limit)) + 1):
                if sieve[i]:
                    sieve[i*i:limit+1:i] = False
            
            self.primes = np.where(sieve)[0].tolist()
        else:
            # Segmented sieve for large limits
            segment_size = max(int(np.sqrt(limit)), 32768)
            
            # Get small primes first
            sqrt_limit = int(np.sqrt(limit)) + 1
            small_sieve = np.ones(sqrt_limit + 1, dtype=bool)
            small_sieve[0] = small_sieve[1] = False
            
            for i in range(2, int(np.sqrt(sqrt_limit)) + 1):
                if small_sieve[i]:
                    small_sieve[i*i:sqrt_limit+1:i] = False
            
            small_primes = np.where(small_sieve)[0].tolist()
            
            # Now segment
            self.primes = []
            for low in range(0, limit + 1, segment_size):
                high = min(low + segment_size, limit + 1)
                segment = np.ones(high - low, dtype=bool)
                
                for p in small_primes:
                    start = max(p * p, low + (p - low % p) % p)
                    if start < high:
                        segment[start - low::p] = False
                
                if low == 0:
                    segment[0] = segment[1] = False
                elif low == 1:
                    segment[0] = False
                
                for i in range(len(segment)):
                    if segment[i]:
                        self.primes.append(low + i)
        
        elapsed = time.time() - start_time
        self.log(f"Generated {len(self.primes):,} primes in {elapsed:.2f} seconds")
        return self.primes
    
    # ========== GAP ANALYSIS ==========
    
    def analyze_gaps(self):
        """Analyze all gap patterns"""
        self.log("\nAnalyzing prime gaps...")
        
        gap_counts = defaultdict(int)
        gap_pairs = defaultdict(list)
        
        for i in range(len(self.primes) - 1):
            gap = self.primes[i + 1] - self.primes[i]
            gap_counts[gap] += 1
            
            # Track specific gaps
            if gap in [2, 6, 26, 106, 338]:
                gap_pairs[gap].append((self.primes[i], self.primes[i + 1]))
        
        self.gap_data = {
            'counts': dict(gap_counts),
            'pairs': dict(gap_pairs)
        }
        
        # Report key gaps
        for gap in [2, 6, 26]:
            count = len(gap_pairs.get(gap, []))
            density = count / len(self.primes) if self.primes else 0
            self.log(f"  Gap={gap}: {count:,} occurrences, density={density:.6f}")
        
        return self.gap_data
    
    # ========== 13-CYCLE ANALYSIS ==========
    
    def analyze_13_cycle(self, gap):
        """Analyze 13-cycle for specific gap"""
        if gap not in self.gap_data['pairs']:
            return None
        
        pairs = self.gap_data['pairs'][gap]
        phase_counts = [0] * 13
        
        for p1, p2 in pairs:
            phase_counts[p1 % 13] += 1
        
        total = sum(phase_counts)
        expected = total / 13
        
        # Chi-squared test
        chi_squared = sum((obs - expected)**2 / expected for obs in phase_counts if expected > 0)
        
        return {
            'phase_counts': phase_counts,
            'total': total,
            'expected': expected,
            'chi_squared': chi_squared,
            'phase_0_void': phase_counts[0] == 0,
            'phase_11_minimal': phase_counts[11] <= expected * 0.1
        }
    
    # ========== FIBONACCI ANALYSIS ==========
    
    def analyze_fibonacci(self):
        """Generate and analyze Fibonacci primes"""
        self.log("\nAnalyzing Fibonacci connections...")
        
        # Generate Fibonacci numbers
        self.fibonacci_numbers = [1, 1]
        while self.fibonacci_numbers[-1] < self.primes[-1]:
            next_fib = self.fibonacci_numbers[-1] + self.fibonacci_numbers[-2]
            self.fibonacci_numbers.append(next_fib)
        
        # Find Fibonacci primes
        prime_set = set(self.primes)
        self.fibonacci_primes = [f for f in self.fibonacci_numbers if f in prime_set]
        
        self.log(f"  Found {len(self.fibonacci_primes)} Fibonacci primes")
        
        # Check if Fibonacci primes create special gaps
        fib_gaps = defaultdict(int)
        for i, p in enumerate(self.primes[:-1]):
            if p in self.fibonacci_primes:
                gap = self.primes[i + 1] - p
                fib_gaps[gap] += 1
        
        return {
            'fibonacci_count': len(self.fibonacci_numbers),
            'fibonacci_primes': self.fibonacci_primes[:20],  # First 20
            'fibonacci_gaps': dict(fib_gaps)
        }
    
    # ========== PHASE AGREEMENTS ==========
    
    def find_phase_agreements(self):
        """Find hyperdimensional phase agreements"""
        self.log("\nFinding phase agreements...")
        
        agreements = []
        test_primes = self.primes[:min(1000, len(self.primes))]
        bases = [2, 3, 5, 7, 11, 13, self.phi, math.e]
        
        for p in test_primes:
            agreement_count = 0
            
            for base in bases:
                if base != 1:
                    log_val = math.log(p) / math.log(base)
                    fractional = log_val - int(log_val)
                    
                    # Near integer = phase agreement
                    if fractional < 0.1 or fractional > 0.9:
                        agreement_count += 1
            
            if agreement_count >= 3:
                is_fib = p in self.fibonacci_primes
                agreements.append({'prime': p, 'agreements': agreement_count, 'is_fibonacci': is_fib})
        
        return agreements
    
    # ========== 2/3 RATIO ANALYSIS ==========
    
    def analyze_two_thirds(self):
        """Find where 2/3 ratio manifests"""
        ratios = {}
        
        # Gap density ratios
        if 2 in self.gap_data['pairs'] and 26 in self.gap_data['pairs']:
            density_2 = len(self.gap_data['pairs'][2]) / len(self.primes)
            density_26 = len(self.gap_data['pairs'][26]) / len(self.primes)
            
            ratios['gap_26_to_theoretical'] = density_26 / (2/13)
            ratios['fibonacci_prime_density'] = len(self.fibonacci_primes) / len(self.fibonacci_numbers)
        
        # Active phases (non-void, non-minimal)
        cycle_26 = self.analyze_13_cycle(26)
        if cycle_26:
            active_phases = sum(1 for c in cycle_26['phase_counts'] if c > cycle_26['expected'] * 0.5)
            ratios['active_phases'] = active_phases / 13
        
        return ratios
    
    # ========== REPORT GENERATION ==========
    
    def generate_report(self):
        """Generate complete analysis report"""
        lines = []
        lines.append("=" * 80)
        lines.append("COMPLETE UFRF PRIME GAP ANALYSIS REPORT")
        lines.append(f"Generated: {datetime.now()}")
        lines.append("=" * 80)
        
        # Configuration
        lines.append(f"\nCONFIGURATION:")
        lines.append(f"  Prime limit: {self.primes[-1]:,}")
        lines.append(f"  Total primes: {len(self.primes):,}")
        
        # Gap statistics
        lines.append("\n" + "-" * 40)
        lines.append("GAP STATISTICS")
        lines.append("-" * 40)
        
        for gap in [2, 6, 26, 106, 338]:
            if gap in self.gap_data['pairs']:
                count = len(self.gap_data['pairs'][gap])
                density = count / len(self.primes)
                lines.append(f"\nGap={gap}:")
                lines.append(f"  Count: {count:,}")
                lines.append(f"  Density: {density:.6f}")
                
                if gap == 26:
                    theoretical = 2/13
                    ratio = density / theoretical
                    lines.append(f"  Theoretical (2/13): {theoretical:.6f}")
                    lines.append(f"  Observed/Theoretical: {ratio:.4f}")
        
        # Gap dominance check
        gap_2_count = len(self.gap_data['pairs'].get(2, []))
        gap_6_count = len(self.gap_data['pairs'].get(6, []))
        
        lines.append("\n" + "-" * 40)
        lines.append("GAP DOMINANCE TEST")
        lines.append("-" * 40)
        lines.append(f"Gap=2 count: {gap_2_count:,}")
        lines.append(f"Gap=6 count: {gap_6_count:,}")
        if gap_6_count > gap_2_count:
            lines.append("*** REVOLUTIONARY: Gap=6 EXCEEDS Gap=2! ***")
        
        # 13-Cycle analysis
        lines.append("\n" + "-" * 40)
        lines.append("13-CYCLE ANALYSIS")
        lines.append("-" * 40)
        
        for gap in [2, 6, 26]:
            cycle = self.analyze_13_cycle(gap)
            if cycle:
                lines.append(f"\nGap={gap}:")
                lines.append(f"  Chi-squared: {cycle['chi_squared']:.2f}")
                lines.append(f"  Phase 0 void: {cycle['phase_0_void']}")
                lines.append(f"  Phase 11 minimal: {cycle['phase_11_minimal']}")
                
                if gap == 26:
                    lines.append("  Phase distribution:")
                    for i, count in enumerate(cycle['phase_counts']):
                        pct = 100 * count / cycle['total']
                        lines.append(f"    Phase {i:2d}: {count:5d} ({pct:5.2f}%)")
        
        # Fibonacci analysis
        fib_data = self.analyze_fibonacci()
        lines.append("\n" + "-" * 40)
        lines.append("FIBONACCI PRIME ANALYSIS")
        lines.append("-" * 40)
        lines.append(f"Fibonacci numbers up to limit: {fib_data['fibonacci_count']}")
        lines.append(f"Fibonacci primes found: {len(self.fibonacci_primes)}")
        lines.append(f"First 10 Fibonacci primes: {self.fibonacci_primes[:10]}")
        
        lines.append("\nGaps created by Fibonacci primes:")
        for gap, count in sorted(fib_data['fibonacci_gaps'].items())[:10]:
            lines.append(f"  Gap={gap}: {count} times")
        
        # Phase agreements
        agreements = self.find_phase_agreements()
        fib_agreements = [a for a in agreements if a['is_fibonacci']]
        
        lines.append("\n" + "-" * 40)
        lines.append("HYPERDIMENSIONAL PHASE AGREEMENTS")
        lines.append("-" * 40)
        lines.append(f"Total phase agreements: {len(agreements)}")
        lines.append(f"Fibonacci prime agreements: {len(fib_agreements)}")
        
        # 2/3 ratio
        ratios = self.analyze_two_thirds()
        lines.append("\n" + "-" * 40)
        lines.append("2/3 RATIO MANIFESTATIONS")
        lines.append("-" * 40)
        for key, value in ratios.items():
            lines.append(f"{key}: {value:.4f}")
        
        return "\n".join(lines)
    
    # ========== RESULTS FOR CLAUDE ==========
    
    def generate_claude_report(self):
        """Generate formatted results to report back"""
        lines = []
        lines.append("HYPERDIMENSIONAL ANALYSIS RESULTS")
        lines.append("=" * 50)
        lines.append(f"Configuration: {len(self.primes):,} primes analyzed (limit: {self.primes[-1]:,})")
        
        # Gap dominance
        gap_2 = len(self.gap_data['pairs'].get(2, []))
        gap_6 = len(self.gap_data['pairs'].get(6, []))
        gap_26 = len(self.gap_data['pairs'].get(26, []))
        
        lines.append("\nGAP DOMINANCE:")
        lines.append(f"Gap=2: {gap_2:,}")
        lines.append(f"Gap=6: {gap_6:,}")
        lines.append(f"Dominance: Gap=6 {'DOES' if gap_6 > gap_2 else 'DOES NOT'} exceed Gap=2")
        
        # Gap=26 structure
        lines.append("\nGAP=26 STRUCTURE:")
        lines.append(f"Count: {gap_26:,}")
        
        if gap_26 > 0:
            density_26 = gap_26 / len(self.primes)
            theoretical = 2/13
            ratio = density_26 / theoretical
            
            lines.append(f"Density: {density_26:.6f}")
            lines.append(f"Theoretical (2/13): {theoretical:.6f}")
            lines.append(f"Observed/Theoretical: {ratio:.4f}")
            
            cycle_26 = self.analyze_13_cycle(26)
            if cycle_26:
                lines.append(f"Phase 0: {cycle_26['phase_counts'][0]} (void confirmed: {'YES' if cycle_26['phase_0_void'] else 'NO'})")
                lines.append(f"Phase 11: {cycle_26['phase_counts'][11]} (minimal confirmed: {'YES' if cycle_26['phase_11_minimal'] else 'NO'})")
        
        # Fibonacci
        lines.append("\nFIBONACCI CONNECTIONS:")
        lines.append(f"Fibonacci primes found: {self.fibonacci_primes[:10]}")
        
        fib_data = self.analyze_fibonacci()
        if 2 in fib_data['fibonacci_gaps'] or 6 in fib_data['fibonacci_gaps'] or 26 in fib_data['fibonacci_gaps']:
            lines.append("Create special gaps: YES")
            for gap in [2, 6, 26]:
                if gap in fib_data['fibonacci_gaps']:
                    lines.append(f"  Gap={gap}: {fib_data['fibonacci_gaps'][gap]} times")
        
        # Phase agreements
        agreements = self.find_phase_agreements()
        fib_agreements = [a for a in agreements if a['is_fibonacci']]
        lines.append(f"Phase agreements at Fib primes: {len(fib_agreements)}")
        
        # 2/3 ratio
        lines.append("\n2/3 RATIO MANIFESTATIONS:")
        ratios = self.analyze_two_thirds()
        for key, value in ratios.items():
            lines.append(f"  {key}: {value:.4f}")
        
        # Anomalies
        lines.append("\nANOMALIES:")
        if gap_6 > gap_2:
            lines.append("  - Gap=6 exceeds Gap=2 (UNEXPECTED)")
        if gap_26 > 0:
            cycle = self.analyze_13_cycle(26)
            if cycle and cycle['phase_0_void']:
                lines.append("  - Phase 0 is completely void for Gap=26 (CONFIRMS UFRF)")
        
        return "\n".join(lines)
    
    # ========== VISUALIZATION ==========
    
    def create_plots(self):
        """Create visualization if matplotlib available"""
        if not MATPLOTLIB_AVAILABLE or not SAVE_PLOTS:
            return
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            
            # Gap counts
            ax = axes[0, 0]
            gaps = [2, 6, 26]
            counts = [len(self.gap_data['pairs'].get(g, [])) for g in gaps]
            ax.bar(gaps, counts)
            ax.set_xlabel('Gap Size')
            ax.set_ylabel('Count')
            ax.set_title('Gap Distribution')
            
            # 13-cycle for gap=26
            ax = axes[0, 1]
            cycle = self.analyze_13_cycle(26)
            if cycle:
                ax.bar(range(13), cycle['phase_counts'])
                ax.axhline(y=cycle['expected'], color='r', linestyle='--', label='Expected')
                ax.set_xlabel('Phase (mod 13)')
                ax.set_ylabel('Count')
                ax.set_title('Gap=26 13-Cycle')
                ax.legend()
            
            # Fibonacci primes
            ax = axes[1, 0]
            if self.fibonacci_primes:
                ax.scatter(range(len(self.fibonacci_primes[:20])), self.fibonacci_primes[:20])
                ax.set_xlabel('Index')
                ax.set_ylabel('Fibonacci Prime Value')
                ax.set_title('First 20 Fibonacci Primes')
                ax.set_yscale('log')
            
            # Density comparison
            ax = axes[1, 1]
            gap_types = ['Gap=2', 'Gap=6', 'Gap=26']
            densities = []
            for g in [2, 6, 26]:
                if g in self.gap_data['pairs']:
                    densities.append(len(self.gap_data['pairs'][g]) / len(self.primes))
                else:
                    densities.append(0)
            
            ax.bar(gap_types, densities)
            ax.set_ylabel('Density')
            ax.set_title('Gap Density Comparison')
            
            plt.tight_layout()
            plt.savefig('analysis_plots.png', dpi=150, bbox_inches='tight')
            self.log("Plots saved to analysis_plots.png")
            
        except Exception as e:
            self.log(f"Plot generation failed: {e}")
    
    # ========== MAIN EXECUTION ==========
    
    def run_complete_analysis(self, limit):
        """Run the complete analysis pipeline"""
        print("\n" + "=" * 80)
        print("STARTING COMPLETE UFRF ANALYSIS")
        print("=" * 80)
        
        start_time = time.time()
        
        # Generate primes
        self.generate_primes(limit)
        
        # Analyze gaps
        self.analyze_gaps()
        
        # Generate reports
        full_report = self.generate_report()
        claude_report = self.generate_claude_report()
        
        # Save reports
        with open('complete_analysis_report.txt', 'w') as f:
            f.write(full_report)
        
        with open('results_for_claude.txt', 'w') as f:
            f.write(claude_report)
        
        # Create plots
        self.create_plots()
        
        # Print summary
        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE")
        print("=" * 80)
        
        elapsed = time.time() - start_time
        print(f"Time taken: {elapsed:.2f} seconds")
        print(f"\nFiles generated:")
        print("  - complete_analysis_report.txt (full results)")
        print("  - results_for_claude.txt (COPY THIS TO CLAUDE)")
        
        if MATPLOTLIB_AVAILABLE and SAVE_PLOTS:
            print("  - analysis_plots.png (visualizations)")
        
        # Print key findings
        print("\n" + "=" * 80)
        print("KEY FINDINGS TO REPORT:")
        print("=" * 80)
        
        gap_2 = len(self.gap_data['pairs'].get(2, []))
        gap_6 = len(self.gap_data['pairs'].get(6, []))
        gap_26 = len(self.gap_data['pairs'].get(26, []))
        
        print(f"1. Gap=6 {'EXCEEDS' if gap_6 > gap_2 else 'does not exceed'} Gap=2")
        print(f"2. Gap=26 count: {gap_26:,}")
        
        cycle_26 = self.analyze_13_cycle(26)
        if cycle_26:
            print(f"3. Phase 0 {'IS' if cycle_26['phase_0_void'] else 'IS NOT'} void for Gap=26")
            print(f"4. Phase 11 {'IS' if cycle_26['phase_11_minimal'] else 'IS NOT'} minimal for Gap=26")
        
        print(f"5. Found {len(self.fibonacci_primes)} Fibonacci primes")
        
        print("\n>>> COPY THE CONTENTS OF 'results_for_claude.txt' AND PASTE BACK <<<")
        
        return {
            'primes_count': len(self.primes),
            'gap_2': len(self.gap_data['pairs'].get(2, [])),
            'gap_6': len(self.gap_data['pairs'].get(6, [])),
            'gap_26': len(self.gap_data['pairs'].get(26, [])),
            'fibonacci_primes': len(self.fibonacci_primes)
        }

# ========== MAIN EXECUTION ==========

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     UNIFIED FRACTAL RESONANCE FRAMEWORK (UFRF)              ║
    ║     Complete Prime Gap Analysis with Fibonacci Connections   ║
    ╔══════════════════════════════════════════════════════════════╗
    
    This will analyze prime gaps focusing on:
    - Gap=26 (2×13) geometric necessity
    - Gap=6 dominance phenomenon
    - 13-cycle phase patterns
    - Fibonacci prime relationships
    - Hyperdimensional phase agreements
    - 2/3 ratio manifestations
    """)
    
    # Create and run analyzer
    analyzer = CompleteUFRFAnalysis(verbose=VERBOSE)
    
    try:
        results = analyzer.run_complete_analysis(PRIME_LIMIT)
        
        # Final success message
        print("\n" + "✓" * 40)
        print("SUCCESS! Analysis complete.")
        print("Please copy the contents of 'results_for_claude.txt'")
        print("and paste them back for interpretation.")
        print("✓" * 40)
        
    except MemoryError:
        print("\n" + "!" * 40)
        print("MEMORY ERROR: Reduce PRIME_LIMIT")
        print("Try 10_000_000 instead of", PRIME_LIMIT)
        print("!" * 40)
        
    except Exception as e:
        print("\n" + "!" * 40)
        print(f"ERROR: {e}")
        print("Please report this error with the full message")
        print("!" * 40)
        
    print("\n[END OF ANALYSIS]")


