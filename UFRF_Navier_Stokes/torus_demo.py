import numpy as np
from scipy.fft import fftn, ifftn
import json


def run_torus_demo(n_points=32, steps=200, dt=0.01):
    phi = (1 + np.sqrt(5)) / 2
    sqrt_phi = np.sqrt(phi)
    nu_intrinsic = 1.0 / (4.0 * np.pi) * sqrt_phi

    d_M = np.log(144000.0 / 1440.0)
    alpha = 0.5
    S = -0.1
    epsilon = 0.0
    nu_observed = nu_intrinsic * np.exp(d_M * alpha * S + epsilon)

    r = np.linspace(0.5, 1.5, n_points)
    theta = np.linspace(0.0, 2.0 * np.pi, n_points)
    phi_angle = np.linspace(0.0, 2.0 * np.pi, n_points)
    R_major = 13.0 / (2.0 * np.pi)

    R_grid, theta_grid, phi_grid = np.meshgrid(r, theta, phi_angle, indexing='ij')
    position = (phi_grid / (2.0 * np.pi)) * 13.0

    u_theta = sqrt_phi / R_grid * np.sin(2.0 * np.pi * phi_grid / 13.0)
    u_phi = np.cos(2.0 * np.pi * theta_grid / 13.0)

    # Evolve u_theta by diffusion in Fourier space
    k = np.fft.fftfreq(n_points, d=1.0 / n_points)
    kx, ky, kz = np.meshgrid(k, k, k, indexing='ij')
    k2 = kx ** 2 + ky ** 2 + kz ** 2
    k2[k2 == 0] = 1e-10
    mask = (np.sqrt(k2) <= 1.0 / 13.0)

    u = u_theta.copy()
    for _ in range(steps):
        u_hat = fftn(u)
        u_hat = u_hat * mask
        u_hat = u_hat * np.exp(-nu_observed * k2 * dt)
        u = np.real(ifftn(u_hat))

    mean_u_theta = float(np.mean(u))
    max_grad_approx = float(np.max(np.gradient(u)[0]))
    energy_density = float(0.5 * np.mean(u ** 2 + u_phi ** 2))

    return {
        "nu_observed": float(nu_observed),
        "mean_u_theta": mean_u_theta,
        "max_grad_approx": max_grad_approx,
        "energy_density": energy_density,
    }


if __name__ == "__main__":
    print(json.dumps(run_torus_demo()))

