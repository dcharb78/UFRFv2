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
    outdir = os.path.abspath("results_inviscid")
    os.makedirs(outdir, exist_ok=True)

    # Use smaller dt and steps to reduce numerical drift
    out = run([sys.executable, "ufrf_ns_min.py", "--n", "128", "--steps", "800", "--dt", "0.0025", "--nu", "0.0", "--seed", "1717", "--halfwidth-deg", "6", "--init", "random", "--outdir", outdir, "--csv-base", "timeseries_inviscid", "--log-interval", "50"])
    metrics = json.loads(out)
    std = metrics["standard"]
    ufrf = metrics["ufrf"]
    # Report relative energy change
    def rel_change(m):
        e0 = m.get("energy_initial", 0.0)
        ef = m.get("energy_final", 0.0)
        return (ef - e0) / e0 if e0 else 0.0

    lines = [
        "# Inviscid Check (nu=0)\n\n",
        f"Standard relative energy change: {rel_change(std):.4e}\n",
        f"UFRF relative energy change: {rel_change(ufrf):.4e}\n",
    ]
    with open(os.path.join(outdir, "InviscidCheck.md"), "w") as f:
        f.writelines(lines)
    print(json.dumps({"rel_energy_change": {"standard": rel_change(std), "ufrf": rel_change(ufrf)}}, indent=2))


if __name__ == "__main__":
    main()

