import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import json


def lid_driven_cavity(n=64, steps=5000, dt=1e-4, nu=1e-3, U=1.0, outdir="results_boundary"):
    os.makedirs(outdir, exist_ok=True)
    # Grid in [0,1]x[0,1]
    psi = np.zeros((n, n))
    omega = np.zeros((n, n))
    dx = 1.0 / (n - 1)
    dy = dx

    def apply_boundary(psi, omega):
        # No-slip on all walls; moving lid at top: u=U, v=0
        # Streamfunction constant at walls
        psi[0, :] = 0.0
        psi[-1, :] = 0.0
        psi[:, 0] = 0.0
        psi[:, -1] = 0.0
        # Vorticity boundary using Thom formula
        # Bottom y=0
        omega[:, 0] = -2.0 * (psi[:, 1] - psi[:, 0]) / (dy ** 2)
        # Top y=1 with moving lid u=U => psi boundary same, add -2U/dy
        omega[:, -1] = -2.0 * (psi[:, -2] - psi[:, -1]) / (dy ** 2) - 2.0 * U / dy
        # Left x=0
        omega[0, :] = -2.0 * (psi[1, :] - psi[0, :]) / (dx ** 2)
        # Right x=1
        omega[-1, :] = -2.0 * (psi[-2, :] - psi[-1, :]) / (dx ** 2)

    def solve_poisson(psi, omega, iters=100):
        # Jacobi iterations for ∇^2 psi = -omega
        psi_new = psi.copy()
        for _ in range(iters):
            psi_new[1:-1, 1:-1] = 0.25 * (
                psi[2:, 1:-1] + psi[:-2, 1:-1] + psi[1:-1, 2:] + psi[1:-1, :-2] + dx * dx * (-omega[1:-1, 1:-1])
            )
            psi, psi_new = psi_new, psi
            # Enforce Dirichlet boundaries
            psi[0, :] = 0.0
            psi[-1, :] = 0.0
            psi[:, 0] = 0.0
            psi[:, -1] = 0.0
        return psi

    def velocity(psi):
        # u = d psi/dy, v = -d psi/dx (central differences)
        u = np.zeros_like(psi)
        v = np.zeros_like(psi)
        u[:, 1:-1] = (psi[:, 2:] - psi[:, :-2]) / (2.0 * dy)
        v[1:-1, :] = -(psi[2:, :] - psi[:-2, :]) / (2.0 * dx)
        # Enforce lid velocity at top boundary
        u[:, -1] = U
        u[:, 0] = 0.0
        v[:, 0] = 0.0
        v[:, -1] = 0.0
        u[0, :] = 0.0
        u[-1, :] = 0.0
        v[0, :] = 0.0
        v[-1, :] = 0.0
        return u, v

    apply_boundary(psi, omega)

    for step in range(steps):
        # Solve Poisson for psi from current omega
        psi = solve_poisson(psi, omega, iters=10)
        u, v = velocity(psi)
        # Compute advection and diffusion for omega
        dwdx = np.zeros_like(omega)
        dwdy = np.zeros_like(omega)
        d2wdx2 = np.zeros_like(omega)
        d2wdy2 = np.zeros_like(omega)
        dwdx[1:-1, :] = (omega[2:, :] - omega[:-2, :]) / (2.0 * dx)
        dwdy[:, 1:-1] = (omega[:, 2:] - omega[:, :-2]) / (2.0 * dy)
        d2wdx2[1:-1, :] = (omega[2:, :] - 2.0 * omega[1:-1, :] + omega[:-2, :]) / (dx ** 2)
        d2wdy2[:, 1:-1] = (omega[:, 2:] - 2.0 * omega[:, 1:-1] + omega[:, :-2]) / (dy ** 2)
        adv = u * dwdx + v * dwdy
        diff = nu * (d2wdx2 + d2wdy2)
        omega[1:-1, 1:-1] += dt * (-adv[1:-1, 1:-1] + diff[1:-1, 1:-1])
        apply_boundary(psi, omega)

    # Plot velocity magnitude
    u, v = velocity(psi)
    speed = np.sqrt(u ** 2 + v ** 2)
    plt.figure(figsize=(5, 4))
    plt.imshow(speed.T, origin='lower', cmap='viridis')
    plt.colorbar(label='|u|')
    plt.title('Lid-Driven Cavity Speed')
    plt.savefig(os.path.join(outdir, 'cavity_speed.png'), dpi=150, bbox_inches='tight')
    plt.close()

    center_u = float(u[n//2, n-2])
    center_v = float(v[n//2, n//2])
    with open(os.path.join(outdir, 'cavity_summary.json'), 'w') as f:
        json.dump({"center_u": center_u, "center_v": center_v}, f, indent=2)

    return {"center_u": center_u, "center_v": center_v}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=64)
    ap.add_argument('--steps', type=int, default=5000)
    ap.add_argument('--dt', type=float, default=1e-4)
    ap.add_argument('--nu', type=float, default=1e-3)
    ap.add_argument('--U', type=float, default=1.0)
    ap.add_argument('--outdir', type=str, default='results_boundary')
    args = ap.parse_args()
    summary = lid_driven_cavity(n=args.n, steps=args.steps, dt=args.dt, nu=args.nu, U=args.U, outdir=args.outdir)
    print(json.dumps(summary))


if __name__ == '__main__':
    main()


