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
    outdir = os.path.abspath("results_ablation")
    os.makedirs(outdir, exist_ok=True)

    cases = [
        {"name": "baseline", "args": []},
        {"name": "wedge_only", "args": ["--wedge-halfwidth", "6", "--wedge-half"]},
        {"name": "friction_only", "args": ["--friction-gamma", "0.02"]},
        {"name": "wedge_and_friction", "args": ["--wedge-halfwidth", "6", "--wedge-half", "--friction-gamma", "0.02"]},
    ]
    summaries = {}
    for c in cases:
        print("Running ablation:", c["name"]) 
        out = run([sys.executable, "ufrf_ns_min.py", "--grid", "128", "--steps", "400", "--dt", "0.005", "--eta_over_s_proj", "0.001", "--seed", "1717", "--outdir", outdir] + c["args"]) 
        summaries[c["name"]] = json.loads(out)

    with open(os.path.join(outdir, "AblationSummary.json"), "w") as f:
        json.dump(summaries, f, indent=2)
    print(json.dumps(summaries, indent=2))


if __name__ == "__main__":
    main()

