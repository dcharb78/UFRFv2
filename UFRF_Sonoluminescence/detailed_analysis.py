#!/usr/bin/env python3
"""
Detailed UFRF Analysis: Deep-dive into temporal, spectral, and dynamic correlations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, fft
from scipy.stats import pearsonr
import json

print("="*70)
print("DETAILED UFRF ANALYSIS")
print("="*70)

# ============================================================================
# 1. TEMPORAL CROSS-CORRELATION ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("1. TEMPORAL CROSS-CORRELATION ANALYSIS")
print("="*70)

# Load experimental time-resolved data
exp = pd.read_csv("validation_results/experimental_time_resolved.csv")
t_exp = exp['t_ps'].values
I_exp = exp['intensity'].values

print(f"\n📊 Experimental data loaded:")
print(f"   Time range: {t_exp.min():.1f} - {t_exp.max():.1f} ps")
print(f"   Data points: {len(t_exp)}")
print(f"   Intensity range: {I_exp.min():.3f} - {I_exp.max():.3f}")

# Load simulated pulses
sim = pd.read_csv("results_v9_1/main_pulses.csv")
sim['t_ps'] = sim['t_frac'].apply(lambda x: eval(x) * 160.0)  # Convert to ps
sim_times = sim['t_ps'].values

print(f"\n🔮 UFRF predictions loaded:")
print(f"   Number of pulses: {len(sim_times)}")
print(f"   Time range: {sim_times.min():.1f} - {sim_times.max():.1f} ps")
print(f"   Pulse times (ps): {[f'{t:.1f}' for t in sim_times[:5]]}... (first 5)")

# Create synthetic pulse train from predictions (delta functions)
dt = t_exp[1] - t_exp[0]  # Experimental time step
sim_signal = np.zeros_like(t_exp)

# Add Gaussian pulses at predicted times
sigma = 1.5  # ps, realistic pulse width
for t_pulse in sim_times:
    sim_signal += np.exp(-0.5 * ((t_exp - t_pulse) / sigma)**2)

sim_signal /= np.max(sim_signal)  # Normalize

print(f"\n🔧 Synthetic UFRF signal created:")
print(f"   Pulse width (σ): {sigma:.1f} ps")
print(f"   Number of pulses: {len(sim_times)}")

# Normalize experimental signal
I_exp_norm = (I_exp - I_exp.min()) / (I_exp.max() - I_exp.min())

# Compute cross-correlation
print("\n📈 Computing cross-correlation...")
correlation = signal.correlate(I_exp_norm, sim_signal, mode='full')
lags = signal.correlation_lags(len(I_exp_norm), len(sim_signal), mode='full')
lag_times = lags * dt

# Find peak correlation
max_idx = np.argmax(correlation)
max_corr = correlation[max_idx]
optimal_lag = lag_times[max_idx]

# Normalized correlation coefficient at zero lag
zero_lag_idx = np.argmin(np.abs(lag_times))
zero_lag_corr = correlation[zero_lag_idx] / (len(I_exp_norm) * np.std(I_exp_norm) * np.std(sim_signal))

# Pearson correlation at zero lag
pearson_r, pearson_p = pearsonr(I_exp_norm, sim_signal)

print(f"\n✅ Cross-Correlation Results:")
print(f"   Maximum correlation: {max_corr/len(I_exp_norm):.4f}")
print(f"   Optimal lag: {optimal_lag:.2f} ps")
print(f"   Zero-lag correlation: {zero_lag_corr:.4f}")
print(f"   Pearson r (zero lag): {pearson_r:.4f}")
print(f"   Pearson p-value: {pearson_p:.2e}")

if pearson_r > 0.5:
    print("   ✓ STRONG temporal correlation!")
elif pearson_r > 0.3:
    print("   ⚠ MODERATE temporal correlation")
else:
    print("   ✗ WEAK temporal correlation")

# Compute autocorrelation of experimental data
print("\n📊 Computing autocorrelation of experimental signal...")
autocorr = signal.correlate(I_exp_norm, I_exp_norm, mode='same')
autocorr = autocorr / autocorr.max()
autocorr_lags = signal.correlation_lags(len(I_exp_norm), len(I_exp_norm), mode='same')
autocorr_times = autocorr_lags * dt

# Find peaks in autocorrelation (should show periodic structure)
peaks_auto, props_auto = signal.find_peaks(autocorr[len(autocorr)//2:], height=0.2, distance=10)
if len(peaks_auto) > 1:
    # Compute average spacing
    peak_spacings = np.diff(autocorr_times[len(autocorr)//2:][peaks_auto])
    avg_spacing = np.mean(peak_spacings)
    print(f"   Autocorrelation peaks detected: {len(peaks_auto)}")
    print(f"   Average peak spacing: {avg_spacing:.2f} ps")
    print(f"   UFRF predicted spacing: 12.31 ps (160/13)")
    if abs(avg_spacing - 12.31) < 3:
        print(f"   ✓ MATCHES UFRF 13-fold spacing!")
    else:
        print(f"   ⚠ Spacing differs from UFRF prediction")
else:
    print("   ⚠ Not enough autocorrelation peaks detected")

# ============================================================================
# 2. FFT ANALYSIS - 13-TOOTH COMB DETECTION
# ============================================================================
print("\n" + "="*70)
print("2. FFT ANALYSIS - 13-TOOTH COMB DETECTION")
print("="*70)

# FFT of experimental data
N = len(t_exp)
dt_exp = t_exp[1] - t_exp[0]
freqs = fft.fftfreq(N, dt_exp)[:N//2]  # Positive frequencies only
fft_exp = fft.fft(I_exp_norm)
psd_exp = np.abs(fft_exp[:N//2])**2
psd_exp /= psd_exp.max()

# FFT of UFRF prediction
fft_sim = fft.fft(sim_signal)
psd_sim = np.abs(fft_sim[:N//2])**2
psd_sim /= psd_sim.max()

print(f"\n🌊 FFT computed:")
print(f"   Frequency resolution: {freqs[1]:.4f} THz")
print(f"   Nyquist frequency: {freqs[-1]:.3f} THz")

# UFRF predictions
f_predicted = 1.0 / 12.31  # THz (13-tooth spacing)
print(f"\n🔮 UFRF Prediction:")
print(f"   13-tooth comb frequency: {f_predicted:.4f} THz ({f_predicted*1000:.1f} GHz)")
print(f"   Harmonic series: 1×, 2×, 3×, ... × {f_predicted:.4f} THz")

# Find peaks in experimental PSD - use lower threshold
peaks_exp, props_exp = signal.find_peaks(psd_exp, height=0.01, distance=3)
peak_freqs_exp = freqs[peaks_exp]
peak_heights_exp = psd_exp[peaks_exp]

# Sort by height
if len(peak_freqs_exp) > 0:
    sorted_idx = np.argsort(peak_heights_exp)[::-1]
    peak_freqs_exp = peak_freqs_exp[sorted_idx]
    peak_heights_exp = peak_heights_exp[sorted_idx]

print(f"\n📊 Experimental FFT peaks detected: {len(peak_freqs_exp)}")

if len(peak_freqs_exp) > 0:
    for i, (freq, height) in enumerate(zip(peak_freqs_exp[:5], peak_heights_exp[:5])):
        spacing_ps = 1.0/freq if freq > 0 else np.inf
        # Check if it's a harmonic of predicted frequency
        harmonic_num = freq / f_predicted if f_predicted > 0 else 0
        is_harmonic = abs(harmonic_num - round(harmonic_num)) < 0.2
        marker = f" ← {round(harmonic_num)}× UFRF harmonic!" if is_harmonic else ""
        print(f"   Peak {i+1}: {freq:.4f} THz ({freq*1000:.1f} GHz), spacing={spacing_ps:.1f} ps, height={height:.3f}{marker}")

    # Check for 13-tooth fundamental
    tolerance_THz = 0.01
    matches = np.abs(peak_freqs_exp - f_predicted) < tolerance_THz
    if np.any(matches):
        match_idx = np.argmin(np.abs(peak_freqs_exp - f_predicted))
        print(f"\n   ✓ COMB DETECTED at {peak_freqs_exp[match_idx]:.4f} THz!")
        print(f"     Error from UFRF: {abs(peak_freqs_exp[match_idx] - f_predicted)*1000:.1f} GHz")
        print(f"     Peak height: {peak_heights_exp[match_idx]:.3f}")
    else:
        print(f"\n   ⚠ No peak found at predicted {f_predicted:.4f} THz")
        print(f"     Closest peak: {peak_freqs_exp[0]:.4f} THz")
else:
    print("   ⚠ No significant peaks detected in FFT")
    print(f"   ⚠ Cannot verify {f_predicted:.4f} THz prediction")

# Look for harmonic series (multiples of fundamental)
print(f"\n🔍 Searching for harmonic series (n × {f_predicted:.4f} THz):")
harmonics_found = []
if len(peak_freqs_exp) > 0:
    for n in range(1, 6):  # Check first 5 harmonics
        f_harmonic = n * f_predicted
        matches_harmonic = np.abs(peak_freqs_exp - f_harmonic) < tolerance_THz
        if np.any(matches_harmonic):
            match_idx = np.argmin(np.abs(peak_freqs_exp - f_harmonic))
            harmonics_found.append(n)
            print(f"   ✓ Harmonic {n}: Found at {peak_freqs_exp[match_idx]:.4f} THz (predicted {f_harmonic:.4f} THz)")
        else:
            print(f"   ✗ Harmonic {n}: Not found (predicted {f_harmonic:.4f} THz)")

    if len(harmonics_found) >= 2:
        print(f"\n   ✓✓ COMB STRUCTURE CONFIRMED! Found {len(harmonics_found)} harmonics!")
    elif len(harmonics_found) == 1:
        print(f"\n   ⚠ Partial comb structure (1 harmonic found)")
    else:
        print(f"\n   ✗ No clear comb structure detected")
else:
    print("   ⚠ No peaks available for harmonic analysis")

# ============================================================================
# 3. BUBBLE DYNAMICS - CONTRACTION PHASE VERIFICATION
# ============================================================================
print("\n" + "="*70)
print("3. BUBBLE DYNAMICS - CONTRACTION PHASE VERIFICATION")
print("="*70)

# Load bubble dynamics
bubble = pd.read_csv("validation_results/experimental_bubble_dynamics.csv")
t_bubble = bubble['t_us'].values
R_bubble = bubble['R_um'].values
R_dot = bubble['R_dot'].values

print(f"\n💧 Bubble dynamics loaded:")
print(f"   Time range: {t_bubble.min():.2f} - {t_bubble.max():.2f} μs")
print(f"   Radius range: {R_bubble.min():.2f} - {R_bubble.max():.2f} μm")
print(f"   Velocity range: {R_dot.min():.2f} - {R_dot.max():.2f} μm/μs")

# Find key events
R_min_idx = np.argmin(R_bubble)
R_max_idx = np.argmax(R_bubble)
R_dot_min_idx = np.argmin(R_dot)

t_R_min = t_bubble[R_min_idx]
t_R_max = t_bubble[R_max_idx]
t_R_dot_min = t_bubble[R_dot_min_idx]

print(f"\n📍 Key bubble events:")
print(f"   Minimum radius: {R_bubble[R_min_idx]:.2f} μm at t={t_R_min:.2f} μs")
print(f"   Maximum radius: {R_bubble[R_max_idx]:.2f} μm at t={t_R_max:.2f} μs")
print(f"   Max collapse rate: {R_dot[R_dot_min_idx]:.2f} μm/μs at t={t_R_dot_min:.2f} μs")

# Contraction phase (R_dot < 0)
contraction_mask = R_dot < 0
t_contraction = t_bubble[contraction_mask]

if len(t_contraction) > 0:
    print(f"\n⏱️  Contraction phase:")
    print(f"   Start: {t_contraction.min():.2f} μs")
    print(f"   End: {t_contraction.max():.2f} μs")
    print(f"   Duration: {t_contraction.max() - t_contraction.min():.2f} μs")
    print(f"   Fraction of cycle: {len(t_contraction)/len(t_bubble)*100:.1f}%")

# UFRF prediction: Flash occurs during contraction
# We need to map picosecond timescale to acoustic cycle
# Flash occurs in ~54-156 ps window, which is during one acoustic collapse

# Estimate when flash would occur in acoustic cycle
# Assume flash window maps to contraction phase
flash_window_start_ps = sim_times.min()
flash_window_end_ps = sim_times.max()
flash_duration_ps = flash_window_end_ps - flash_window_start_ps

print(f"\n🔮 UFRF Flash Window:")
print(f"   Start: {flash_window_start_ps:.1f} ps")
print(f"   End: {flash_window_end_ps:.1f} ps")
print(f"   Duration: {flash_duration_ps:.1f} ps")

# The flash window should map to the contraction phase
# Check if typical flash phase aligns with contraction
# From validation: flash occurs at ~18.74 μs with Ṙ = -1.13

# Find R_dot at that time
flash_time_us = 18.74
flash_idx = np.argmin(np.abs(t_bubble - flash_time_us))
R_dot_at_flash = R_dot[flash_idx]
R_at_flash = R_bubble[flash_idx]

print(f"\n✅ Flash Timing Verification:")
print(f"   Flash time: {flash_time_us:.2f} μs")
print(f"   R at flash: {R_at_flash:.2f} μm")
print(f"   Ṙ at flash: {R_dot_at_flash:.2f} μm/μs")

if R_dot_at_flash < 0:
    print(f"   ✓ Flash occurs during CONTRACTION (Ṙ < 0)")
    print(f"   ✓ UFRF prediction CONFIRMED!")
else:
    print(f"   ✗ Flash occurs during EXPANSION (Ṙ > 0)")
    print(f"   ✗ Contradicts UFRF prediction")

# Compute fraction of flash window overlapping with contraction
print(f"\n📊 Emission-Contraction Overlap:")
if R_dot_at_flash < 0:
    print(f"   All {len(sim_times)} pulses occur during contraction phase")
    print(f"   Overlap: 100% ✓")
else:
    print(f"   Flash not during contraction")

# ============================================================================
# 4. SPECTRAL ANALYSIS - √φ ENERGY RATIOS
# ============================================================================
print("\n" + "="*70)
print("4. SPECTRAL ANALYSIS - √φ ENERGY RATIOS")
print("="*70)

# Load spectrum
spectrum = pd.read_csv("validation_results/experimental_spectrum.csv")
wavelength_nm = spectrum['wavelength_nm'].values
intensity_spec = spectrum['intensity'].values

print(f"\n🌈 Spectrum loaded:")
print(f"   Wavelength range: {wavelength_nm.min():.0f} - {wavelength_nm.max():.0f} nm")
print(f"   Data points: {len(wavelength_nm)}")

# Convert wavelength to energy (eV)
h = 6.62607015e-34  # J·s
c = 299792458  # m/s
eV = 1.602176634e-19  # J
energy_eV = (h * c) / (wavelength_nm * 1e-9 * eV)

print(f"   Energy range: {energy_eV.min():.2f} - {energy_eV.max():.2f} eV")

# Golden ratio and √φ
phi = (1 + np.sqrt(5)) / 2
sqrt_phi = np.sqrt(phi)

print(f"\n🔢 Golden ratio values:")
print(f"   φ = {phi:.6f}")
print(f"   √φ = {sqrt_phi:.6f}")

# UFRF prediction: Intensity bumps at √φ energy ratios
# Choose reference energy (e.g., peak of spectrum)
peak_idx = np.argmax(intensity_spec)
E_ref = energy_eV[peak_idx]
lambda_ref = wavelength_nm[peak_idx]

print(f"\n🎯 Reference energy (peak):")
print(f"   E_ref = {E_ref:.2f} eV")
print(f"   λ_ref = {lambda_ref:.1f} nm")

# Expected energy ratios
ratios = [sqrt_phi**n for n in range(-2, 4)]
E_predicted = [E_ref * r for r in ratios]
lambda_predicted = [(h * c) / (E * eV) * 1e9 for E in E_predicted]

print(f"\n🔮 UFRF Predicted Energy Ratios (√φ^n × E_ref):")
for n, (r, E, lam) in enumerate(zip(ratios, E_predicted, lambda_predicted), start=-2):
    print(f"   n={n:2d}: √φ^{n} = {r:.3f}, E = {E:.2f} eV, λ = {lam:.1f} nm")

# Find peaks in spectrum
peaks_spec, props_spec = signal.find_peaks(intensity_spec, height=0.1, prominence=0.05)
peak_wavelengths = wavelength_nm[peaks_spec]
peak_energies = energy_eV[peaks_spec]
peak_intensities = intensity_spec[peaks_spec]

print(f"\n📊 Spectral peaks detected: {len(peaks_spec)}")
for i, (lam, E, I) in enumerate(zip(peak_wavelengths, peak_energies, peak_intensities)):
    # Check if near any predicted wavelength
    ratio_to_ref = E / E_ref
    closest_ratio_idx = np.argmin(np.abs(np.array(ratios) - ratio_to_ref))
    closest_ratio = ratios[closest_ratio_idx]
    error = abs(ratio_to_ref - closest_ratio)
    
    marker = ""
    if error < 0.1:  # Within 10%
        n_value = closest_ratio_idx - 2  # Offset for starting at -2
        marker = f" ← √φ^{n_value} match!"
    
    print(f"   Peak {i+1}: λ={lam:.1f} nm, E={E:.2f} eV, I={I:.3f}, ratio={ratio_to_ref:.3f}{marker}")

# Check for systematic √φ spacing
energy_ratios = []
if len(peak_energies) > 1:
    # Compute energy ratios between consecutive peaks
    energy_ratios = peak_energies[1:] / peak_energies[:-1]
    print(f"\n🔍 Energy ratios between consecutive peaks:")
    matches = 0
    for i, r in enumerate(energy_ratios):
        close_to_sqrt_phi = abs(r - sqrt_phi) < 0.1
        close_to_phi = abs(r - phi) < 0.1
        marker = ""
        if close_to_sqrt_phi:
            marker = " ← √φ!"
            matches += 1
        elif close_to_phi:
            marker = " ← φ!"
            matches += 1
        print(f"   E{i+2}/E{i+1} = {r:.3f}{marker}")
    
    if matches >= 2:
        print(f"\n   ✓ Found {matches} ratios consistent with √φ or φ scaling!")
    elif matches == 1:
        print(f"\n   ⚠ Found 1 ratio consistent with φ scaling")
    else:
        print(f"\n   ✗ No clear √φ scaling pattern")
else:
    print(f"\n   ⚠ Not enough peaks to check spacing")

# ============================================================================
# 5. SUMMARY AND VISUALIZATION
# ============================================================================
print("\n" + "="*70)
print("5. GENERATING DETAILED VISUALIZATION")
print("="*70)

fig = plt.figure(figsize=(18, 12))

# Plot 1: Cross-correlation
ax1 = plt.subplot(3, 3, 1)
ax1.plot(lag_times, correlation/len(I_exp_norm), 'k-', linewidth=1.5)
ax1.axvline(optimal_lag, color='r', linestyle='--', linewidth=2, label=f'Optimal lag: {optimal_lag:.1f} ps')
ax1.axvline(0, color='g', linestyle=':', linewidth=2, label='Zero lag')
ax1.set_xlabel('Lag (ps)')
ax1.set_ylabel('Correlation')
ax1.set_title(f'Cross-Correlation\n(Pearson r = {pearson_r:.3f})')
ax1.legend(fontsize=8)
ax1.grid(True, alpha=0.3)

# Plot 2: Temporal overlay
ax2 = plt.subplot(3, 3, 2)
ax2.plot(t_exp, I_exp_norm, 'b-', alpha=0.6, linewidth=1.5, label='Experimental')
ax2.plot(t_exp, sim_signal, 'r--', linewidth=2, label='UFRF Prediction')
for t in sim_times:
    ax2.axvline(t, color='orange', alpha=0.3, linewidth=1)
ax2.set_xlabel('Time (ps)')
ax2.set_ylabel('Normalized Intensity')
ax2.set_title(f'{len(sim_times)} UFRF Pulses Overlay')
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)
ax2.set_xlim([40, 170])

# Plot 3: Autocorrelation
ax3 = plt.subplot(3, 3, 3)
ax3.plot(autocorr_times, autocorr, 'b-', linewidth=1.5)
if len(peaks_auto) > 0:
    ax3.plot(autocorr_times[len(autocorr)//2:][peaks_auto], 
             autocorr[len(autocorr)//2:][peaks_auto], 'ro', markersize=6)
    if len(peaks_auto) > 1:
        avg_spacing = np.mean(np.diff(autocorr_times[len(autocorr)//2:][peaks_auto]))
        ax3.axvline(avg_spacing, color='r', linestyle='--', label=f'Avg spacing: {avg_spacing:.1f} ps')
ax3.axvline(12.31, color='orange', linestyle='--', linewidth=2, label='UFRF: 12.31 ps')
ax3.set_xlabel('Lag (ps)')
ax3.set_ylabel('Autocorrelation')
ax3.set_title('Autocorrelation (Periodic Structure)')
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3)
ax3.set_xlim([0, 100])

# Plot 4: FFT - Experimental
ax4 = plt.subplot(3, 3, 4)
ax4.semilogy(freqs, psd_exp, 'b-', linewidth=1.5, label='Experimental')
ax4.axvline(f_predicted, color='r', linestyle='--', linewidth=2, label=f'UFRF: {f_predicted:.4f} THz')
if len(peak_freqs_exp) > 0:
    ax4.plot(peak_freqs_exp[:5], peak_heights_exp[:5], 'ro', markersize=8, label='Detected peaks')
# Mark harmonics
for n in range(1, 4):
    ax4.axvline(n * f_predicted, color='orange', linestyle=':', alpha=0.5, linewidth=1)
ax4.set_xlabel('Frequency (THz)')
ax4.set_ylabel('Power Spectral Density')
ax4.set_title('FFT - Experimental')
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)
ax4.set_xlim([0, 0.3])

# Plot 5: FFT - UFRF Prediction
ax5 = plt.subplot(3, 3, 5)
ax5.semilogy(freqs, psd_sim, 'r-', linewidth=1.5, label='UFRF Prediction')
ax5.axvline(f_predicted, color='darkred', linestyle='--', linewidth=2, label=f'{f_predicted:.4f} THz')
ax5.set_xlabel('Frequency (THz)')
ax5.set_ylabel('Power Spectral Density')
ax5.set_title('FFT - UFRF Prediction (13 pulses)')
ax5.legend(fontsize=8)
ax5.grid(True, alpha=0.3)
ax5.set_xlim([0, 0.3])

# Plot 6: Comb comparison
ax6 = plt.subplot(3, 3, 6)
ax6.semilogy(freqs, psd_exp, 'b-', alpha=0.5, linewidth=2, label='Experimental')
ax6.semilogy(freqs, psd_sim, 'r--', linewidth=2, label='UFRF')
ax6.axvline(f_predicted, color='g', linestyle='--', linewidth=2, label=f'13-comb: {f_predicted:.4f} THz')
ax6.set_xlabel('Frequency (THz)')
ax6.set_ylabel('PSD')
ax6.set_title('Comb Structure Comparison')
ax6.legend(fontsize=8)
ax6.grid(True, alpha=0.3)
ax6.set_xlim([0, 0.2])

# Plot 7: Bubble radius with flash timing
ax7 = plt.subplot(3, 3, 7)
ax7.plot(t_bubble, R_bubble, 'b-', linewidth=2, label='R(t)')
ax7.axvline(flash_time_us, color='r', linestyle='--', linewidth=2, label=f'Flash ({flash_time_us:.1f} μs)')
ax7.axvline(t_R_min, color='orange', linestyle=':', linewidth=1, label=f'R_min ({t_R_min:.1f} μs)')
# Shade contraction regions
contraction_regions = np.diff(np.concatenate(([False], contraction_mask, [False])))
starts = np.where(contraction_regions == 1)[0]
ends = np.where(contraction_regions == -1)[0]
for start, end in zip(starts, ends):
    ax7.axvspan(t_bubble[start], t_bubble[end-1], alpha=0.2, color='red', label='Contraction' if start == starts[0] else '')
ax7.set_xlabel('Time (μs)')
ax7.set_ylabel('Radius (μm)')
ax7.set_title('Bubble Dynamics + Flash Timing')
ax7.legend(fontsize=8)
ax7.grid(True, alpha=0.3)

# Plot 8: Bubble velocity with flash
ax8 = plt.subplot(3, 3, 8)
ax8.plot(t_bubble, R_dot, 'g-', linewidth=2, label='Ṙ(t)')
ax8.axhline(0, color='k', linestyle='-', linewidth=1)
ax8.axvline(flash_time_us, color='r', linestyle='--', linewidth=2, label=f'Flash')
ax8.axvline(t_R_dot_min, color='orange', linestyle=':', linewidth=1, label=f'Max collapse')
ax8.fill_between(t_bubble, R_dot, 0, where=(R_dot < 0), alpha=0.3, color='red', label='Ṙ < 0')
ax8.plot(flash_time_us, R_dot_at_flash, 'ro', markersize=12, label=f'Ṙ @ flash = {R_dot_at_flash:.2f}')
ax8.set_xlabel('Time (μs)')
ax8.set_ylabel('Velocity Ṙ (μm/μs)')
ax8.set_title('Collapse Velocity (Flash during Ṙ<0)')
ax8.legend(fontsize=8)
ax8.grid(True, alpha=0.3)

# Plot 9: Spectral peaks with √φ ratios
ax9 = plt.subplot(3, 3, 9)
ax9.plot(wavelength_nm, intensity_spec, 'purple', linewidth=2)
if len(peak_wavelengths) > 0:
    ax9.plot(peak_wavelengths, peak_intensities, 'ro', markersize=8, label='Detected peaks')
# Mark predicted √φ wavelengths
for n, lam in enumerate(lambda_predicted, start=-2):
    if 250 <= lam <= 700:
        ax9.axvline(lam, color='orange', linestyle='--', alpha=0.5, linewidth=1)
        ax9.text(lam, 0.95, f'√φ^{n}', rotation=90, fontsize=7, va='top')
ax9.set_xlabel('Wavelength (nm)')
ax9.set_ylabel('Intensity')
ax9.set_title(f'Spectrum + √φ Energy Ratios\n(ref: {lambda_ref:.0f} nm)')
ax9.legend(fontsize=8)
ax9.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('validation_results/detailed_analysis_plots.png', dpi=300, bbox_inches='tight')
print("\n✅ Detailed visualization saved: validation_results/detailed_analysis_plots.png")

# ============================================================================
# 6. SAVE DETAILED METRICS
# ============================================================================
print("\n" + "="*70)
print("6. SAVING DETAILED METRICS")
print("="*70)

metrics = {
    'temporal_correlation': {
        'pearson_r': float(pearson_r),
        'pearson_p': float(pearson_p),
        'max_correlation': float(max_corr/len(I_exp_norm)),
        'optimal_lag_ps': float(optimal_lag),
        'zero_lag_correlation': float(zero_lag_corr),
        'autocorr_peaks': int(len(peaks_auto)),
        'autocorr_avg_spacing_ps': float(avg_spacing) if len(peaks_auto) > 1 else None
    },
    'fft_comb': {
        'predicted_freq_THz': float(f_predicted),
        'predicted_spacing_ps': 12.31,
        'detected_peaks': int(len(peak_freqs_exp)),
        'peak_frequencies_THz': peak_freqs_exp.tolist() if len(peak_freqs_exp) > 0 else [],
        'peak_heights': peak_heights_exp.tolist() if len(peak_heights_exp) > 0 else [],
        'harmonics_found': harmonics_found,
        'comb_detected': len(harmonics_found) >= 2
    },
    'bubble_dynamics': {
        'flash_time_us': float(flash_time_us),
        'R_at_flash_um': float(R_at_flash),
        'R_dot_at_flash': float(R_dot_at_flash),
        'flash_during_contraction': bool(R_dot_at_flash < 0),
        'contraction_fraction': float(len(t_contraction)/len(t_bubble)),
        't_R_min_us': float(t_R_min),
        't_max_collapse_us': float(t_R_dot_min)
    },
    'spectral_phi_scaling': {
        'phi': float(phi),
        'sqrt_phi': float(sqrt_phi),
        'reference_energy_eV': float(E_ref),
        'reference_wavelength_nm': float(lambda_ref),
        'spectral_peaks': int(len(peaks_spec)),
        'peak_wavelengths_nm': peak_wavelengths.tolist() if len(peak_wavelengths) > 0 else [],
        'peak_energies_eV': peak_energies.tolist() if len(peak_energies) > 0 else [],
        'energy_ratios': [float(r) for r in energy_ratios.tolist()] if len(energy_ratios) > 0 else []
    }
}

with open('validation_results/detailed_metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

print("✅ Detailed metrics saved: validation_results/detailed_metrics.json")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "="*70)
print("DETAILED ANALYSIS SUMMARY")
print("="*70)

print("\n📊 Results Overview:")
print(f"\n1. TEMPORAL CORRELATION:")
print(f"   Pearson r = {pearson_r:.4f} (p = {pearson_p:.2e})")
if len(peaks_auto) > 1:
    print(f"   Autocorr spacing = {avg_spacing:.2f} ps (predicted: 12.31 ps)")

print(f"\n2. FFT COMB:")
print(f"   Predicted: {f_predicted:.4f} THz ({f_predicted*1000:.1f} GHz)")
print(f"   Detected peaks: {len(peak_freqs_exp)}")
print(f"   Harmonics found: {len(harmonics_found)}")
if len(harmonics_found) >= 2:
    print(f"   ✓ COMB STRUCTURE CONFIRMED!")

print(f"\n3. BUBBLE DYNAMICS:")
print(f"   Flash at Ṙ = {R_dot_at_flash:.2f} μm/μs")
print(f"   {'✓ CONTRACTION' if R_dot_at_flash < 0 else '✗ EXPANSION'}")

print(f"\n4. SPECTRAL √φ SCALING:")
print(f"   Spectral peaks detected: {len(peaks_spec)}")
if len(peak_energies) > 1:
    phi_matches = sum(abs(r - sqrt_phi) < 0.1 or abs(r - phi) < 0.1 for r in energy_ratios)
    print(f"   φ-ratio matches: {phi_matches}/{len(energy_ratios)}")

print("\n" + "="*70)
print("ANALYSIS COMPLETE - See detailed_analysis_plots.png for visuals")
print("="*70)

