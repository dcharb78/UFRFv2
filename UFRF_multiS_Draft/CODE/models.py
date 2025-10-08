
import numpy as np
def rlc_series_gamma(f, R, L, C, Z0):
    w = 2*np.pi*f
    Z = R + 1j*w*L + 1/(1j*w*C)
    return (Z - Z0)/(Z + Z0)

def rlc_series_gamma_ufrf(f, R, L, C, Z0, a, phi, n_cycles=13):
    w = 2*np.pi*f
    Z = R + 1j*w*L + 1/(1j*w*C)
    X = Z.imag
    logf = np.log(f); P = (logf.max()-logf.min())/max(1,n_cycles)
    phase = (logf - logf.min())/P * 2*np.pi + phi
    mod = 1.0 + a*np.sin(phase)
    X_mod = np.sign(X) * (np.abs(X) * mod)
    Zm = Z.real + 1j*X_mod
    return (Zm - Z0)/(Zm + Z0)

def _vandermonde_logf(logf, deg):
    cols = [np.ones_like(logf)]
    for d in range(1, deg+1):
        cols.append(logf**d)
    return np.column_stack(cols)

def _add_ufrf_cols(X, logf, n_cycles=13):
    P = (logf.max()-logf.min())/max(1,n_cycles)
    theta = (logf - logf.min())/P * 2*np.pi
    return np.column_stack([X, np.sin(theta), np.cos(theta)])

def fit_poly_complex_logf(f, y, deg=3, ridge=0.0, add_ufrf=False, n_cycles=13, ridge_on_last2=True):
    logf = np.log(f)
    X = _vandermonde_logf(logf, deg)
    if add_ufrf:
        X = _add_ufrf_cols(X, logf, n_cycles=n_cycles)
    def solve(X, t):
        XtX = X.T @ X
        if ridge>0:
            R = np.zeros_like(XtX)
            if ridge_on_last2 and add_ufrf:
                for i in range(X.shape[1]-2, X.shape[1]):
                    R[i,i] = ridge
            else:
                R += ridge*np.eye(X.shape[1])
            XtX = XtX + R
        return np.linalg.solve(XtX, X.T @ t)
    wr = solve(X, y.real)
    wi = solve(X, y.imag)
    return wr, wi, X

def predict_poly_complex_logf(f, wr, wi, deg=3, add_ufrf=False, n_cycles=13):
    logf = np.log(f)
    X = _vandermonde_logf(logf, deg)
    if add_ufrf:
        X = _add_ufrf_cols(X, logf, n_cycles=n_cycles)
    yr = X @ wr; yi = X @ wi
    return yr + 1j*yi
