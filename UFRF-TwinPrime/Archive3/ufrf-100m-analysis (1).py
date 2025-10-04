#!/usr/bin/env python3
"""
UFRF PRIME ANALYSIS - HYPERDIMENSIONAL OVERLAP
Testing overlapping prime phase spaces and interference patterns
Each prime creates its own phase space - all operate simultaneously
"""

import numpy as np
import time
import json
from datetime import datetime
from collections import defaultdict, Counter
import math
import sys
import os

# ============= CONFIGURATION =============
PRIME_LIMIT = 100_000_000  # 100 million (can be overridden by env var PRIME_LIMIT or CLI)
ANALYZE_PHASE_OVERLAP = True  # Analyze overlapping prime phase spaces
TRACK_INTERFERENCE = True  # Track multi-prime interference

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

# ============= HYPERDIMENSIONAL ANALYSIS =============
class HyperdimensionalAnalyzer:
    """Analyze overlapping prime phase spaces"""
    
    def __init__(self):
        self.primes = []
        self.gap_data = defaultdict(list)
        self.phase_data = defaultdict(lambda: defaultdict(int))
        self.phase_space_overlaps = defaultdict(lambda: defaultdict(int))
        self.interference_patterns = {}
        self.results = {}
        
    def calculate_phase_space_position(self, value, base_prime):
        """Calculate position in a prime's phase space"""
        if base_prime == 1:  # Linear space
            return value
        elif base_prime == 2:  # Binary log space
            return math.log2(value) if value > 0 else 0
        elif base_prime == 3:  # Ternary log space
            return math.log(value) / math.log(3) if value > 0 else 0
        else:  # General prime log space
            return math.log(value) / math.log(base_prime) if value > 0 else 0
    
    def analyze_overlapping_phase_spaces(self, primes):
        """Analyze how gaps manifest in overlapping prime phase spaces"""
        self.primes = primes
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analyzing overlapping phase spaces...")
        
        # Key gaps to analyze
        target_gaps = [2, 4, 6, 10, 14, 22, 26, 34, 46, 58, 62, 106, 338]
        
        # For each prime that creates a phase space
        base_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        
        # Sample of primes to check (can't do all for memory)
        sample_size = min(10000, len(primes))
        sample_indices = np.linspace(0, len(primes)-2, sample_size, dtype=int)
        
        overlap_matrix = defaultdict(lambda: defaultdict(int))
        
        for idx in sample_indices:
            p1 = primes[idx]
            p2 = primes[idx + 1]
            gap = p2 - p1
            
            if gap in target_gaps:
                # Check position in each base prime's phase space
                phase_positions = {}
                
                for base in base_primes:
                    # Position in base's phase space
                    pos1 = self.calculate_phase_space_position(p1, base)
                    pos2 = self.calculate_phase_space_position(p2, base)
                    
                    # Phase within that space's 13-cycle
                    phase1 = int((pos1 * 13) % 13)
                    phase2 = int((pos2 * 13) % 13)
                    
                    phase_positions[base] = (phase1, phase2)
                    
                    # Track which phases this gap occurs at in each space
                    self.phase_space_overlaps[gap][f"base_{base}_phase_{phase1}"] += 1
                
                # Check for phase agreements (multiple spaces align)
                phase_values = [phases[0] for phases in phase_positions.values()]
                if len(set(phase_values)) <= 3:  # At least 3 spaces agree
                    overlap_matrix[gap]['high_agreement'] += 1
                else:
                    overlap_matrix[gap]['low_agreement'] += 1
        
        self.results['phase_space_overlaps'] = dict(overlap_matrix)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Phase space overlap analysis complete")
    
    def analyze_gap_channels(self, primes):
        """Each prime creates a 'channel' at gap 2×prime"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analyzing prime-created gap channels...")
        
        # Count all gaps
        all_gaps = Counter()
        gap_to_prime_map = defaultdict(list)
        
        for i in range(len(primes) - 1):
            gap = primes[i + 1] - primes[i]
            all_gaps[gap] += 1
            
            # Map gaps to their prime factors (gap = 2×prime for prime channels)
            if gap % 2 == 0:
                half_gap = gap // 2
                if half_gap in primes[:100]:  # Check if it's a prime channel
                    gap_to_prime_map[gap].append(half_gap)
                    self.gap_data[gap].append(primes[i])
        
        # Analyze strength of each prime's channel
        channel_strengths = {}
        for prime in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
            gap = 2 * prime
            count = all_gaps.get(gap, 0)
            density = count / len(primes) if primes else 0
            
            channel_strengths[prime] = {
                'gap': gap,
                'count': count,
                'density': density,
                'strength': count / prime  # Normalized by prime value
            }
        
        self.results['channel_strengths'] = channel_strengths
        
        # Find which channels dominate
        sorted_channels = sorted(channel_strengths.items(), 
                               key=lambda x: x[1]['count'], 
                               reverse=True)
        
        self.results['dominant_channels'] = {
            'top_3': [(p, data['gap'], data['count']) 
                     for p, data in sorted_channels[:3]]
        }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Gap channel analysis complete")
    
    def analyze_interference_patterns(self, primes):
        """Analyze interference between multiple prime phase spaces"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analyzing interference patterns...")
        
        # Key gaps and their prime decomposition
        gap_structures = {
            2: [1],      # 2×1 (unity channel)
            6: [3],      # 2×3 (trinity channel)  
            26: [13],    # 2×13 (cycle channel)
            10: [5],     # 2×5 (pentagon channel)
            14: [7],     # 2×7 (heptagon channel)
            22: [11],    # 2×11 (hendecagon channel)
            30: [3, 5],  # 2×3×5 (trinity×pentagon interference)
            42: [3, 7],  # 2×3×7 (trinity×heptagon interference)
            66: [3, 11], # 2×3×11 (trinity×hendecagon interference)
            78: [3, 13], # 2×3×13 (trinity×cycle interference)
        }
        
        interference_results = {}
        
        for gap, prime_factors in gap_structures.items():
            gap_count = sum(1 for i in range(len(primes)-1) 
                          if primes[i+1] - primes[i] == gap)
            
            if len(prime_factors) == 1:
                # Single channel
                interference_results[gap] = {
                    'type': 'single_channel',
                    'channel': prime_factors[0],
                    'count': gap_count,
                    'density': gap_count / len(primes) if primes else 0
                }
            else:
                # Interference between channels
                interference_results[gap] = {
                    'type': 'interference',
                    'channels': prime_factors,
                    'count': gap_count,
                    'density': gap_count / len(primes) if primes else 0,
                    'interference_ratio': gap_count / (sum(prime_factors) * 100)  # Normalized
                }
        
        self.interference_patterns = interference_results
        self.results['interference'] = interference_results
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Interference analysis complete")
    
    def analyze_standard_gaps(self, primes):
        """Standard gap analysis with 13-cycle phases"""
        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Analyzing standard gap patterns...")
        
        # Primary gaps
        target_gaps = [2, 4, 6, 10, 14, 22, 26, 34, 46, 58, 62, 106, 338]
        
        # Count gaps and phases
        for i in range(len(primes) - 1):
            gap = primes[i + 1] - primes[i]
            
            if gap in target_gaps:
                self.gap_data[gap].append(primes[i])
                phase = primes[i] % 13
                self.phase_data[gap][phase] += 1
        
        # Calculate statistics
        self.results['gaps'] = {}
        
        for gap in target_gaps:
            count = len(self.gap_data[gap])
            density = count / len(primes) if primes else 0
            
            self.results['gaps'][gap] = {
                'count': count,
                'density': density,
                'phase_distribution': dict(self.phase_data[gap])
            }
            
            # Chi-squared test
            if count > 0:
                expected = count / 13
                chi_squared = sum((self.phase_data[gap].get(p, 0) - expected)**2 / expected 
                                for p in range(13) if expected > 0)
                self.results['gaps'][gap]['chi_squared'] = chi_squared
                
                # Phase 0 and 11
                self.results['gaps'][gap]['phase_0_count'] = self.phase_data[gap].get(0, 0)
                self.results['gaps'][gap]['phase_11_count'] = self.phase_data[gap].get(11, 0)
        
        # Trinity dominance check
        gap2 = self.results['gaps'][2]['count']
        gap6 = self.results['gaps'][6]['count']
        gap26 = self.results['gaps'][26]['count']
        
        self.results['dominance'] = {
            'gap6_to_gap2': gap6 / gap2 if gap2 > 0 else 0,
            'trinity_dominates': gap6 > gap2
        }
        
        # Projection factor for gap 26
        if gap26 > 0:
            theoretical = 2/13
            observed = self.results['gaps'][26]['density']
            self.results['projection'] = {
                'theoretical': theoretical,
                'observed': observed,
                'factor': observed / theoretical,
                'binary_levels': math.log2(theoretical / observed) if observed > 0 else 0
            }
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Standard gap analysis complete")
    
    def generate_report(self):
        """Generate comprehensive report"""
        lines = []
        lines.append("=" * 80)
        lines.append("HYPERDIMENSIONAL PRIME ANALYSIS - OVERLAPPING PHASE SPACES")
        lines.append(f"Generated: {datetime.now()}")
        lines.append("=" * 80)
        
        lines.append(f"\nCONFIGURATION:")
        lines.append(f"  Prime limit: {self.primes[-1]:,}")
        lines.append(f"  Total primes: {len(self.primes):,}")
        
        # Trinity dominance
        lines.append("\n" + "=" * 40)
        lines.append("TRINITY DOMINANCE")
        lines.append("=" * 40)
        
        gap2 = self.results['gaps'][2]
        gap6 = self.results['gaps'][6]
        
        lines.append(f"Gap=2: {gap2['count']:,} (density: {gap2['density']:.6f})")
        lines.append(f"Gap=6: {gap6['count']:,} (density: {gap6['density']:.6f})")
        lines.append(f"Ratio: {self.results['dominance']['gap6_to_gap2']:.4f}")
        
        if self.results['dominance']['trinity_dominates']:
            lines.append("*** Trinity dominates Unity ***")
        
        # Prime channels
        lines.append("\n" + "=" * 40)
        lines.append("PRIME-CREATED GAP CHANNELS")
        lines.append("=" * 40)
        
        if 'channel_strengths' in self.results:
            lines.append("Channel strengths (prime → gap = 2×prime):")
            for prime, data in sorted(self.results['channel_strengths'].items()):
                lines.append(f"  Prime {prime:2d} → Gap {data['gap']:3d}: {data['count']:,} (strength: {data['strength']:.2f})")
            
            lines.append("\nDominant channels:")
            for prime, gap, count in self.results['dominant_channels']['top_3']:
                lines.append(f"  {prime} (gap={gap}): {count:,} occurrences")
        
        # Interference patterns
        lines.append("\n" + "=" * 40)
        lines.append("INTERFERENCE PATTERNS")
        lines.append("=" * 40)
        
        if 'interference' in self.results:
            lines.append("Single channels:")
            for gap, data in self.results['interference'].items():
                if data['type'] == 'single_channel':
                    lines.append(f"  Gap {gap:2d} (prime {data['channel']}): {data['count']:,}")
            
            lines.append("\nInterference between channels:")
            for gap, data in self.results['interference'].items():
                if data['type'] == 'interference':
                    channels_str = '×'.join(map(str, data['channels']))
                    lines.append(f"  Gap {gap:2d} ({channels_str}): {data['count']:,} (ratio: {data['interference_ratio']:.4f})")
        
        # Phase space overlaps
        lines.append("\n" + "=" * 40)
        lines.append("PHASE SPACE OVERLAPS")
        lines.append("=" * 40)
        
        if 'phase_space_overlaps' in self.results:
            for gap, overlaps in self.results['phase_space_overlaps'].items():
                high = overlaps.get('high_agreement', 0)
                low = overlaps.get('low_agreement', 0)
                total = high + low
                if total > 0:
                    lines.append(f"Gap {gap}: {high}/{total} ({high/total*100:.1f}%) high phase agreement")
        
        # Gap 26 detailed
        lines.append("\n" + "=" * 40)
        lines.append("GAP=26 STRUCTURE (2×13 CYCLE)")
        lines.append("=" * 40)
        
        gap26 = self.results['gaps'][26]
        lines.append(f"Count: {gap26['count']:,}")
        lines.append(f"Phase 0: {gap26['phase_0_count']} (void: {gap26['phase_0_count'] < 5})")
        
        if 'projection' in self.results:
            proj = self.results['projection']
            lines.append(f"Projection factor: {proj['factor']:.4f} (≈1/{1/proj['factor']:.0f})")
            lines.append(f"Binary levels: {proj['binary_levels']:.2f}")
        
        # Phase distribution for gap 26
        if gap26['phase_distribution']:
            lines.append("\nPhase distribution:")
            for phase in range(13):
                count = gap26['phase_distribution'].get(phase, 0)
                pct = count / gap26['count'] * 100 if gap26['count'] > 0 else 0
                bar = '█' * int(pct/2)
                lines.append(f"  Phase {phase:2d}: {count:5d} ({pct:5.2f}%) {bar}")
        
        return "\n".join(lines)

# ============= MAIN EXECUTION =============
def _resolve_prime_limit(default_limit: int) -> int:
    """Resolve prime limit from env var PRIME_LIMIT or first CLI arg."""
    # Environment variable takes precedence
    env_val = os.environ.get("PRIME_LIMIT")
    if env_val:
        try:
            return int(env_val.replace("_", ""))
        except ValueError:
            pass
    # CLI: allow --limit N or positional N
    args = sys.argv[1:]
    # Try --limit style
    if "--limit" in args:
        try:
            idx = args.index("--limit")
            return int(str(args[idx + 1]).replace("_", ""))
        except Exception:
            pass
    # Try positional first arg
    if len(args) >= 1:
        try:
            return int(str(args[0]).replace("_", ""))
        except ValueError:
            pass
    return default_limit


def run_hyperdimensional_analysis(limit=None):
    """Execute complete hyperdimensional analysis"""
    if limit is None:
        limit = _resolve_prime_limit(PRIME_LIMIT)
    
    print("\n" + "=" * 80)
    print("HYPERDIMENSIONAL PRIME ANALYSIS")
    print("Each prime creates overlapping phase spaces")
    print("=" * 80)
    
    start_time = time.time()
    
    # Generate primes
    generator = EfficientPrimeGenerator(limit)
    primes = generator.generate()
    
    # Run analysis
    analyzer = HyperdimensionalAnalyzer()
    analyzer.analyze_standard_gaps(primes)
    analyzer.analyze_gap_channels(primes)
    analyzer.analyze_interference_patterns(primes)
    
    if ANALYZE_PHASE_OVERLAP:
        analyzer.analyze_overlapping_phase_spaces(primes)
    
    # Generate report
    report = analyzer.generate_report()
    
    # Save outputs
    # Output filenames (both unsuffixed and suffixed with PRIME_LIMIT)
    suffix = f"_{limit}"
    report_unsuffixed = 'hyperdimensional_report.txt'
    report_suffixed = f'hyperdimensional_report{suffix}.txt'
    with open(report_unsuffixed, 'w') as f:
        f.write(report)
    with open(report_suffixed, 'w') as f:
        f.write(report)
    
    # Create summary for Claude
    summary = {
        'timestamp': datetime.now().isoformat(),
        'prime_limit': limit,
        'total_primes': len(primes),
        'trinity_dominance': analyzer.results['dominance'],
        'gap_26': {
            'count': analyzer.results['gaps'][26]['count'],
            'density': analyzer.results['gaps'][26]['density'],
            'phase_0': analyzer.results['gaps'][26]['phase_0_count'],
            'projection_factor': analyzer.results.get('projection', {}).get('factor', 0)
        },
        'channel_strengths': {
            p: data['count'] for p, data in analyzer.results.get('channel_strengths', {}).items()
        },
        'interference_patterns': {
            gap: {'count': data['count'], 'type': data['type']}
            for gap, data in analyzer.results.get('interference', {}).items()
        },
        'phase_overlaps': analyzer.results.get('phase_space_overlaps', {})
    }
    
    results_unsuffixed = 'results_for_claude.json'
    results_suffixed = f'results_for_claude{suffix}.json'
    with open(results_unsuffixed, 'w') as f:
        json.dump(summary, f, indent=2)
    with open(results_suffixed, 'w') as f:
        json.dump(summary, f, indent=2)
    
    # Print report
    print(report)
    
    elapsed = time.time() - start_time
    print(f"\n" + "=" * 40)
    print(f"Runtime: {elapsed:.2f} seconds")
    print("\nFiles generated:")
    print(f"  {report_unsuffixed} - Full report")
    print(f"  {report_suffixed} - Full report (suffixed)")
    print(f"  {results_unsuffixed} - Copy this back!")
    print(f"  {results_suffixed} - Copy this back! (suffixed)")
    print("=" * 40)

if __name__ == "__main__":
    run_hyperdimensional_analysis()
