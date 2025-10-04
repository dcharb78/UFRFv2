import subprocess
import json
import os
import sys


def run(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(res.stderr)
        raise SystemExit(res.returncode)
    return res.stdout.strip()


def main():
    outdir = os.path.abspath("results_sweep")
    os.makedirs(outdir, exist_ok=True)
    halfwidths = [3, 6, 9]
    table = []
    for hw in halfwidths:
        out = run([sys.executable, "ufrf_ns_min.py", "--n", "128", "--steps", "400", "--dt", "0.005", "--nu", "0.001", "--seed", "1717", "--halfwidth-deg", str(hw), "--include-half", "--init", "random", "--outdir", outdir, "--csv-base", f"timeseries_hw{hw}", "--log-interval", "50"])
        metrics = json.loads(out)
        row = {
            "halfwidth_deg": hw,
            "std_energy_final": metrics["standard"]["energy_final"],
            "ufrf_energy_final": metrics["ufrf"]["energy_final"],
            "std_enstrophy_final": metrics["standard"]["enstrophy_final"],
            "ufrf_enstrophy_final": metrics["ufrf"]["enstrophy_final"],
        }
        table.append(row)

    md = ["# Halfwidth Sweep (random init)\n\n", "| halfwidth_deg | E_std | E_ufrf | Z_std | Z_ufrf |\n", "|---:|---:|---:|---:|---:|\n"]
    for r in table:
        md.append(f"| {r['halfwidth_deg']} | {r['std_energy_final']:.6e} | {r['ufrf_energy_final']:.6e} | {r['std_enstrophy_final']:.6e} | {r['ufrf_enstrophy_final']:.6e} |\n")
    with open(os.path.join(outdir, "HalfwidthSweep.md"), "w") as f:
        f.writelines(md)
    print(json.dumps(table, indent=2))


if __name__ == "__main__":
    main()

