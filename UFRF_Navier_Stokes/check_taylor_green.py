import subprocess
import json
import os
import sys
import numpy as np


def run(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(res.stderr)
        raise SystemExit(res.returncode)
    return res.stdout.strip()


def main():
    outdir = os.path.abspath("results_tg")
    os.makedirs(outdir, exist_ok=True)
    # Analytical decay for Taylor–Green at wavenumber k=2π: E(t) = E0 * exp(-2 ν k^2 t)
    # With our normalization, initial E0 ~ 0.25; we extract E0 from metrics instead of assuming
    dt = 0.0025
    steps = 800
    nu = 0.001
    out = run([sys.executable, "ufrf_ns_min.py", "--n", "128", "--steps", str(steps), "--dt", str(dt), "--nu", str(nu), "--seed", "1717", "--halfwidth-deg", "6", "--init", "taylor_green", "--outdir", outdir, "--csv-base", "timeseries_tg", "--log-interval", "40"])
    metrics = json.loads(out)

    E0_std = metrics["standard"]["energy_initial"]
    Ef_std = metrics["standard"]["energy_final"]
    E0_ufrf = metrics["ufrf"]["energy_initial"]
    Ef_ufrf = metrics["ufrf"]["energy_final"]

    t = steps * dt
    k = 2.0 * np.pi
    E_pred = lambda E0: E0 * np.exp(-2.0 * nu * (k ** 2) * t)

    lines = [
        "# Taylor–Green Validation\n\n",
        f"Standard: E0={E0_std:.6e}, Ef={Ef_std:.6e}, E_pred={E_pred(E0_std):.6e}\n",
        f"UFRF:     E0={E0_ufrf:.6e}, Ef={Ef_ufrf:.6e}, E_pred={E_pred(E0_ufrf):.6e}\n",
    ]
    with open(os.path.join(outdir, "TaylorGreen.md"), "w") as f:
        f.writelines(lines)
    print(json.dumps({
        "standard": {"E0": E0_std, "Ef": Ef_std, "E_pred": float(E_pred(E0_std))},
        "ufrf": {"E0": E0_ufrf, "Ef": Ef_ufrf, "E_pred": float(E_pred(E0_ufrf))}
    }, indent=2))


if __name__ == "__main__":
    main()

