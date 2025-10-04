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
    outdir = os.path.abspath("results")
    os.makedirs(outdir, exist_ok=True)

    # Random init
    print("Running random-init...")
    out = run([sys.executable, "ufrf_ns_min.py", "--n", "128", "--steps", "400", "--dt", "0.005", "--nu", "0.001", "--seed", "1717", "--halfwidth-deg", "6", "--include-half", "--init", "random", "--outdir", outdir])
    metrics_random = json.loads(out) if out else {}

    # Shear init
    print("Running shear-init...")
    out = run([
        sys.executable, "ufrf_ns_min.py",
        "--n", "256",
        "--steps", "800",
        "--dt", "0.001",
        "--nu", "0.002",
        "--seed", "1717",
        "--halfwidth-deg", "6",
        "--include-half",
        "--init", "shear",
        "--delta", "0.05",
        "--u0", "1.0",
        "--noise-eps", "0.0005",
        "--filter-strength", "20.0",
        "--filter-order", "8",
        "--outdir", outdir
    ])
    metrics_shear = json.loads(out) if out else {}

    # Torus demo
    print("Running torus demo...")
    out = run([sys.executable, "torus_demo.py"])
    metrics_torus = json.loads(out) if out else {}

    results = {
        "random": metrics_random,
        "shear": metrics_shear,
        "outdir": outdir,
        "torus": metrics_torus,
    }

    # Write Results.md
    lines = [
        "# Results\n",
        "\n",
        "## Random Initialization\n",
        f"Standard: {metrics_random.get('standard')}\n",
        f"UFRF: {metrics_random.get('ufrf')}\n",
        f"Spectra: {os.path.join(outdir, 'spectrum_compare_random.png')}\n",
        f"Vorticity (Std): {os.path.join(outdir, 'snapshot_vorticity_standard_random.png')}\n",
        f"Vorticity (UFRF): {os.path.join(outdir, 'snapshot_vorticity_ufrf13_random.png')}\n",
        "\n",
        "## Shear Initialization\n",
        f"Standard: {metrics_shear.get('standard')}\n",
        f"UFRF: {metrics_shear.get('ufrf')}\n",
        f"Spectra: {os.path.join(outdir, 'spectrum_compare_shear.png')}\n",
        f"Vorticity (Std): {os.path.join(outdir, 'snapshot_vorticity_standard_shear.png')}\n",
        f"Vorticity (UFRF): {os.path.join(outdir, 'snapshot_vorticity_ufrf13_shear.png')}\n",
        "\n",
        "\n",
        "## Torus Diffusion Demo (3D)\n",
        f"Metrics: {metrics_torus}\n",
        "\n",
        "---\n",
        "References: UFRF consolidated repo `UFRFv2` (https://github.com/dcharb78/UFRFv2)\n",
    ]
    with open(os.path.join(outdir, "Results.md"), "w") as f:
        f.writelines(lines)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

