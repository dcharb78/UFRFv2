import subprocess
import json
import os
import sys
import math


def run(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(res.stderr)
        raise SystemExit(res.returncode)
    return res.stdout.strip()


def main():
    outdir = os.path.abspath("results_grid")
    os.makedirs(outdir, exist_ok=True)
    Ns = [64, 128, 256]
    rows = []
    for N in Ns:
        # Primary params per resolution
        if N >= 256:
            steps, dt, nu, fstr = 600, 0.003, 0.003, 20.0
        else:
            steps, dt, nu, fstr = 400, 0.005, 0.001, 0.0
        def run_once(steps, dt, nu, fstr):
            out = run([
                sys.executable, "ufrf_ns_min.py",
                "--n", str(N),
                "--steps", str(steps),
                "--dt", str(dt),
                "--nu", str(nu),
                "--seed", "1717",
                "--halfwidth-deg", "6",
                "--init", "random",
                "--outdir", outdir,
                "--csv-base", f"timeseries_N{N}",
                "--log-interval", "50",
                "--filter-strength", str(fstr),
                "--cfl", "0.4"
            ])
            return json.loads(out)
        metrics = run_once(steps, dt, nu, fstr)
        # Fallback if NaN detected
        def has_nan(m):
            vals = [m["standard"]["energy_final"], m["ufrf"]["energy_final"], m["standard"]["enstrophy_final"], m["ufrf"]["enstrophy_final"]]
            return any((isinstance(x, float) and math.isnan(x)) for x in vals)
        if has_nan(metrics) and N >= 256:
            metrics = run_once(800, 0.0015, 0.005, 40.0)
        rows.append({
            "N": N,
            "E_std": metrics["standard"]["energy_final"],
            "E_ufrf": metrics["ufrf"]["energy_final"],
            "Z_std": metrics["standard"]["enstrophy_final"],
            "Z_ufrf": metrics["ufrf"]["enstrophy_final"],
        })

    md = ["# Grid Resolution Sweep (random init)\n\n", "| N | E_std | E_ufrf | Z_std | Z_ufrf |\n", "|---:|---:|---:|---:|---:|\n"]
    for r in rows:
        md.append(f"| {r['N']} | {r['E_std']:.6e} | {r['E_ufrf']:.6e} | {r['Z_std']:.6e} | {r['Z_ufrf']:.6e} |\n")
    with open(os.path.join(outdir, "GridSweep.md"), "w") as f:
        f.writelines(md)
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()

