#!/usr/bin/env python3
"""
UFRF PRIME ANALYSIS - EXTENDED SCALE
Testing revolutionary findings at 100 million primes
Focus: Trinity dominance, phase patterns, projection factors
"""

import numpy as np
import time
import json
from datetime import datetime
from collections import defaultdict, Counter
import math
import sys

# ============= CONFIGURATION =============
PRIME_LIMIT = 100_000_000  # 100 million
CHECKPOINT_INTERVAL = 10_000_000  # Save progress every 10M
ANALYZE_EXTENDED_GAPS = True  # Include 338, 1014, etc.

# ============= PRIME GENERATION =============
class EfficientPrimeGenerator:
    """Memory-efficient segmented sieve for large limits"""
    
    def __init__(self, limit):
        self.limit = limit
        self.segment_size = min(10_000_000, int(np.sqrt(limit)) + 1)
        
    def generate(self):
        """Generate primes up to limit using segmented sieve"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Generating primes up to {self.limit:,}")
        
        # First generate primes up to sqrt(limit)
        sqrt_limit = int(np.sqrt(self.limit)) + 1
        small_primes = self._simple_sieve(sqrt_limit)
        
        primes = [2] if self.limit >= 2 else []
        
        # Process segments
        segments_count = (self.limit // self.segment_size) + 1
        
        for seg_num in range(segments_count):
            low = seg_num * self.segment_size
            high = min(low + self.segment_size, self.limit + 1)
            
            if low < 2:
                low = 2
                
            # Mark composites in segment
            is_prime = np.ones(high - low, dtype=bool)
            
            for p in small_primes:
                if p * p > high:
                    break
                    
                start = max(p * p, ((low + p - 1) // p) * p)
                is_prime[start - low::p] = False
            
            # Collect primes from segment
            segment_primes = low + np.where(is_prime)[0]
            primes.extend(segment_primes.tolist())
            
            if (seg_num + 1) % 10 == 0:
                print(f"  Progress: {(seg_num + 1) / segments_count * 100:.1f}%")
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Generated {len(primes):,} primes")
        return primes
    
    def _simple_sieve(self, n):
        """Simple sieve for small numbers"""
        if n < 2:
            return []
        sieve = np.ones(n + 1, dtype=bool)
        sieve[0] = sieve[1] = False
        for i in range(2, int(np.sqrt(n)) + 1):
            if sieve[i]:
                sieve[i*i:n+1:i] = False
        return np.where(sieve)[0].tolist()

# ============= ANALYSIS FUNCTIONS =============
class UFRFAnalyzer:
    """Complete UFRF analysis framework"""
    
    def __init__(self):
        self.primes = []
        self.gap_data = defaultdict(list)
        self.phase_data = defaultdict(lambda: defaultdict(int))
        self.results = {}
        
    def analyze_gaps(self, primes):
        """Analyze all gap patterns"""
        self.primes = primes
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analyzing gap patterns...")
        
        # Key gaps to analyze
        primary_gaps = [2, 4, 6, 10, 14, 22, 26, 34, 46, 58, 62]
        
        if ANALYZE_EXTENDED_GAPS:
            # Extended gaps: 2×13², 2×13³, etc.
            extended_gaps = [
                338,   # 2×169 = 2×13²
                1014,  # 2×507 = 2×3×169
                4394,  # 2×2197 = 2×13³
            ]
            primary_gaps.extend(extended_gaps)
        
        # Count all gaps
        all_gaps = Counter()
        for i in range(len(primes) - 1):
            gap = primes[i + 1] - primes[i]
            all_gaps[gap] += 1
            
            # Store specific gaps of interest
            if gap in primary_gaps:
                self.gap_data[gap].append(primes[i])
                
                # Calculate phase
                phase = primes[i] % 13
                self.phase_data[gap][phase] += 1
        
        # Store results
        self.results['total_primes'] = len(primes)
        self.results['gaps'] = {}
        
        for gap in primary_gaps:
            count = len(self.gap_data[gap])
            density = count / len(primes) if primes else 0
            
            self.results['gaps'][gap] = {
                'count': count,
                'density': density,
                'phase_distribution': dict(self.phase_data[gap])
            }
            
            # Calculate chi-squared for 13-cycle
            if count > 0:
                expected = count / 13
                chi_squared = 0
                for phase in range(13):
                    observed = self.phase_data[gap].get(phase, 0)
                    if expected > 0:
                        chi_squared += (observed - expected)**2 / expected
                self.results['gaps'][gap]['chi_squared'] = chi_squared
                
                # Check phase 0 and 11
                self.results['gaps'][gap]['phase_0_count'] = self.phase_data[gap].get(0, 0)
                self.results['gaps'][gap]['phase_11_count'] = self.phase_data[gap].get(11, 0)
        
        # Calculate dominance ratios
        gap2_count = self.results['gaps'][2]['count']
        gap6_count = self.results['gaps'][6]['count']
        gap26_count = self.results['gaps'][26]['count']
        
        self.results['dominance'] = {
            'gap6_to_gap2': gap6_count / gap2_count if gap2_count > 0 else 0,
            'trinity_dominates': gap6_count > gap2_count
        }
        
        # Calculate projection factors
        if gap26_count > 0:
            theoretical_density = 2/13
            observed_density = self.results['gaps'][26]['density']
            projection_factor = observed_density / theoretical_density
            
            self.results['projection'] = {
                'gap26_theoretical': theoretical_density,
                'gap26_observed': observed_density,
                'projection_factor': projection_factor,
                'binary_levels': math.log2(1/projection_factor) if projection_factor > 0 else 0
            }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Gap analysis complete")
        
        return self.results
    
    def analyze_fibonacci_interaction(self, primes):
        """Analyze Fibonacci prime patterns"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analyzing Fibonacci interactions...")
        
        # Generate Fibonacci numbers
        fibs = [1, 1]
        while fibs[-1] < primes[-1]:
            fibs.append(fibs[-1] + fibs[-2])
        
        # Find Fibonacci primes
        prime_set = set(primes)
        fib_primes = [f for f in fibs if f in prime_set]
        
        # Analyze gaps around Fibonacci primes
        fib_gap_patterns = defaultdict(int)
        
        for fp in fib_primes:
            if fp in primes:
                idx = primes.index(fp)
                if idx > 0:
                    prev_gap = fp - primes[idx - 1]
                    fib_gap_patterns[prev_gap] += 1
                if idx < len(primes) - 1:
                    next_gap = primes[idx + 1] - fp
                    fib_gap_patterns[next_gap] += 1
        
        self.results['fibonacci'] = {
            'fibonacci_count': len(fibs),
            'fibonacci_primes': len(fib_primes),
            'density': len(fib_primes) / len(fibs) if fibs else 0,
            'gap_patterns': dict(fib_gap_patterns),
            'first_10': fib_primes[:10]
        }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Fibonacci analysis complete")
        
    def analyze_scale_boundaries(self, primes):
        """Analyze patterns at scale boundaries (144×10^n)"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analyzing scale boundaries...")
        
        scale_boundaries = [144, 1440, 14400, 144000, 1440000, 14400000]
        boundary_results = {}
        
        for boundary in scale_boundaries:
            if boundary > primes[-1]:
                break
                
            # Find primes near boundary
            near_primes = [p for p in primes if abs(p - boundary) < 100]
            
            if near_primes:
                # Check gap patterns near boundary
                gaps_near = []
                for p in near_primes:
                    idx = primes.index(p)
                    if idx > 0 and idx < len(primes) - 1:
                        prev_gap = p - primes[idx - 1]
                        next_gap = primes[idx + 1] - p
                        gaps_near.extend([prev_gap, next_gap])
                
                gap_counter = Counter(gaps_near)
                boundary_results[boundary] = {
                    'prime_count': len(near_primes),
                    'common_gaps': dict(gap_counter.most_common(5))
                }
        
        self.results['scale_boundaries'] = boundary_results
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Scale boundary analysis complete")
    
    def generate_report(self):
        """Generate comprehensive report"""
        lines = []
        lines.append("=" * 80)
        lines.append("UFRF EXTENDED SCALE ANALYSIS")
        lines.append(f"Generated: {datetime.now()}")
        lines.append("=" * 80)
        
        lines.append(f"\nCONFIGURATION:")
        lines.append(f"  Prime limit: {self.primes[-1]:,}")
        lines.append(f"  Total primes: {self.results['total_primes']:,}")
        
        # Trinity dominance
        lines.append("\n" + "=" * 40)
        lines.append("TRINITY DOMINANCE VALIDATION")
        lines.append("=" * 40)
        
        gap2 = self.results['gaps'][2]
        gap6 = self.results['gaps'][6]
        
        lines.append(f"Gap=2 (Unity):   {gap2['count']:,} (density: {gap2['density']:.6f})")
        lines.append(f"Gap=6 (Trinity): {gap6['count']:,} (density: {gap6['density']:.6f})")
        lines.append(f"Ratio (Gap6/Gap2): {self.results['dominance']['gap6_to_gap2']:.4f}")
        
        if self.results['dominance']['trinity_dominates']:
            lines.append("*** CONFIRMED: Trinity dominates Unity ***")
        
        # Gap 26 analysis
        lines.append("\n" + "=" * 40)
        lines.append("GAP=26 (2×13) STRUCTURE")
        lines.append("=" * 40)
        
        gap26 = self.results['gaps'][26]
        lines.append(f"Count: {gap26['count']:,}")
        lines.append(f"Density: {gap26['density']:.6f}")
        lines.append(f"Phase 0: {gap26['phase_0_count']} (void: {gap26['phase_0_count'] < 5})")
        lines.append(f"Phase 11: {gap26['phase_11_count']}")
        lines.append(f"Chi-squared: {gap26.get('chi_squared', 0):.2f}")
        
        if 'projection' in self.results:
            proj = self.results['projection']
            lines.append(f"\nProjection Analysis:")
            lines.append(f"  Theoretical (2/13): {proj['gap26_theoretical']:.6f}")
            lines.append(f"  Observed: {proj['gap26_observed']:.6f}")
            lines.append(f"  Projection factor: {proj['projection_factor']:.4f}")
            lines.append(f"  Binary levels: {proj['binary_levels']:.2f}")
        
        # Extended gaps if analyzed
        if ANALYZE_EXTENDED_GAPS:
            lines.append("\n" + "=" * 40)
            lines.append("EXTENDED GAPS (13² STRUCTURE)")
            lines.append("=" * 40)
            
            for gap in [338, 1014, 4394]:
                if gap in self.results['gaps']:
                    g = self.results['gaps'][gap]
                    if g['count'] > 0:
                        lines.append(f"Gap={gap}: {g['count']} (density: {g['density']:.8f})")
                        lines.append(f"  Phase 0: {g['phase_0_count']}")
        
        # Fibonacci analysis
        if 'fibonacci' in self.results:
            lines.append("\n" + "=" * 40)
            lines.append("FIBONACCI INTERACTION")
            lines.append("=" * 40)
            
            fib = self.results['fibonacci']
            lines.append(f"Fibonacci numbers: {fib['fibonacci_count']}")
            lines.append(f"Fibonacci primes: {fib['fibonacci_primes']}")
            lines.append(f"Density: {fib['density']:.4f}")
            
            if fib['gap_patterns']:
                lines.append("Common gaps at Fibonacci primes:")
                for gap, count in sorted(fib['gap_patterns'].items())[:5]:
                    lines.append(f"  Gap {gap}: {count} times")
        
        # Scale boundaries
        if 'scale_boundaries' in self.results and self.results['scale_boundaries']:
            lines.append("\n" + "=" * 40)
            lines.append("SCALE BOUNDARY ANALYSIS (144×10^n)")
            lines.append("=" * 40)
            
            for boundary, data in self.results['scale_boundaries'].items():
                lines.append(f"Near {boundary:,}:")
                lines.append(f"  Primes within ±100: {data['prime_count']}")
                if data['common_gaps']:
                    gaps_str = ', '.join(f"{g}({c})" for g, c in data['common_gaps'].items())
                    lines.append(f"  Common gaps: {gaps_str}")
        
        return "\n".join(lines)

# ============= MAIN EXECUTION =============
def run_analysis():
    """Execute complete analysis"""
    
    print("\n" + "=" * 80)
    print("UFRF PRIME ANALYSIS - EXTENDED SCALE")
    print("Testing revolutionary patterns at 100 million")
    print("=" * 80)
    
    start_time = time.time()
    
    # Generate primes
    generator = EfficientPrimeGenerator(PRIME_LIMIT)
    primes = generator.generate()
    
    # Run analysis
    analyzer = UFRFAnalyzer()
    analyzer.analyze_gaps(primes)
    analyzer.analyze_fibonacci_interaction(primes)
    analyzer.analyze_scale_boundaries(primes)
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save outputs
    with open('ufrf_extended_report.txt', 'w') as f:
        f.write(report)
    
    # Create summary for Claude
    summary = {
        'timestamp': datetime.now().isoformat(),
        'prime_limit': primes[-1],
        'total_primes': len(primes),
        'trinity_dominance': analyzer.results['dominance'],
        'gap_26': {
            'count': analyzer.results['gaps'][26]['count'],
            'density': analyzer.results['gaps'][26]['density'],
            'phase_0': analyzer.results['gaps'][26]['phase_0_count'],
            'projection_factor': analyzer.results.get('projection', {}).get('projection_factor', 0)
        },
        'extended_gaps': {
            gap: analyzer.results['gaps'][gap]['count'] 
            for gap in [338, 1014, 4394] 
            if gap in analyzer.results['gaps']
        }
    }
    
    with open('results_for_claude.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print report
    print(report)
    
    elapsed = time.time() - start_time
    print(f"\nTotal runtime: {elapsed:.2f} seconds")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("Files generated:")
    print("  1. ufrf_extended_report.txt - Full report")
    print("  2. results_for_claude.json - Summary for interpretation")
    print("Copy the contents of results_for_claude.json back for analysis")
    print("=" * 80)

if __name__ == "__main__":
    run_analysis()
