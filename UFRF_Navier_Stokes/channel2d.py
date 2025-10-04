import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import json


def poiseuille_channel(n=64, steps=3000, dt=1e-4, nu=1e-3, dpdx=-1.0, outdir="results_boundary"):
    os.makedirs(outdir, exist_ok=True)
    # Grid [0,1]x[0,1]
    psi = np.zeros((n, n))
    omega = np.zeros((n, n))
    dx = 1.0 / (n - 1)
    dy = dx

    def apply_boundary(psi, omega):
        psi[0, :] = 0.0
        psi[-1, :] = 0.0
        psi[:, 0] = 0.0
        psi[:, -1] = 0.0
        # No-slip walls top/bottom
        omega[:, 0] = -2.0 * (psi[:, 1] - psi[:, 0]) / (dy ** 2)
        omega[:, -1] = -2.0 * (psi[:, -2] - psi[:, -1]) / (dy ** 2)
        # Zero-gradient for left/right vorticity
        omega[0, :] = omega[1, :]
        omega[-1, :] = omega[-2, :]

    def solve_poisson(psi, omega, iters=100):
        psi_new = psi.copy()
        for _ in range(iters):
            psi_new[1:-1, 1:-1] = 0.25 * (
                psi[2:, 1:-1] + psi[:-2, 1:-1] + psi[1:-1, 2:] + psi[1:-1, :-2] + dx * dx * (-omega[1:-1, 1:-1])
            )
            psi, psi_new = psi_new, psi
            psi[0, :] = 0.0
            psi[-1, :] = 0.0
            psi[:, 0] = 0.0
            psi[:, -1] = 0.0
        return psi

    def velocity(psi):
        u = np.zeros_like(psi)
        v = np.zeros_like(psi)
        u[:, 1:-1] = (psi[:, 2:] - psi[:, :-2]) / (2.0 * dy)
        v[1:-1, :] = -(psi[2:, :] - psi[:-2, :]) / (2.0 * dx)
        # No-slip at walls
        u[:, 0] = 0.0
        u[:, -1] = 0.0
        v[0, :] = 0.0
        v[-1, :] = 0.0
        return u, v

    apply_boundary(psi, omega)

    # Body force equivalent to dp/dx
    Fx = dpdx

    for step in range(steps):
        psi = solve_poisson(psi, omega, iters=10)
        u, v = velocity(psi)
        # Add body force effect to vorticity via curl(F) = -dFx/dy ~ 0 for constant Fx; drive through streamfunction increment
        # Simple explicit drive: u += dt * Fx
        u += dt * Fx
        # Update omega from updated velocity approximately via curl
        dVdx = np.zeros_like(omega)
        dUdy = np.zeros_like(omega)
        dVdx[1:-1, :] = (v[2:, :] - v[:-2, :]) / (2.0 * dx)
        dUdy[:, 1:-1] = (u[:, 2:] - u[:, :-2]) / (2.0 * dy)
        omega = dVdx - dUdy
        # Diffuse omega
        d2wdx2 = np.zeros_like(omega)
        d2wdy2 = np.zeros_like(omega)
        d2wdx2[1:-1, :] = (omega[2:, :] - 2.0 * omega[1:-1, :] + omega[:-2, :]) / (dx ** 2)
        d2wdy2[:, 1:-1] = (omega[:, 2:] - 2.0 * omega[:, 1:-1] + omega[:, :-2]) / (dy ** 2)
        omega += dt * nu * (d2wdx2 + d2wdy2)
        apply_boundary(psi, omega)

    u, v = velocity(psi)
    y = np.linspace(0.0, 1.0, n)
    u_centerline = u[n//2, :]
    plt.figure(figsize=(5, 4))
    plt.plot(y, u_centerline)
    plt.xlabel('y')
    plt.ylabel('u_centerline')
    plt.title('Channel Centerline Velocity')
    plt.savefig(os.path.join(outdir, 'channel_centerline.png'), dpi=150, bbox_inches='tight')
    plt.close()

    # Fit to parabolic profile a*y*(1-y)
    A = np.vstack([y*(1.0 - y), np.ones_like(y)]).T
    coeff, _, _, _ = np.linalg.lstsq(A, u_centerline, rcond=None)
    a = float(coeff[0])
    with open(os.path.join(outdir, 'channel_summary.json'), 'w') as f:
        json.dump({"a_parabola": a}, f, indent=2)
    return {"a_parabola": a}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=64)
    ap.add_argument('--steps', type=int, default=3000)
    ap.add_argument('--dt', type=float, default=1e-4)
    ap.add_argument('--nu', type=float, default=1e-3)
    ap.add_argument('--dpdx', type=float, default=-1.0)
    ap.add_argument('--outdir', type=str, default='results_boundary')
    args = ap.parse_args()
    summary = poiseuille_channel(n=args.n, steps=args.steps, dt=args.dt, nu=args.nu, dpdx=args.dpdx, outdir=args.outdir)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()


