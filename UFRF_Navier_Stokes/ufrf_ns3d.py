import numpy as np
import argparse
import os
import json
import matplotlib.pyplot as plt


def fftfreq_3d(n):
    k = np.fft.fftfreq(n, d=1.0 / n)
    return np.meshgrid(k, k, k, indexing='ij')


def dealias_mask_3d(n):
    kx, ky, kz = fftfreq_3d(n)
    kmax = n / 2
    cutoff = (2.0 / 3.0) * kmax
    return (np.abs(kx) <= cutoff) & (np.abs(ky) <= cutoff) & (np.abs(kz) <= cutoff)


def project_incompressible(u_hat, kx, ky, kz):
    # Helmholtz projection: u_hat <- (I - kk^T/k^2) u_hat
    k2 = kx**2 + ky**2 + kz**2
    with np.errstate(divide='ignore', invalid='ignore'):
        kdotu = kx * u_hat[0] + ky * u_hat[1] + kz * u_hat[2]
        for i, ki in enumerate([kx, ky, kz]):
            u_hat[i] = u_hat[i] - np.where(k2 != 0, (ki * kdotu) / k2, 0.0)
    return u_hat


def energy_spectrum_3d(u_hat, kx, ky, kz):
    k_mag = np.sqrt(kx**2 + ky**2 + kz**2)
    k_bins = np.arange(0.5, np.max(k_mag) + 1.5, 1.0)
    ek = np.zeros_like(k_bins)
    e_density = 0.5 * (np.abs(u_hat[0])**2 + np.abs(u_hat[1])**2 + np.abs(u_hat[2])**2)
    for i, kb in enumerate(k_bins):
        mask = (k_mag >= (kb - 0.5)) & (k_mag < (kb + 0.5))
        ek[i] = np.sum(e_density[mask])
    return k_bins, ek


def init_taylor_green(n):
    # Domain [0, 2π)^3
    x = np.linspace(0.0, 2.0*np.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing='ij')
    u = np.sin(X) * np.cos(Y) * np.cos(Z)
    v = -np.cos(X) * np.sin(Y) * np.cos(Z)
    w = np.zeros_like(u)
    return u, v, w


def rhs(u, v, w, nu, kx, ky, kz, dmask, forcing=None, friction_gamma=0.0):
    # Compute nonlinear term in physical space
    # Gradients in spectral space
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    ikz = 1j * (2.0 * np.pi) * kz

    u_hat = np.fft.fftn(u), np.fft.fftn(v), np.fft.fftn(w)
    u_hat = list(u_hat)
    u_hat = project_incompressible(u_hat, kx, ky, kz)
    for i in range(3):
        u_hat[i] *= dmask

    ux = np.fft.ifftn(ikx * u_hat[0]).real
    uy = np.fft.ifftn(iky * u_hat[0]).real
    uz = np.fft.ifftn(ikz * u_hat[0]).real
    vx = np.fft.ifftn(ikx * u_hat[1]).real
    vy = np.fft.ifftn(iky * u_hat[1]).real
    vz = np.fft.ifftn(ikz * u_hat[1]).real
    wx = np.fft.ifftn(ikx * u_hat[2]).real
    wy = np.fft.ifftn(iky * u_hat[2]).real
    wz = np.fft.ifftn(ikz * u_hat[2]).real

    adv_u = u * ux + v * uy + w * uz
    adv_v = u * vx + v * vy + w * vz
    adv_w = u * wx + v * wy + w * wz

    adv_u_hat = np.fft.fftn(adv_u) * dmask
    adv_v_hat = np.fft.fftn(adv_v) * dmask
    adv_w_hat = np.fft.fftn(adv_w) * dmask

    k2 = (2.0 * np.pi)**2 * (kx**2 + ky**2 + kz**2)
    rhs_u_hat = -adv_u_hat - nu * k2 * u_hat[0]
    rhs_v_hat = -adv_v_hat - nu * k2 * u_hat[1]
    rhs_w_hat = -adv_w_hat - nu * k2 * u_hat[2]

    # Forcing in spectral space
    if forcing is not None:
        ftype = forcing.get('type')
        if ftype == 'kolmogorov3d':
            F0 = forcing.get('amp', 0.0)
            kf = forcing.get('kf', 1)
            # Fx = F0 * sin(2π kf y), constant across x,z
            n = u.shape[0]
            y = np.linspace(0.0, 1.0, n, endpoint=False)
            Fx = F0 * np.sin(2.0 * np.pi * kf * y)
            Fx_field = np.tile(Fx, (n, 1))
            Fx_field = np.tile(Fx_field[:, None, :], (1, n, 1))
            rhs_u_hat += np.fft.fftn(Fx_field) * dmask
        elif ftype == 'ufrf_shell':
            hat = forcing.get('hat')
            if hat is not None:
                # Apply identical isotropic forcing to u-component
                rhs_u_hat += hat * dmask

    # Linear friction (REST projection analogue)
    if friction_gamma and friction_gamma > 0.0:
        rhs_u_hat += -friction_gamma * u_hat[0]
        rhs_v_hat += -friction_gamma * u_hat[1]
        rhs_w_hat += -friction_gamma * u_hat[2]

    # Project to incompressible
    rhs_hat = [rhs_u_hat, rhs_v_hat, rhs_w_hat]
    rhs_hat = project_incompressible(rhs_hat, kx, ky, kz)

    return np.fft.ifftn(rhs_hat[0]).real, np.fft.ifftn(rhs_hat[1]).real, np.fft.ifftn(rhs_hat[2]).real


def rk4(u, v, w, dt, rhs_fn):
    k1 = rhs_fn(u, v, w)
    k2 = rhs_fn(u + 0.5*dt*k1[0], v + 0.5*dt*k1[1], w + 0.5*dt*k1[2])
    k3 = rhs_fn(u + 0.5*dt*k2[0], v + 0.5*dt*k2[1], w + 0.5*dt*k2[2])
    k4 = rhs_fn(u + dt*k3[0], v + dt*k3[1], w + dt*k3[2])
    u_new = u + (dt/6.0)*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0])
    v_new = v + (dt/6.0)*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1])
    w_new = w + (dt/6.0)*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2])
    return u_new, v_new, w_new


def compute_energy(u, v, w):
    return 0.5 * float(np.mean(u*u + v*v + w*w))


def compute_dissipation(u, v, w, nu):
    ux = np.gradient(u, axis=0)
    uy = np.gradient(u, axis=1)
    uz = np.gradient(u, axis=2)
    vx = np.gradient(v, axis=0)
    vy = np.gradient(v, axis=1)
    vz = np.gradient(v, axis=2)
    wx = np.gradient(w, axis=0)
    wy = np.gradient(w, axis=1)
    wz = np.gradient(w, axis=2)
    # 2ν <|∇u|^2>
    grad2 = ux*ux + uy*uy + uz*uz + vx*vx + vy*vy + vz*vz + wx*wx + wy*wy + wz*wz
    return 2.0 * nu * float(np.mean(grad2))


def build_ufrf_shell_force_hat(kx, ky, kz, kmin, kmax, amp, seed):
    kmag = np.sqrt(kx**2 + ky**2 + kz**2)
    mask = (kmag >= kmin) & (kmag <= kmax)
    rng = np.random.default_rng(seed)
    phase = rng.uniform(0.0, 2.0*np.pi, size=kx.shape)
    hat = amp * (np.cos(phase) + 1j*np.sin(phase)) * mask
    # Hermitian symmetry for real field
    n = kx.shape[0]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                ii = (-i) % n
                jj = (-j) % n
                kk = (-k) % n
                hat[ii, jj, kk] = np.conj(hat[i, j, k])
    return hat


def run_tg(n=64, steps=400, dt=1e-3, nu=1e-3, seed=1717, outdir="results3d", forcing_type='none', force_amp=0.0, force_kf=1, friction_gamma=0.0, force_kmin=1.0, force_kmax=2.0):
    os.makedirs(outdir, exist_ok=True)
    kx, ky, kz = fftfreq_3d(n)
    dmask = dealias_mask_3d(n)

    u, v, w = init_taylor_green(n)
    E0 = compute_energy(u, v, w)

    forcing = None
    if forcing_type == 'kolmogorov3d' and force_amp != 0.0:
        forcing = {'type': 'kolmogorov3d', 'amp': force_amp, 'kf': int(force_kf)}
    elif forcing_type == 'ufrf_shell' and force_amp != 0.0:
        hat = build_ufrf_shell_force_hat(kx, ky, kz, force_kmin, force_kmax, force_amp, seed)
        forcing = {'type': 'ufrf_shell', 'hat': hat}

    def rhs_fn(u_, v_, w_):
        return rhs(u_, v_, w_, nu, kx, ky, kz, dmask, forcing=forcing, friction_gamma=friction_gamma)

    csv_path = os.path.join(outdir, "tg_timeseries.csv")
    with open(csv_path, 'w') as f:
        f.write("step,time,E,epsilon,dE_dt,P_in,residual\n")

    prev_E = E0
    t = 0.0
    for step in range(1, steps+1):
        u, v, w = rk4(u, v, w, dt, rhs_fn)
        if step % 20 == 0 or step == steps:
            E = compute_energy(u, v, w)
            eps = compute_dissipation(u, v, w, nu)
            dE_dt = (E - prev_E) / dt
            # Power input estimate
            Pin = 0.0
            if forcing is not None and forcing.get('type') == 'kolmogorov3d':
                F0 = forcing.get('amp', 0.0)
                kf = forcing.get('kf', 1)
                y = np.linspace(0.0, 1.0, n, endpoint=False)
                Fx = F0 * np.sin(2.0 * np.pi * kf * y)
                Fx_field = np.tile(Fx, (n, 1))
                Fx_field = np.tile(Fx_field[:, None, :], (1, n, 1))
                Pin = float(np.mean(Fx_field * u))
            elif forcing is not None and forcing.get('type') == 'ufrf_shell':
                Pin = dE_dt + eps
            residual = dE_dt - (Pin - eps)
            with open(csv_path, 'a') as f:
                f.write(f"{step},{t+dt},{E},{eps},{dE_dt},{Pin},{residual}\n")
            prev_E = E
        t += dt

    u_hat = np.fft.fftn(u), np.fft.fftn(v), np.fft.fftn(w)
    u_hat = list(u_hat)
    k_bins, ek = energy_spectrum_3d(u_hat, kx, ky, kz)

    plt.figure(figsize=(6,4))
    plt.loglog(k_bins, ek + 1e-20)
    plt.xlabel('k')
    plt.ylabel('E(k)')
    plt.title('3D TG Energy Spectrum')
    plt.savefig(os.path.join(outdir, 'tg_spectrum.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Slope fit on spectrum (log-log)
    def fit_slope(k, Ek, kmin=2.0, kmax=None):
        x = np.array(k)
        y = np.array(Ek) + 1e-30
        if kmax is None:
            kmax = np.max(x)
        mask = (x >= kmin) & (x <= kmax) & (y > 0)
        if np.sum(mask) < 3:
            return None
        X = np.log(x[mask])
        Y = np.log(y[mask])
        A = np.vstack([X, np.ones_like(X)]).T
        slope, intercept = np.linalg.lstsq(A, Y, rcond=None)[0]
        return float(slope)

    slope_energy = fit_slope(k_bins, ek, kmin=2.0)

    with open(os.path.join(outdir, 'tg_summary.json'), 'w') as f:
        json.dump({"E0": E0, "E_final": E, "epsilon_final": eps, "slope_energy": slope_energy}, f, indent=2)

    return {"E0": E0, "E_final": E, "epsilon_final": eps}


def main():
    parser = argparse.ArgumentParser(description='3D Taylor–Green decay (pseudo-spectral)')
    parser.add_argument('--n', type=int, default=64)
    parser.add_argument('--steps', type=int, default=400)
    parser.add_argument('--dt', type=float, default=1e-3)
    parser.add_argument('--nu', type=float, default=1e-3)
    parser.add_argument('--outdir', type=str, default='results3d')
    parser.add_argument('--force-amp', type=float, default=0.0)
    parser.add_argument('--force-kf', type=int, default=1)
    parser.add_argument('--force-kmin', type=float, default=1.0)
    parser.add_argument('--force-kmax', type=float, default=2.0)
    parser.add_argument('--friction-gamma', type=float, default=0.0)
    parser.add_argument('--forcing-type', type=str, default='none', choices=['none', 'kolmogorov3d', 'ufrf_shell'])
    args = parser.parse_args()
    forcing = getattr(args, 'forcing_type', 'none')
    summary = run_tg(n=args.n, steps=args.steps, dt=args.dt, nu=args.nu, outdir=args.outdir, forcing_type=forcing, force_amp=args.force_amp, force_kf=args.force_kf, friction_gamma=args.friction_gamma, force_kmin=args.force_kmin, force_kmax=args.force_kmax)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()


