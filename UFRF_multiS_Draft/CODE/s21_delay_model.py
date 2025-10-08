
import numpy as np

def _unwrap_phase(ph):
    return np.unwrap(ph)

def _estimate_delay_phase(f, S, w_mag=True):
    ph = _unwrap_phase(np.angle(S))
    x = f.astype(float)
    X = np.column_stack([x, np.ones_like(x)])
    if w_mag:
        w = np.abs(S) + 1e-12
        W = np.diag(w / np.max(w))
        XtX = X.T @ W @ X
        Xty = X.T @ W @ ph
    else:
        XtX = X.T @ X
        Xty = X.T @ ph
    beta = np.linalg.solve(XtX, Xty)
    slope, phi0 = beta
    tau = -slope / (2*np.pi)
    return float(tau), float(phi0)

def _vandermonde_logf(logf, deg):
    cols = [np.ones_like(logf)]
    for d in range(1, deg+1):
        cols.append(logf**d)
    return np.column_stack(cols)

def _add_ripple_cols(X, logf, n_cycles=13):
    P = (logf.max()-logf.min())/max(1, n_cycles)
    theta = (logf - logf.min())/P * 2*np.pi
    return np.column_stack([X, np.sin(theta), np.cos(theta)])

def fit_delay_aware(f, S, deg=3, ridge=1e-3, n_cycles=13, gate=None):
    f = f.astype(float)
    logf = np.log(f)
    tau, phi0 = _estimate_delay_phase(f, S, w_mag=True)
    base_phase = -(2*np.pi*f)*tau + phi0
    phase = _unwrap_phase(np.angle(S))
    dphi = phase - base_phase
    A = np.abs(S)

    Xa = _vandermonde_logf(logf, deg)
    Xp = _vandermonde_logf(logf, deg)
    Xa_u = _add_ripple_cols(Xa, logf, n_cycles=n_cycles)
    Xp_u = _add_ripple_cols(Xp, logf, n_cycles=n_cycles)

    def _ridge_solve(X, y, ridge_mask_cols=None, lam=0.0):
        XtX = X.T @ X
        if lam>0 and ridge_mask_cols is not None:
            R = np.zeros_like(XtX)
            for i in ridge_mask_cols:
                R[i,i] = lam
            XtX = XtX + R
        return np.linalg.solve(XtX, X.T @ y)

    wa = _ridge_solve(Xa, A, None, 0.0)
    wp = _ridge_solve(Xp, dphi, None, 0.0)

    ridge_cols = [Xa_u.shape[1]-2, Xa_u.shape[1]-1]
    wa_u = _ridge_solve(Xa_u, A, ridge_cols, ridge)
    wp_u = _ridge_solve(Xp_u, dphi, ridge_cols, ridge)

    def mse(u,v): d=u-v; return float(np.mean(d*d))
    A_b = Xa @ wa; A_u = Xa_u @ wa_u
    dphi_b = Xp @ wp; dphi_u = Xp_u @ wp_u
    mse_b = mse(A, A_b) + mse(dphi, dphi_b)
    mse_u = mse(A, A_u) + mse(dphi, dphi_u)
    train_gain = 0.0 if mse_b==0 else (mse_b - mse_u)/abs(mse_b)

    use_uf = True
    if gate is not None and train_gain < gate:
        use_uf = False

    params = dict(tau=tau, phi0=phi0, deg=deg, ridge=ridge, n_cycles=n_cycles,
                  wa=wa.tolist(), wp=wp.tolist(),
                  wa_u=wa_u.tolist(), wp_u=wp_u.tolist(),
                  gate=gate, train_gain=float(train_gain), use_uf=use_uf)

    def predict(fq):
        lf = np.log(fq.astype(float))
        def vand(lf, deg):
            cols=[np.ones_like(lf)]
            for d in range(1,deg+1):
                cols.append(lf**d)
            return np.column_stack(cols)
        Xa_q = vand(lf, deg)
        Xp_q = vand(lf, deg)
        if use_uf:
            P = (lf.max()-lf.min())/max(1, n_cycles)
            th = (lf - lf.min())/P * 2*np.pi
            Xa_q = np.column_stack([Xa_q, np.sin(th), np.cos(th)])
            Xp_q = np.column_stack([Xp_q, np.sin(th), np.cos(th)])
            wa_q = np.array(wa_u); wp_q = np.array(wp_u)
        else:
            wa_q = np.array(wa);   wp_q = np.array(wp)
        Ahat = Xa_q @ wa_q
        dphihat = Xp_q @ wp_q
        phase_hat = -(2*np.pi*fq)*tau + phi0 + dphihat
        return Ahat * np.exp(-1j*phase_hat)

    return params, predict
