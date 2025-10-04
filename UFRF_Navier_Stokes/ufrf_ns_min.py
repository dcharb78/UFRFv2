
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
import argparse
import os
import json


# ===== Determinism =====
DEFAULT_SEED = 1717
rng = np.random.default_rng(DEFAULT_SEED)


# ===== Utilities =====
def fftfreq_2d(n):
    k = np.fft.fftfreq(n, d=1.0 / n)
    return np.meshgrid(k, k, indexing='ij')


def dealias_mask(n):
    # 2/3 rule
    kx, ky = fftfreq_2d(n)
    kmax = n / 2
    cutoff = (2.0 / 3.0) * kmax
    return (np.abs(kx) <= cutoff) & (np.abs(ky) <= cutoff)


def laplacian_hat(kx, ky):
    return -(2.0 * np.pi) ** 2 * (kx ** 2 + ky ** 2)


def energy_spectrum(u_hat, v_hat, kx, ky):
    # Compute isotropic 1D spectrum E(k)
    k_mag = np.sqrt(kx ** 2 + ky ** 2)
    k_bins = np.arange(0.5, np.max(k_mag) + 1.5, 1.0)
    ek = np.zeros_like(k_bins)
    vel_hat_energy = 0.5 * (np.abs(u_hat) ** 2 + np.abs(v_hat) ** 2)
    for i, kb in enumerate(k_bins):
        mask = (k_mag >= (kb - 0.5)) & (k_mag < (kb + 0.5))
        ek[i] = np.sum(vel_hat_energy[mask])
    return k_bins, ek


def compute_metrics(u, v, w):
    energy = 0.5 * np.mean(u ** 2 + v ** 2)
    enstrophy = 0.5 * np.mean(w ** 2)
    max_grad_w = np.max(np.abs(np.gradient(w)[0]))
    return {
        "energy": float(energy),
        "enstrophy": float(enstrophy),
        "max_grad_w": float(max_grad_w),
    }


def compute_divergence(u, v):
    du_dx = np.gradient(u, axis=0)
    dv_dy = np.gradient(v, axis=1)
    div = du_dx + dv_dy
    return float(np.sqrt(np.mean(div ** 2)))


def build_high_k_filter(kx, ky, dt, strength=0.0, order=8):
    if strength <= 0.0:
        return None
    k_mag = np.sqrt(kx ** 2 + ky ** 2)
    kmax = np.max(k_mag)
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(kmax > 0, k_mag / kmax, 0.0)
    filt = np.exp(-strength * (ratio ** order) * dt)
    return filt


def enstrophy_spectrum(w_hat, kx, ky):
    k_mag = np.sqrt(kx ** 2 + ky ** 2)
    k_bins = np.arange(0.5, np.max(k_mag) + 1.5, 1.0)
    zk = np.zeros_like(k_bins)
    w_energy = 0.5 * (np.abs(w_hat) ** 2)
    for i, kb in enumerate(k_bins):
        mask = (k_mag >= (kb - 0.5)) & (k_mag < (kb + 0.5))
        zk[i] = np.sum(w_energy[mask])
    return k_bins, zk


def compute_energy_flux_2d(u_hat, v_hat, kx, ky):
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    # Gradients in spectral
    ux_hat = ikx * u_hat
    uy_hat = iky * u_hat
    vx_hat = ikx * v_hat
    vy_hat = iky * v_hat
    # Back to physical
    u = np.fft.ifft2(u_hat).real
    v = np.fft.ifft2(v_hat).real
    ux = np.fft.ifft2(ux_hat).real
    uy = np.fft.ifft2(uy_hat).real
    vx = np.fft.ifft2(vx_hat).real
    vy = np.fft.ifft2(vy_hat).real
    # Advective terms
    advu = u * ux + v * uy
    advv = u * vx + v * vy
    advu_hat = np.fft.fft2(advu)
    advv_hat = np.fft.fft2(advv)
    # Transfer and flux
    transfer = np.real(np.conj(u_hat) * (-advu_hat) + np.conj(v_hat) * (-advv_hat))
    k_mag = np.sqrt(kx ** 2 + ky ** 2)
    k_bins = np.arange(0.5, np.max(k_mag) + 1.5, 1.0)
    Tk = np.zeros_like(k_bins)
    for i, kb in enumerate(k_bins):
        mask = (k_mag >= (kb - 0.5)) & (k_mag < (kb + 0.5))
        Tk[i] = np.sum(transfer[mask])
    # Cumulative flux from high to low k
    Pi = np.cumsum(Tk[::-1])[::-1]
    return k_bins, Pi


def compute_shell_transfer_2d(u_hat, v_hat, kx, ky):
    # Use transfer spectrum Tk as net transfer into shell
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    ux_hat = ikx * u_hat
    uy_hat = iky * u_hat
    vx_hat = ikx * v_hat
    vy_hat = iky * v_hat
    u = np.fft.ifft2(u_hat).real
    v = np.fft.ifft2(v_hat).real
    ux = np.fft.ifft2(ux_hat).real
    uy = np.fft.ifft2(uy_hat).real
    vx = np.fft.ifft2(vx_hat).real
    vy = np.fft.ifft2(vy_hat).real
    advu_hat = np.fft.fft2(u * ux + v * uy)
    advv_hat = np.fft.fft2(u * vx + v * vy)
    transfer = np.real(np.conj(u_hat) * (-advu_hat) + np.conj(v_hat) * (-advv_hat))
    k_mag = np.sqrt(kx ** 2 + ky ** 2)
    k_bins = np.arange(0.5, np.max(k_mag) + 1.5, 1.0)
    Tk = np.zeros_like(k_bins)
    for i, kb in enumerate(k_bins):
        mask = (k_mag >= (kb - 0.5)) & (k_mag < (kb + 0.5))
        Tk[i] = np.sum(transfer[mask])
    return k_bins, Tk


def fit_slope_loglog(k, Ek, kmin=2.0, kmax=None):
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


def build_ufrf_wedge_force_hat(kx, ky, cfg: 'UfrfWedgeConfig', kmin: float, kmax: float, amp: float, seed: int):
    # Build spectral vorticity forcing aligned with UFRF wedges within k band
    angle = np.degrees(np.arctan2(ky, kx)) % 360.0
    centers = [(360.0 / 13.0) * i for i in range(13)]
    if cfg.include_half:
        offset = (360.0 / 13.0) / 2.0
        centers += [((360.0 / 13.0) * i + offset) % 360.0 for i in range(13)]
    mask_ang = np.zeros_like(angle, dtype=bool)
    for c in centers:
        d = np.minimum(np.abs(angle - c), 360.0 - np.abs(angle - c))
        mask_ang |= (d <= cfg.halfwidth_deg)
    kmag = np.sqrt(kx ** 2 + ky ** 2)
    mask_mag = (kmag >= kmin) & (kmag <= kmax)
    mask = mask_ang & mask_mag
    # Deterministic complex field with random phases
    local_rng = np.random.default_rng(seed)
    phase = local_rng.uniform(0.0, 2.0 * np.pi, size=kx.shape)
    force_hat = amp * (np.cos(phase) + 1j * np.sin(phase))
    force_hat *= mask
    # Enforce Hermitian symmetry for real spatial field
    n = kx.shape[0]
    for i in range(n):
        for j in range(n):
            ii = (-i) % n
            jj = (-j) % n
            force_hat[ii, jj] = np.conj(force_hat[i, j])
    return force_hat


# ===== UFRF Wedge Filter =====
@dataclass
class UfrfWedgeConfig:
    halfwidth_deg: float = 6.0
    include_half: bool = False


def build_angular_wedge_mask(kx, ky, cfg: UfrfWedgeConfig):
    # Angles in degrees, with centers at 360/13 spacing
    angle = np.degrees(np.arctan2(ky, kx)) % 360.0
    centers = [(360.0 / 13.0) * i for i in range(13)]
    if cfg.include_half:
        offset = (360.0 / 13.0) / 2.0
        centers += [((360.0 / 13.0) * i + offset) % 360.0 for i in range(13)]
    mask = np.zeros_like(angle, dtype=bool)
    for c in centers:
        # angular distance on circle
        d = np.minimum(np.abs(angle - c), 360.0 - np.abs(angle - c))
        mask |= (d <= cfg.halfwidth_deg)
    # Always keep k=0 (avoid zeroing mean pressure mode handling)
    mask[(kx == 0) & (ky == 0)] = True
    return mask


# ===== Navier–Stokes (vorticity-streamfunction) =====
def rhs_vorticity(omega, nu, n, kx, ky, dealias, ufrf_mask=None, forcing=None, friction_gamma=0.0):
    # Streamfunction: \nabla^2 psi = -omega
    lap_hat = laplacian_hat(kx, ky)
    omega_hat = np.fft.fft2(omega)
    # Solve in Fourier space, handle k=0
    with np.errstate(divide='ignore', invalid='ignore'):
        psi_hat = -omega_hat / lap_hat
    psi_hat[0, 0] = 0.0

    # Velocity from streamfunction: u = d psi/dy, v = -d psi/dx
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    u_hat = iky * psi_hat
    v_hat = -ikx * psi_hat

    u = np.fft.ifft2(u_hat).real
    v = np.fft.ifft2(v_hat).real

    # Nonlinear term: J(psi, omega) = d psi/dx d omega/dy - d psi/dy d omega/dx
    dpsidx = np.fft.ifft2(ikx * psi_hat).real
    dpsidy = np.fft.ifft2(iky * psi_hat).real
    domegadx = np.fft.ifft2(ikx * omega_hat).real
    domegady = np.fft.ifft2(iky * omega_hat).real
    adv = dpsidx * domegady - dpsidy * domegadx

    # FFT of advective term and optional UFRF masking
    adv_hat = np.fft.fft2(adv)
    if ufrf_mask is not None:
        adv_hat = adv_hat * ufrf_mask

    # Dealiasing
    adv_hat = adv_hat * dealias

    # Diffusion term in Fourier
    rhs_hat = -adv_hat + nu * lap_hat * omega_hat

    # Optional forcing
    if forcing is not None:
        ftype = forcing.get("type")
        if ftype == "kolmogorov":
            F0 = forcing.get("amp", 0.0)
            kf = forcing.get("kf", 1)
            y = np.linspace(0.0, 1.0, n, endpoint=False)
            cosy = np.cos(2.0 * np.pi * kf * y)
            curl_f = (-F0 * 2.0 * np.pi * kf) * np.tile(cosy, (n, 1))
            rhs_hat += np.fft.fft2(curl_f)
        elif ftype == "ufrf_wedge":
            force_hat = forcing.get("hat")
            if force_hat is not None:
                rhs_hat += force_hat

    # Linear friction (REST projection damping)
    if friction_gamma and friction_gamma > 0.0:
        rhs_hat += -friction_gamma * omega_hat
    rhs = np.fft.ifft2(rhs_hat).real
    return rhs


def rk4_step(omega, dt, rhs_fn):
    k1 = rhs_fn(omega)
    k2 = rhs_fn(omega + 0.5 * dt * k1)
    k3 = rhs_fn(omega + 0.5 * dt * k2)
    k4 = rhs_fn(omega + dt * k3)
    return omega + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def init_vorticity(n, seed=DEFAULT_SEED):
    local_rng = np.random.default_rng(seed)
    # Smooth random field via spectral shaping
    kx, ky = fftfreq_2d(n)
    kmag = np.sqrt(kx ** 2 + ky ** 2)
    spec = local_rng.standard_normal((n, n)) + 1j * local_rng.standard_normal((n, n))
    spec *= np.exp(-(kmag / (n / 16.0)) ** 2)
    spec[0, 0] = 0.0
    w = np.fft.ifft2(spec).real
    w -= w.mean()
    return w


def init_vorticity_shear(n, delta=0.05, u0=1.0, noise_eps=1e-3, seed=DEFAULT_SEED):
    # Double shear layer in y with small x-perturbation
    local_rng = np.random.default_rng(seed)
    x = np.linspace(0.0, 1.0, n, endpoint=False)
    y = np.linspace(0.0, 1.0, n, endpoint=False)
    X, Y = np.meshgrid(x, y, indexing='ij')

    def tanh_layer(y, y0):
        return np.tanh((y - y0) / delta)

    U = u0 * (tanh_layer(Y, 0.25) - tanh_layer(Y, 0.75))
    V = noise_eps * (np.sin(2.0 * np.pi * X) + 0.1 * local_rng.standard_normal((n, n)))

    # Spectral curl w = dv/dx - du/dy
    kx, ky = fftfreq_2d(n)
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    Uh = np.fft.fft2(U)
    Vh = np.fft.fft2(V)
    dVdx = np.fft.ifft2(ikx * Vh).real
    dUdy = np.fft.ifft2(iky * Uh).real
    w = dVdx - dUdy
    w -= w.mean()
    return w


def init_vorticity_taylor_green(n):
    # Domain [0,1)^2; u = sin(2πx) cos(2πy), v = -cos(2πx) sin(2πy)
    x = np.linspace(0.0, 1.0, n, endpoint=False)
    y = np.linspace(0.0, 1.0, n, endpoint=False)
    X, Y = np.meshgrid(x, y, indexing='ij')
    U = np.sin(2.0 * np.pi * X) * np.cos(2.0 * np.pi * Y)
    V = -np.cos(2.0 * np.pi * X) * np.sin(2.0 * np.pi * Y)
    # Spectral curl
    kx, ky = fftfreq_2d(n)
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    Uh = np.fft.fft2(U)
    Vh = np.fft.fft2(V)
    dVdx = np.fft.ifft2(ikx * Vh).real
    dUdy = np.fft.ifft2(iky * Uh).real
    w = dVdx - dUdy
    w -= w.mean()
    return w


def run_sim(n=128, steps=800, dt=5e-3, nu=1e-3, seed=DEFAULT_SEED, halfwidth_deg=6.0, include_half=False, out_prefix="standard", outdir=".", init_type="random", delta=0.05, u0=1.0, noise_eps=1e-3, omega0=None, filter_strength=0.0, filter_order=8, log_interval=0, csv_base=None, cfl=0.0, forcing_type="none", force_amp=0.0, force_kf=1, friction_gamma=0.0, force_kmin=1.0, force_kmax=4.0):
    kx, ky = fftfreq_2d(n)
    dmask = dealias_mask(n)
    if omega0 is not None:
        w = omega0.copy()
    else:
        if init_type == "shear":
            w = init_vorticity_shear(n, delta=delta, u0=u0, noise_eps=noise_eps, seed=seed)
        elif init_type == "taylor_green":
            w = init_vorticity_taylor_green(n)
        else:
            w = init_vorticity(n, seed)

    # Build optional UFRF mask in Fourier space for advective term
    ufrf_mask = None
    if out_prefix != "standard":
        cfg = UfrfWedgeConfig(halfwidth_deg=halfwidth_deg, include_half=include_half)
        ufrf_mask = build_angular_wedge_mask(kx, ky, cfg)

    forcing = None
    if forcing_type == "kolmogorov" and force_amp != 0.0:
        forcing = {"type": "kolmogorov", "amp": force_amp, "kf": int(force_kf)}
    elif forcing_type == "ufrf_wedge" and force_amp != 0.0:
        cfg = UfrfWedgeConfig(halfwidth_deg=halfwidth_deg, include_half=include_half)
        force_hat = build_ufrf_wedge_force_hat(kx, ky, cfg, force_kmin, force_kmax, force_amp, seed)
        # Respect dealiasing
        force_hat = force_hat * dmask
        forcing = {"type": "ufrf_wedge", "hat": force_hat}

    def rhs_fn(omega):
        return rhs_vorticity(omega, nu, n, kx, ky, dmask, ufrf_mask, forcing, friction_gamma)

    hi_k_filter = build_high_k_filter(kx, ky, dt, strength=filter_strength, order=filter_order)

    # Initial u, v and metrics
    w_hat0 = np.fft.fft2(w)
    lap_hat = laplacian_hat(kx, ky)
    with np.errstate(divide='ignore', invalid='ignore'):
        psi_hat0 = -w_hat0 / lap_hat
    psi_hat0[0, 0] = 0.0
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    u_hat0 = iky * psi_hat0
    v_hat0 = -ikx * psi_hat0
    u0_r = np.fft.ifft2(u_hat0).real
    v0_r = np.fft.ifft2(v_hat0).real
    metrics_initial = compute_metrics(u0_r, v0_r, w)

    os.makedirs(outdir, exist_ok=True)
    csv_path = None
    if csv_base:
        csv_path = os.path.join(outdir, f"{csv_base}_{out_prefix}_{init_type}.csv")
        with open(csv_path, 'w') as f:
            f.write("step,time,energy,enstrophy,div_rms,epsilon,dE_dt,P_in,residual\n")

    # Initialize for CFL control
    u_cfl = u0_r
    v_cfl = v0_r
    dx = 1.0 / n

    prev_energy = metrics_initial["energy"]
    prev_time = 0.0
    for step in range(1, steps + 1):
        dt_eff = dt
        if cfl and cfl > 0.0:
            umax = max(np.max(np.abs(u_cfl)), np.max(np.abs(v_cfl))) + 1e-8
            dt_eff = min(dt, cfl * dx / umax)
        w = rk4_step(w, dt_eff, rhs_fn)
        if hi_k_filter is not None:
            w_hat_step = np.fft.fft2(w)
            w_hat_step *= hi_k_filter
            w = np.fft.ifft2(w_hat_step).real
        if log_interval and (step % log_interval == 0 or step == steps):
            w_hat_tmp = np.fft.fft2(w)
            with np.errstate(divide='ignore', invalid='ignore'):
                psi_hat_tmp = -w_hat_tmp / lap_hat
            psi_hat_tmp[0, 0] = 0.0
            u_hat_tmp = iky * psi_hat_tmp
            v_hat_tmp = -ikx * psi_hat_tmp
            u_tmp = np.fft.ifft2(u_hat_tmp).real
            v_tmp = np.fft.ifft2(v_hat_tmp).real
            u_cfl, v_cfl = u_tmp, v_tmp
            m = compute_metrics(u_tmp, v_tmp, w)
            div_rms = compute_divergence(u_tmp, v_tmp)
            # Momentum and circulation density
            mean_ux = float(np.mean(u_tmp))
            mean_vy = float(np.mean(v_tmp))
            circ_density = float(np.mean(w))
            # Dissipation epsilon = 2 * nu * <|∇u|^2>
            du_dx = np.gradient(u_tmp, axis=0)
            du_dy = np.gradient(u_tmp, axis=1)
            dv_dx = np.gradient(v_tmp, axis=0)
            dv_dy = np.gradient(v_tmp, axis=1)
            eps = 2.0 * nu * float(np.mean(du_dx**2 + du_dy**2 + dv_dx**2 + dv_dy**2))
            # dE/dt finite difference
            current_time = prev_time + dt_eff
            dE_dt = (m['energy'] - prev_energy) / (dt_eff if dt_eff > 0 else dt)
            # Forcing power input P_in
            Pin = 0.0
            if forcing is not None and forcing.get('type') == 'kolmogorov':
                F0 = forcing.get('amp', 0.0)
                kf = forcing.get('kf', 1)
                y = np.linspace(0.0, 1.0, n, endpoint=False)
                Fx = F0 * np.sin(2.0 * np.pi * kf * y)
                Fx_field = np.tile(Fx, (n, 1))
                Pin = float(np.mean(Fx_field * u_tmp))
            elif forcing is not None and forcing.get('type') == 'ufrf_wedge':
                # Report inferred input from budget
                Pin = float(dE_dt + eps)
            residual = float(dE_dt - (Pin - eps))
            prev_energy = m['energy']
            prev_time = current_time
            if csv_path:
                with open(csv_path, 'a') as f:
                    f.write(f"{step},{step*dt_eff},{m['energy']},{m['enstrophy']},{div_rms},{eps},{dE_dt},{Pin},{residual}\n")
            # Save energy flux at final step
            if step == steps:
                k_bins_flux, Pi = compute_energy_flux_2d(u_hat_tmp, v_hat_tmp, kx, ky)
                flux_path = os.path.join(outdir, f"flux_{out_prefix}_{init_type}.csv")
                with open(flux_path, 'w') as f:
                    f.write("k,Pi\n")
                    for kb, p in zip(k_bins_flux, Pi):
                        f.write(f"{kb},{p}\n")

    # Final velocity and energy spectrum
    w_hat = np.fft.fft2(w)
    lap_hat = laplacian_hat(kx, ky)
    with np.errstate(divide='ignore', invalid='ignore'):
        psi_hat = -w_hat / lap_hat
    psi_hat[0, 0] = 0.0
    ikx = 1j * (2.0 * np.pi) * kx
    iky = 1j * (2.0 * np.pi) * ky
    u_hat = iky * psi_hat
    v_hat = -ikx * psi_hat
    u = np.fft.ifft2(u_hat).real
    v = np.fft.ifft2(v_hat).real

    k_bins, ek = energy_spectrum(u_hat, v_hat, kx, ky)
    kz_bins, zk = enstrophy_spectrum(w_hat, kx, ky)
    slope_energy = fit_slope_loglog(k_bins, ek, kmin=2.0)

    # Final metrics
    metrics_final = compute_metrics(u, v, w)
    decay = 0.0
    if metrics_initial["energy"] > 0:
        decay = (metrics_initial["energy"] - metrics_final["energy"]) / metrics_initial["energy"]
    metrics = {
        "init_type": init_type,
        "out_prefix": out_prefix,
        "energy_initial": metrics_initial["energy"],
        "energy_final": metrics_final["energy"],
        "energy_decay_fraction": float(decay),
        "enstrophy_initial": metrics_initial["enstrophy"],
        "enstrophy_final": metrics_final["enstrophy"],
        "max_grad_w_final": metrics_final["max_grad_w"],
    }

    # Plot vorticity snapshot
    os.makedirs(outdir, exist_ok=True)
    plt.figure(figsize=(6, 5))
    plt.imshow(w, origin='lower', cmap='RdBu_r')
    plt.colorbar(label='vorticity')
    if out_prefix == 'standard':
        plt.title(f'Vorticity (Standard, {init_type})')
        plt.savefig(os.path.join(outdir, f'snapshot_vorticity_standard_{init_type}.png'), dpi=150, bbox_inches='tight')
    else:
        plt.title(f'Vorticity (UFRF 13-wedge, {init_type})')
        plt.savefig(os.path.join(outdir, f'snapshot_vorticity_ufrf13_{init_type}.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Plot enstrophy spectrum
    plt.figure(figsize=(6, 4))
    plt.loglog(kz_bins, zk + 1e-20)
    plt.xlabel('k')
    plt.ylabel('Z(k)')
    plt.title(f'Enstrophy Spectrum ({init_type}, {out_prefix})')
    plt.savefig(os.path.join(outdir, f'enstrophy_spectrum_{out_prefix}_{init_type}.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Dump shell transfer and slope
    k_shell, Tk_shell = compute_shell_transfer_2d(u_hat, v_hat, kx, ky)
    with open(os.path.join(outdir, f'shell_transfer_{out_prefix}_{init_type}.csv'), 'w') as f:
        f.write('k,Tk\n')
        for kb, tk in zip(k_shell, Tk_shell):
            f.write(f'{kb},{tk}\n')
    with open(os.path.join(outdir, f'slopes_{out_prefix}_{init_type}.json'), 'w') as f:
        json.dump({"energy_slope": slope_energy}, f)

    return k_bins, ek, metrics


def main():
    parser = argparse.ArgumentParser(description='UFRF vs Standard 2D Navier–Stokes')
    parser.add_argument('--n', type=int, default=128)
    parser.add_argument('--grid', type=int, help='Alias for --n')
    parser.add_argument('--steps', type=int, default=800)
    parser.add_argument('--dt', type=float, default=5e-3)
    parser.add_argument('--nu', type=float, default=1e-3)
    parser.add_argument('--eta_over_s_proj', type=float, help='Alias mapping to nu for projection-based viscosity')
    parser.add_argument('--seed', type=int, default=DEFAULT_SEED)
    parser.add_argument('--halfwidth-deg', type=float, default=6.0)
    parser.add_argument('--wedge-halfwidth', type=float, help='Alias for --halfwidth-deg')
    parser.add_argument('--include-half', action='store_true')
    parser.add_argument('--wedge-half', action='store_true', help='Alias for --include-half')
    parser.add_argument('--init', type=str, default='random', choices=['random', 'shear', 'taylor_green'])
    parser.add_argument('--delta', type=float, default=0.05)
    parser.add_argument('--u0', type=float, default=1.0)
    parser.add_argument('--noise-eps', type=float, default=1e-3)
    parser.add_argument('--outdir', type=str, default='.')
    parser.add_argument('--filter-strength', type=float, default=0.0)
    parser.add_argument('--filter-order', type=int, default=8)
    parser.add_argument('--log-interval', type=int, default=0)
    parser.add_argument('--csv-base', type=str, default=None)
    parser.add_argument('--cfl', type=float, default=0.0)
    parser.add_argument('--forcing', type=str, default='none', choices=['none', 'kolmogorov', 'ufrf_wedge'])
    parser.add_argument('--force-amp', type=float, default=0.0)
    parser.add_argument('--force-kf', type=int, default=1)
    parser.add_argument('--friction-gamma', type=float, default=0.0)
    parser.add_argument('--force-kmin', type=float, default=1.0)
    parser.add_argument('--force-kmax', type=float, default=4.0)
    args = parser.parse_args()
    # Aliases
    if args.grid is not None:
        args.n = args.grid
    if args.eta_over_s_proj is not None:
        args.nu = args.eta_over_s_proj
    if args.wedge_halfwidth is not None:
        args.halfwidth_deg = args.wedge_halfwidth
    if args.wedge_half:
        args.include_half = True

    # Standard run
    k_std, e_std, m_std = run_sim(n=args.n, steps=args.steps, dt=args.dt, nu=args.nu, seed=args.seed, out_prefix="standard", outdir=args.outdir, init_type=args.init, delta=args.delta, u0=args.u0, noise_eps=args.noise_eps, filter_strength=args.filter_strength, filter_order=args.filter_order, log_interval=args.log_interval, csv_base=args.csv_base, cfl=args.cfl, forcing_type=args.forcing, force_amp=args.force_amp, force_kf=args.force_kf)
    # UFRF run
    k_ufrf, e_ufrf, m_ufrf = run_sim(n=args.n, steps=args.steps, dt=args.dt, nu=args.nu, seed=args.seed, halfwidth_deg=args.halfwidth_deg, include_half=args.include_half, out_prefix="ufrf", outdir=args.outdir, init_type=args.init, delta=args.delta, u0=args.u0, noise_eps=args.noise_eps, filter_strength=args.filter_strength, filter_order=args.filter_order, log_interval=args.log_interval, csv_base=args.csv_base, cfl=args.cfl, forcing_type=args.forcing, force_amp=args.force_amp, force_kf=args.force_kf)

    # Spectrum overlay
    plt.figure(figsize=(6, 4))
    plt.loglog(k_std, e_std + 1e-16, label='Standard')
    plt.loglog(k_ufrf, e_ufrf + 1e-16, label='UFRF 13-wedge')
    plt.xlabel('k')
    plt.ylabel('E(k)')
    plt.legend()
    plt.title(f'Kinetic Energy Spectrum ({args.init})')
    os.makedirs(args.outdir, exist_ok=True)
    plt.savefig(os.path.join(args.outdir, f'spectrum_compare_{args.init}.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Print metrics summary (stdout) as JSON
    print(json.dumps({"standard": m_std, "ufrf": m_ufrf}))


if __name__ == '__main__':
    main()
