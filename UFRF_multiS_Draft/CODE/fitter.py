
import numpy as np
from CODE.models import rlc_series_gamma, rlc_series_gamma_ufrf, fit_poly_complex_logf, predict_poly_complex_logf

def complex_mse(a, b):
    d = a - b
    return float(np.mean(d.real**2 + d.imag**2))

def train_test_split(freqs, s, test_frac=0.2, mode="random", seed=42):
    N = len(freqs); idx = np.arange(N)
    if mode=="interleave":
        step = max(5, int(1/test_frac)) if test_frac>0 else 5
        test_idx = idx[::step]
    else:
        rng = np.random.default_rng(seed)
        rng.shuffle(idx)
        n_test = max(5, int(N*test_frac))
        test_idx = np.sort(idx[:n_test])
    train_idx = np.array([i for i in idx if i not in set(test_idx)])
    return train_idx, test_idx

def fit_reflection_models(f_tr, g_tr, Z0, n_cycles=13):
    R_grid = np.linspace(1.0, 100.0, 18)
    L_grid = np.linspace(0.1e-9, 10e-9, 16)
    C_grid = np.linspace(0.2e-12, 5e-12, 16)
    best = (np.inf, None)
    for R in R_grid:
        for L in L_grid:
            for C in C_grid:
                g = rlc_series_gamma(f_tr, R, L, C, Z0)
                e = complex_mse(g, g_tr)
                if e < best[0]: best = (e, (float(R), float(L), float(C)))
    (Rb, Lb, Cb) = best[1]
    Rg = np.linspace(max(0.5, Rb*0.5), Rb*1.5, 8)
    Lg = np.linspace(max(1e-12, Lb*0.5), Lb*1.5, 8)
    Cg = np.linspace(max(1e-13, Cb*0.5), Cb*1.5, 8)
    ag = np.linspace(0, 0.2, 6); phig = np.linspace(0, 2*np.pi, 10, endpoint=False)
    best_u = (np.inf, None)
    for R in Rg:
        for L in Lg:
            for C in Cg:
                for a in ag:
                    for phi in phig:
                        g = rlc_series_gamma_ufrf(f_tr, R, L, C, Z0, a, phi, n_cycles=n_cycles)
                        e = complex_mse(g, g_tr) + 1e-4*(a**2)
                        if e < best_u[0]: best_u = (e, (float(R), float(L), float(C), float(a), float(phi)))
    return (Rb,Lb,Cb), best[0], best_u[1], best_u[0]

def fit_transmission_models(f_tr, s_tr, deg=3, n_cycles=13, ridge=1e-3):
    wr_b, wi_b, _ = fit_poly_complex_logf(f_tr, s_tr, deg=deg, ridge=0.0, add_ufrf=False)
    wr_u, wi_u, _ = fit_poly_complex_logf(f_tr, s_tr, deg=deg, ridge=ridge, add_ufrf=True, n_cycles=n_cycles, ridge_on_last2=True)
    return (wr_b, wi_b), (wr_u, wi_u)

def estimate_delay_params(freqs, s):
    """Estimate group delay tau and phase offset phi0 from complex S21/S12.

    Fits unwrapped phase as a linear function of frequency: phase(f) ≈ m*f + b,
    with tau = -m/(2*pi) and phi0 = -b.
    """
    import numpy as np
    phase = np.unwrap(np.angle(s))
    # Robust linear fit phase ~ m*f + b
    A = np.column_stack([freqs, np.ones_like(freqs)])
    m, b = np.linalg.lstsq(A, phase, rcond=None)[0]
    tau = -m/(2*np.pi)
    phi0 = -b
    return float(tau), float(phi0)

def remove_delay(freqs, s, tau, phi0):
    import numpy as np
    return s * np.exp(1j*(2*np.pi*freqs*tau + phi0))

def apply_delay(freqs, s_amp, tau, phi0):
    import numpy as np
    return s_amp * np.exp(-1j*(2*np.pi*freqs*tau + phi0))

def fit_transmission_models_delay(f_tr, s_tr, deg=3, n_cycles=13, ridge=1e-3):
    """Delay-aware transmission modeling.

    1) Estimate (tau, phi0) from training split only
    2) Dephase training complex data
    3) Fit baseline poly(log f) and poly+UF to dephased complex amplitude
    Returns: (tau, phi0), (wr_b, wi_b), (wr_u, wi_u)
    """
    tau, phi0 = estimate_delay_params(f_tr, s_tr)
    s_tr_amp = remove_delay(f_tr, s_tr, tau, phi0)
    wr_b, wi_b, _ = fit_poly_complex_logf(f_tr, s_tr_amp, deg=deg, ridge=0.0, add_ufrf=False)
    wr_u, wi_u, _ = fit_poly_complex_logf(f_tr, s_tr_amp, deg=deg, ridge=ridge, add_ufrf=True, n_cycles=n_cycles, ridge_on_last2=True)
    return (tau, phi0), (wr_b, wi_b), (wr_u, wi_u)
