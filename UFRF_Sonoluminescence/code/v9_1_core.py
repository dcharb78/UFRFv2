import os, csv, json, yaml
from .scheduler import generate_pattern

def write_csv(path, rows):
    if not rows: return
    cols=list(rows[0].keys())
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)

def run_v9_1(outdir, cfg_path):
    cfg=yaml.safe_load(open(cfg_path))
    os.makedirs(outdir,exist_ok=True)
    pat=generate_pattern(cfg)
    open(os.path.join(outdir,"pattern_schedule.json"),"w").write(json.dumps(pat["schedule"],indent=2))
    write_csv(os.path.join(outdir,"subpeaks.csv"), pat["subpeaks"])
    write_csv(os.path.join(outdir,"main_pulses.csv"), pat["main_pulses"])
    write_csv(os.path.join(outdir,"commutation_defects.csv"), pat["defects"])
    write_csv(os.path.join(outdir,"invariants.csv"), pat["invariants"])
    open(os.path.join(outdir,"scale_lattice.json"),"w").write(json.dumps(pat["scale_lattice"],indent=2))
    return {"subpeaks":len(pat["subpeaks"]), "main_pulses":len(pat["main_pulses"]), "beat_LCM":pat["scale_lattice"]["beat_LCM"]}
