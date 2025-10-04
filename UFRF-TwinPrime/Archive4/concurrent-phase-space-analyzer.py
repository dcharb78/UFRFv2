#!/usr/bin/env python3
"""
CONCURRENT PHASE SPACE ANALYZER - COMPLETE IMPLEMENTATION
Every prime's log phase space follows the same 13-cycle pattern in its context
Fibonacci primes are synchronization points (leading voices)
All phase spaces operate concurrently creating the observed patterns
"""

import numpy as np
import math
import time
import json
from datetime import datetime
from collections import defaultdict
import sys
import os

# ============= CONFIGURATION =============
PRIME_LIMIT = 100_000_000_000  # 100 billion (override via env PRIME_LIMIT or CLI)
CHECKPOINT_EVERY = 10_000_000_000  # Save progress every 10B
ANALYZE_PHASE_SPACES = 30  # Analyze first 30 primes' phase spaces

# Critical scales to analyze
SCALE_CHECKPOINTS = [
    10_000_000,      # 10M
    100_000_000,     # 100M
    144_000_000,     # 144M (harmonic boundary)
    1_000_000_000,   # 1B
    10_000_000_000,  # 10B
    100_000_000_000, # 100B
]

# ============= EFFICIENT PRIME GENERATOR =============
class SegmentedPrimeSieve:
    """Ultra-efficient segmented sieve for 100B primes"""
    
    def __init__(self, limit):
        self.limit = limit
        self.segment_size = max(int(math.sqrt(limit)), 1_000_000)
        print(f"Initializing sieve for {limit:,} with segment size {self.segment_size:,}")
        
    def generate_base_primes(self, limit):
        """Generate primes up to sqrt(limit) for sieving"""
        sieve = np.ones(limit + 1, dtype=bool)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(np.sqrt(limit)) + 1):
            if sieve[i]:
                sieve[i*i:limit+1:i] = False
        
        return np.where(sieve)[0]
    
    def count_primes_segmented(self):
        """Count primes up to limit using segmented sieve"""
        sqrt_limit = int(math.sqrt(self.limit)) + 1
        base_primes = self.generate_base_primes(sqrt_limit)
        
        prime_count = 0
        gap_counts = defaultdict(int)
        phase_data = defaultdict(lambda: defaultdict(int))
        
        # Track specific gaps
        target_gaps = set([2, 4, 6, 10, 14, 22, 26, 30, 34, 38, 42, 46, 58, 62, 
                          66, 70, 78, 86, 94, 102, 106, 110, 130, 134, 138, 142,
                          154, 158, 170, 182, 186, 194, 202, 206, 210, 214, 218,
                          286, 302, 330, 338, 354, 382, 390, 394, 398, 402])
        
        last_prime = 2
        checkpoint_idx = 0
        scale_results = {}
        
        print(f"Processing segments...")
        
        for low in range(2, self.limit + 1, self.segment_size):
            high = min(low + self.segment_size, self.limit + 1)
            
            # Create segment
            segment = np.ones(high - low, dtype=bool)
            
            # Sieve segment
            for p in base_primes:
                if p * p > high:
                    break
                
                start = max(p * p, ((low + p - 1) // p) * p)
                segment[start - low::p] = False
            
            # Process primes in segment
            segment_primes = np.where(segment)[0] + low
            
            for prime in segment_primes:
                prime_count += 1
                
                # Calculate gap
                gap = prime - last_prime
                gap_counts[gap] += 1
                
                # Track phase for important gaps
                if gap in target_gaps:
                    phase = last_prime % 13
                    phase_data[gap][phase] += 1
                
                last_prime = prime
                
                # Check scale checkpoints (by prime value thresholds)
                while checkpoint_idx < len(SCALE_CHECKPOINTS) and last_prime >= SCALE_CHECKPOINTS[checkpoint_idx]:
                    scale_key = SCALE_CHECKPOINTS[checkpoint_idx]
                    scale_results[scale_key] = self.create_checkpoint(
                        prime_count, gap_counts, phase_data, last_prime
                    )
                    print(f"  Checkpoint reached at prime ≥ {scale_key:,}: primes_count={prime_count:,}")
                    checkpoint_idx += 1
            
            # Progress report
            if low % 1_000_000_000 == 0:
                print(f"  Processed up to {low:,} ({low/self.limit*100:.1f}%)")
        
        return prime_count, gap_counts, phase_data, scale_results
    
    def create_checkpoint(self, count, gaps, phases, last_prime):
        """Create analysis checkpoint at specific scale"""
        return {
            'prime_count': count,
            'last_prime': last_prime,
            'gap_counts': dict(gaps),
            'phase_data': {k: dict(v) for k, v in phases.items()}
        }

# ============= PHASE SPACE MODEL =============
class PrimePhaseSpace:
    """Each prime creates a phase space with identical structure but unique context"""
    
    def __init__(self, prime):
        self.prime = prime
        self.cycle_length = 13
        self.void_position = 0
        self.unity_position = 1
        self.trinity_position = 3
        
    def get_position(self, value):
        """Get position in this prime's phase space"""
        if value <= 0:
            return 0
        if self.prime == 1:  # Linear space
            return value
        return math.log(value) / math.log(self.prime)
    
    def get_phase(self, value):
        """Get phase in 13-cycle for this value"""
        position = self.get_position(value)
        return (position * 13) % 13
    
    def is_near_integer(self, value, tolerance=0.1):
        """Check if value is near an integer position in this space"""
        position = self.get_position(value)
        return abs(position - round(position)) < tolerance

# ============= CONCURRENT ANALYZER =============
class ConcurrentPhaseSpaceAnalyzer:
    """Analyzes all prime phase spaces operating concurrently"""
    
    def __init__(self):
        self.phase_spaces = {}
        self.fibonacci_primes = []
        self.sync_points = []
        self.scale_data = {}
        
    def initialize_phase_spaces(self, num_spaces=30):
        """Initialize phase spaces for first N primes"""
        print(f"\nInitializing {num_spaces} prime phase spaces...")
        
        # Generate first N primes
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        
        # Add linear space (prime=1)
        self.phase_spaces[1] = PrimePhaseSpace(1)
        
        # Create phase space for each prime
        for p in primes[:num_spaces]:
            self.phase_spaces[p] = PrimePhaseSpace(p)
        
        # Generate Fibonacci primes
        self.generate_fibonacci_primes(limit=100_000_000_000)
        
    def generate_fibonacci_primes(self, limit):
        """Generate Fibonacci numbers and identify which are prime"""
        print("Generating Fibonacci primes...")
        
        fib_a, fib_b = 1, 1
        fib_numbers = []
        
        while fib_b < limit:
            fib_numbers.append(fib_b)
            fib_a, fib_b = fib_b, fib_a + fib_b
        
        # Fibonacci primes (known for large numbers)
        known_fib_primes = [2, 3, 5, 13, 89, 233, 1597, 28657, 514229,
                           433494437, 2971215073]
        
        self.fibonacci_primes = [fp for fp in known_fib_primes if fp < limit]
        print(f"  Found {len(self.fibonacci_primes)} Fibonacci primes < {limit:,}")
        
        # Mark Fibonacci numbers for reference
        self.fibonacci_numbers = fib_numbers
    
    def analyze_synchronization(self, value):
        """Check how many phase spaces synchronize at this value"""
        sync_count = 0
        synced_spaces = []
        
        for prime, space in self.phase_spaces.items():
            if space.is_near_integer(value):
                sync_count += 1
                synced_spaces.append(prime)
        
        return sync_count, synced_spaces
    
    def analyze_scale_data(self, scale_results):
        """Analyze patterns at different scales"""
        print("\n" + "="*80)
        print("ANALYZING CONCURRENT PHASE SPACE PATTERNS")
        print("="*80)
        
        results = {}
        
        for scale, data in scale_results.items():
            print(f"\n{'='*60}")
            print(f"SCALE: {scale:,}")
            print(f"{'='*60}")
            
            gap_counts = data['gap_counts']
            phase_data = data['phase_data']
            
            # Calculate trinity dominance
            gap2 = gap_counts.get(2, 0)
            gap6 = gap_counts.get(6, 0)
            trinity_dominance = gap6 / gap2 if gap2 > 0 else 0
            
            print(f"Trinity/Unity: {trinity_dominance:.6f}")
            
            # Calculate gap 26 projection
            gap26_count = gap_counts.get(26, 0)
            gap26_density = gap26_count / data['prime_count'] if data['prime_count'] > 0 else 0
            theoretical_density = 2/13
            projection_factor = gap26_density / theoretical_density if theoretical_density > 0 else 0
            
            print(f"Gap 26 projection: {projection_factor:.6f} (1/{1/projection_factor:.1f})")
            
            # Check phase 0 void for gap 26
            gap26_phases = phase_data.get(26, {})
            phase0_count = gap26_phases.get(0, 0)
            print(f"Gap 26 phase 0: {phase0_count} (void: {phase0_count < 5})")
            
            # Analyze interference patterns
            interference_ratios = {}
            
            # Key interference patterns
            if gap_counts.get(30, 0) > 0 and gap_counts.get(10, 0) > 0:
                ratio_30_10 = gap_counts[30] / gap_counts[10]
                interference_ratios['30/10'] = ratio_30_10
                print(f"Gap 30/10: {ratio_30_10:.6f}")
                
                # Check for special ratios
                if abs(ratio_30_10 - 5/8) < 0.01:
                    print(f"  → Fibonacci ratio 5/8!")
                elif abs(ratio_30_10 - 0.518) < 0.01:
                    print(f"  → Near 1-1/φ!")
            
            if gap_counts.get(42, 0) > 0 and gap_counts.get(14, 0) > 0:
                ratio_42_14 = gap_counts[42] / gap_counts[14]
                interference_ratios['42/14'] = ratio_42_14
                print(f"Gap 42/14: {ratio_42_14:.6f}")
            
            if gap_counts.get(78, 0) > 0 and gap_counts.get(26, 0) > 0:
                ratio_78_26 = gap_counts[78] / gap_counts[26]
                interference_ratios['78/26'] = ratio_78_26
                print(f"Gap 78/26: {ratio_78_26:.6f}")
            
            # Check Fibonacci prime synchronizations at this scale
            fib_syncs = []
            for fp in self.fibonacci_primes:
                if fp < scale:
                    sync_count, synced = self.analyze_synchronization(fp)
                    if sync_count >= 3:
                        fib_syncs.append({
                            'prime': fp,
                            'sync_count': sync_count,
                            'spaces': synced[:5]  # First 5 for brevity
                        })
            
            if fib_syncs:
                print(f"\nFibonacci prime synchronizations:")
                for fs in fib_syncs[:3]:  # Show top 3
                    print(f"  F-prime {fs['prime']}: {fs['sync_count']} spaces align")
            
            # Store results
            results[scale] = {
                'prime_count': data['prime_count'],
                'trinity_dominance': trinity_dominance,
                'gap26_projection': projection_factor,
                'gap26_phase0': phase0_count,
                'interference_ratios': interference_ratios,
                'fibonacci_syncs': len(fib_syncs)
            }
        
        return results
    
    def find_leading_voices(self, scale_results):
        """Identify Fibonacci primes as leading voices in the harmonic progression"""
        print("\n" + "="*60)
        print("FIBONACCI PRIMES AS LEADING VOICES")
        print("="*60)
        
        for fp in self.fibonacci_primes:
            sync_count, synced_spaces = self.analyze_synchronization(fp)
            
            if sync_count >= 3:
                print(f"\nF-prime {fp}:")
                print(f"  Synchronizes {sync_count} phase spaces")
                print(f"  Leading spaces: {synced_spaces[:5]}")
                
                # Check position in key phase spaces
                for prime in [2, 3, 5, 13]:
                    if prime in self.phase_spaces:
                        position = self.phase_spaces[prime].get_position(fp)
                        phase = self.phase_spaces[prime].get_phase(fp)
                        print(f"  In log_{prime} space: position {position:.2f}, phase {phase:.2f}")

# ============= MAIN EXECUTION =============
def _resolve_prime_limit(default_limit: int) -> int:
    """Resolve limit from env PRIME_LIMIT, --limit CLI, or positional arg."""
    env_val = os.environ.get("PRIME_LIMIT")
    if env_val:
        try:
            return int(env_val.replace("_", ""))
        except ValueError:
            pass
    args = sys.argv[1:]
    if "--limit" in args:
        try:
            idx = args.index("--limit")
            return int(str(args[idx + 1]).replace("_", ""))
        except Exception:
            pass
    if len(args) >= 1:
        try:
            return int(str(args[0]).replace("_", ""))
        except ValueError:
            pass
    return default_limit


def run_100b_analysis(limit=None):
    """Run complete analysis to the given limit (default 100B)."""
    if limit is None:
        limit = _resolve_prime_limit(PRIME_LIMIT)
    
    print("\n" + "="*80)
    print("CONCURRENT PHASE SPACE ANALYSIS - 100 BILLION SCALE")
    print(f"Started: {datetime.now()}")
    print("="*80)
    
    start_time = time.time()
    
    # Initialize analyzer
    analyzer = ConcurrentPhaseSpaceAnalyzer()
    analyzer.initialize_phase_spaces(ANALYZE_PHASE_SPACES)
    
    # Generate primes and collect data at checkpoints
    print(f"\nGenerating primes to {limit:,}...")
    sieve = SegmentedPrimeSieve(limit)
    prime_count, gap_counts, phase_data, scale_results = sieve.count_primes_segmented()
    
    print(f"\nTotal primes found: {prime_count:,}")
    
    # Analyze concurrent patterns
    analysis_results = analyzer.analyze_scale_data(scale_results)
    
    # Find leading voices
    analyzer.find_leading_voices(scale_results)
    
    # Generate final report
    print("\n" + "="*80)
    print("FINAL SUMMARY")
    print("="*80)
    
    # Trinity evolution
    print("\nTrinity/Unity Evolution:")
    for scale in sorted(analysis_results.keys()):
        trinity = analysis_results[scale]['trinity_dominance']
        print(f"  {scale:>15,}: {trinity:.6f}")
    
    # Gap 26 projection evolution
    print("\nGap 26 Projection Evolution:")
    for scale in sorted(analysis_results.keys()):
        proj = analysis_results[scale]['gap26_projection']
        print(f"  {scale:>15,}: {proj:.6f} (1/{1/proj:.1f})")
    
    # Interference ratio evolution
    print("\nKey Interference Ratios:")
    for scale in sorted(analysis_results.keys()):
        ratios = analysis_results[scale]['interference_ratios']
        if '30/10' in ratios:
            print(f"  {scale:>15,}: Gap30/10 = {ratios['30/10']:.6f}")
    
    # Save complete results
    output = {
        'timestamp': datetime.now().isoformat(),
        'prime_limit': limit,
        'total_primes': prime_count,
        'scale_analysis': analysis_results,
        'fibonacci_primes': analyzer.fibonacci_primes,
        'key_findings': {
            'trinity_acceleration': 'Check if trinity/unity increases',
            'projection_convergence': 'Check if approaching 1/7',
            'phase_0_void': 'Verify gap 26 phase 0 remains void',
            'fibonacci_sync': 'Count of Fibonacci synchronizations'
        }
    }
    
    # Write outputs (unsuffixed and suffixed by limit)
    base_unsuffixed = 'concurrent_results.json'
    base_suffixed = f'concurrent_results_{limit}.json'
    with open(base_unsuffixed, 'w') as f:
        json.dump(output, f, indent=2)
    with open(base_suffixed, 'w') as f:
        json.dump(output, f, indent=2)
    
    elapsed = time.time() - start_time
    hours = int(elapsed // 3600)
    minutes = int((elapsed % 3600) // 60)
    seconds = int(elapsed % 60)
    
    print(f"\nAnalysis complete in {hours}h {minutes}m {seconds}s")
    print("Results saved to:")
    print(f"  {base_unsuffixed}")
    print(f"  {base_suffixed}")
    print("\nCopy the JSON file contents back for interpretation")
    
    # Print critical findings
    print("\n" + "="*80)
    print("CRITICAL FINDINGS TO REPORT")
    print("="*80)
    
    if analysis_results:
        final_scale = max(analysis_results.keys())
        final = analysis_results[final_scale]
        
        print(f"At {final_scale:,} scale:")
        print(f"  Trinity/Unity: {final['trinity_dominance']:.6f}")
        print(f"  Gap 26 projection: {final['gap26_projection']:.6f}")
        print(f"  Gap 26 phase 0: {final['gap26_phase0']}")
        print(f"  Fibonacci syncs: {final['fibonacci_syncs']}")
        
        if '30/10' in final['interference_ratios']:
            ratio = final['interference_ratios']['30/10']
            print(f"  Gap 30/10: {ratio:.6f}")
            if abs(ratio - 5/8) < 0.01:
                print(f"    → EXACT Fibonacci ratio 5/8!")
    else:
        print("No scale checkpoints were reached; try a higher PRIME_LIMIT or adjust SCALE_CHECKPOINTS.")

if __name__ == "__main__":
    run_100b_analysis()
