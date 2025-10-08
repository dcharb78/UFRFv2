
import numpy as np, matplotlib.pyplot as plt
from CODE.smith_chart import smith_background

def plot_reflection_overlays(path_bg, s_full, title):
    fig, ax = plt.subplots(figsize=(6,6))
    smith_background(ax)
    ax.plot(s_full.real, s_full.imag, marker='.', linewidth=0.7, markersize=2)
    ax.set_title(title)
    plt.tight_layout(); plt.savefig(path_bg, dpi=150, bbox_inches="tight"); plt.close()

def plot_transmission_mag(path_png, freqs, s, title):
    fig = plt.figure(figsize=(8,4.5))
    plt.plot(freqs/1e9, 20*np.log10(np.abs(s)))
    plt.xlabel("Frequency (GHz)"); plt.ylabel("|S| (dB)")
    plt.title(title); plt.grid(True, which="both")
    plt.tight_layout(); plt.savefig(path_png, dpi=150, bbox_inches="tight"); plt.close()

def plot_test_overlays_reflection(path_smith_png, path_mag_png, freqs, s_meas, s_base, s_uf):
    fig, ax = plt.subplots(figsize=(6,6))
    smith_background(ax)
    ax.scatter(s_meas.real, s_meas.imag, s=25, label="Measured (test)")
    ax.scatter(s_base.real, s_base.imag, s=25, marker='x', label="Baseline")
    ax.scatter(s_uf.real, s_uf.imag, s=25, marker='^', label="UFRF prior")
    ax.legend(); ax.set_title("Test-set Γ — measured vs models")
    plt.tight_layout(); plt.savefig(path_smith_png, dpi=150, bbox_inches="tight"); plt.close()
    fig = plt.figure(figsize=(8,4.5))
    plt.plot(freqs/1e9, 20*np.log10(np.abs(s_meas)), marker='o', linestyle='none', label="Measured (test)")
    plt.plot(freqs/1e9, 20*np.log10(np.abs(s_base)), marker='x', linestyle='none', label="Baseline")
    plt.plot(freqs/1e9, 20*np.log10(np.abs(s_uf)), marker='^', linestyle='none', label="UFRF prior")
    plt.xlabel("Frequency (GHz)"); plt.ylabel("|S| (dB)")
    plt.title("Test-set |S| (dB) — measured vs models")
    plt.grid(True, which="both"); plt.legend()
    plt.tight_layout(); plt.savefig(path_mag_png, dpi=150, bbox_inches="tight"); plt.close()

def plot_test_overlays_transmission(path_cmp_png, path_mag_png, freqs, s_meas, s_base, s_uf):
    fig = plt.figure(figsize=(6,6))
    plt.scatter(s_meas.real, s_meas.imag, s=25, label="Measured (test)")
    plt.scatter(s_base.real, s_base.imag, s=25, marker='x', label="Baseline")
    plt.scatter(s_uf.real, s_uf.imag, s=25, marker='^', label="UFRF prior")
    plt.xlabel("Re(Sij)"); plt.ylabel("Im(Sij)")
    plt.title("Test-set Sij — measured vs models"); plt.legend()
    plt.tight_layout(); plt.savefig(path_cmp_png, dpi=150, bbox_inches="tight"); plt.close()
    fig = plt.figure(figsize=(8,4.5))
    plt.plot(freqs/1e9, 20*np.log10(np.abs(s_meas)), marker='o', linestyle='none', label="Measured (test)")
    plt.plot(freqs/1e9, 20*np.log10(np.abs(s_base)), marker='x', linestyle='none', label="Baseline")
    plt.plot(freqs/1e9, 20*np.log10(np.abs(s_uf)), marker='^', linestyle='none', label="UFRF prior")
    plt.xlabel("Frequency (GHz)"); plt.ylabel("|S| (dB)")
    plt.title("Test-set |S| (dB) — measured vs models")
    plt.grid(True, which="both"); plt.legend()
    plt.tight_layout(); plt.savefig(path_mag_png, dpi=150, bbox_inches="tight"); plt.close()
