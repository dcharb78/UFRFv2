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
    outdir = os.path.abspath("results_forced")
    os.makedirs(outdir, exist_ok=True)
    # Moderate resolution with CFL and forcing
    # Kolmogorov forcing
    out = run([
        sys.executable, "ufrf_ns_min.py",
        "--n", "256",
        "--steps", "2000",
        "--dt", "0.001",
        "--nu", "0.0015",
        "--seed", "1717",
        "--halfwidth-deg", "6",
        "--include-half",
        "--init", "random",
        "--outdir", outdir,
        "--csv-base", "timeseries_forced",
        "--log-interval", "50",
        "--cfl", "0.2",
        "--filter-strength", "20.0",
        "--forcing", "kolmogorov",
        "--force-amp", "0.01",
        "--force-kf", "4",
        "--friction-gamma", "0.02",
    ])
    metrics = json.loads(out)
    with open(os.path.join(outdir, "ForcedTurbulence.json"), "w") as f:
        json.dump(metrics, f, indent=2)
    print(json.dumps(metrics, indent=2))

    # UFRF wedge forcing comparison (same settings, different forcing)
    out_ufrf = run([
        sys.executable, "ufrf_ns_min.py",
        "--n", "256",
        "--steps", "2000",
        "--dt", "0.001",
        "--nu", "0.0015",
        "--seed", "1717",
        "--halfwidth-deg", "6",
        "--include-half",
        "--init", "random",
        "--outdir", outdir,
        "--csv-base", "timeseries_forced_ufrf",
        "--log-interval", "50",
        "--cfl", "0.2",
        "--filter-strength", "20.0",
        "--forcing", "ufrf_wedge",
        "--force-amp", "0.01",
        "--force-kmin", "1.0",
        "--force-kmax", "4.0",
        "--friction-gamma", "0.02",
    ])
    metrics_ufrf = json.loads(out_ufrf)
    with open(os.path.join(outdir, "ForcedTurbulenceUFRF.json"), "w") as f:
        json.dump(metrics_ufrf, f, indent=2)
    print(json.dumps({"kolmogorov": metrics, "ufrf_wedge": metrics_ufrf}, indent=2))


if __name__ == "__main__":
    main()

