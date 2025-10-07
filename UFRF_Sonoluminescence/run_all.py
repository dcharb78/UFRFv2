#!/usr/bin/env python3
import os, argparse, json
from code.v9_1_core import run_v9_1
def main():
    p=argparse.ArgumentParser(); p.add_argument("--config",default="configs/default.yaml"); args=p.parse_args()
    outdir=os.path.join(os.path.dirname(__file__),"results_v9_1"); os.makedirs(outdir,exist_ok=True)
    res=run_v9_1(outdir,args.config); print("# UFRF v9.1 run complete"); print(json.dumps(res,indent=2))
if __name__=="__main__": main()
