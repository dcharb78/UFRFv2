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
    outdir = os.path.abspath("results3d")
    os.makedirs(outdir, exist_ok=True)

    print("Running 3D Taylor–Green...")
    tg = run([sys.executable, "ufrf_ns3d.py", "--n", "32", "--steps", "200", "--dt", "0.0015", "--nu", "0.0015", "--outdir", outdir])
    print(tg)

    print("Running 3D forced (Kolmogorov)...")
    kol = run([sys.executable, "ufrf_ns3d.py", "--n", "32", "--steps", "400", "--dt", "0.0015", "--nu", "0.0015", "--outdir", outdir, "--forcing-type", "kolmogorov3d", "--force-amp", "0.01", "--force-kf", "2"])
    print(kol)

    print("Running 3D forced (UFRF shell)...")
    ufrf = run([sys.executable, "ufrf_ns3d.py", "--n", "32", "--steps", "400", "--dt", "0.0015", "--nu", "0.0015", "--outdir", outdir, "--forcing-type", "ufrf_shell", "--force-amp", "0.01", "--force-kmin", "1.0", "--force-kmax", "2.0"])
    print(ufrf)

    # Write Results3D.md
    with open(os.path.join(outdir, "Results3D.md"), "w") as f:
        f.writelines([
            "# 3D Results\n\n",
            "- TG summary: tg_summary.json\n",
            "- TG spectrum: tg_spectrum.png\n",
            "- Forced runs: see tg_timeseries.csv for budgets (P_in, epsilon, residual)\n",
        ])


if __name__ == "__main__":
    main()

