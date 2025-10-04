import subprocess
import os
import sys


def run(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(res.stderr)
        raise SystemExit(res.returncode)
    return res.stdout.strip()


def main():
    outdir = os.path.abspath("results_boundary")
    os.makedirs(outdir, exist_ok=True)
    print("Running lid-driven cavity...")
    print(run([sys.executable, "cavity2d.py", "--n", "64", "--steps", "800", "--dt", "2e-4", "--nu", "0.005", "--U", "1.0", "--outdir", outdir]))
    print("Running channel/Poiseuille...")
    print(run([sys.executable, "channel2d.py", "--n", "64", "--steps", "800", "--dt", "2e-4", "--nu", "0.005", "--dpdx", "-1.0", "--outdir", outdir]))
    with open(os.path.join(outdir, "ResultsBoundary.md"), "w") as f:
        f.writelines([
            "# Boundary Flow Results\n\n",
            "- Cavity: cavity_speed.png, cavity_summary.json\n",
            "- Channel: channel_centerline.png, channel_summary.json\n",
        ])


if __name__ == "__main__":
    main()

