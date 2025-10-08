
import numpy as np, matplotlib.pyplot as plt
def smith_background(ax):
    t = np.linspace(0, 2*np.pi, 1000)
    ax.plot(np.cos(t), np.sin(t))
    for r in [0, 0.2, 0.5, 1, 2, 5]:
        c = r/(1+r); R = 1/(1+r)
        ax.plot(c + R*np.cos(t), R*np.sin(t), linewidth=0.3, alpha=0.5)
    for x in [0.2, 0.5, 1, 2, 5]:
        for sgn in (+1,-1):
            c = 1 + 1j*sgn/x; R = 1/abs(x)
            z = c + R*np.exp(1j*t)
            mask = np.abs(z) <= 1.001
            ax.plot(z.real[mask], z.imag[mask], linewidth=0.3, alpha=0.5)
    ax.set_aspect('equal'); ax.set_xlim(-1.1,1.1); ax.set_ylim(-1.1,1.1)
    ax.set_xlabel("Re(Γ)"); ax.set_ylabel("Im(Γ)")
