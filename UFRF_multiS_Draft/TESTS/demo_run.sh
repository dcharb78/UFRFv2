#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python CODE/generate_synth_oneport.py
python CODE/generate_synth_twport.py
python CODE/run_prior_test.py --input TESTS/demo_oneport.s1p --sij 11 --outdir results/demo_s11
python CODE/run_prior_test.py --input TESTS/demo_twoport.s2p --sij 21 --outdir results/demo_s21
