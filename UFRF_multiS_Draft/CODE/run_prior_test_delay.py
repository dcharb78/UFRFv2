
import argparse, os, json, numpy as np, pandas as pd
from CODE.touchstone_any import parse_touchstone_any
from CODE.s21_delay_model import fit_delay_aware
from CODE.fitter import train_test_split, complex_mse
from CODE.plotters import plot_transmission_mag, plot_test_overlays_transmission

def ensure_dir(p): os.makedirs(p, exist_ok=True)

def run_one(path, outdir, sij="21", split="block", test_frac=0.2, block_frac=0.2, deg=3, ridge=1e-3, n_cycles=13, gate=0.02):
    freqs, Sdict, Z0 = parse_touchstone_any(path)
    ij = (sij[0], sij[1])
    if ij not in Sdict: raise ValueError(f"S{sij} not found in {os.path.basename(path)}")
    S = Sdict[ij]
    ensure_dir(outdir)
    plot_transmission_mag(os.path.join(outdir, "mag_full.png"), freqs, S, f"|S{sij}| (dB) — {os.path.basename(path)}")
    N = len(freqs); idx = np.arange(N)
    if split=="block":
        n_test = max(5, int(N*block_frac))
        te_idx = idx[-n_test:]
        tr_idx = idx[:-n_test]
    else:
        mode = "interleave" if split=="interleave" else "random"
        tr_idx, te_idx = train_test_split(freqs, S, test_frac=test_frac, mode=mode)
    f_tr, s_tr = freqs[tr_idx], S[tr_idx]
    f_te, s_te = freqs[te_idx],  S[te_idx]

    params_b, pred_b = fit_delay_aware(f_tr, s_tr, deg=deg, ridge=ridge, n_cycles=n_cycles, gate=1e9)
    s_hat_b = pred_b(f_te); e_te_b = complex_mse(s_hat_b, s_te)

    params_u, pred_u = fit_delay_aware(f_tr, s_tr, deg=deg, ridge=ridge, n_cycles=n_cycles, gate=gate)
    s_hat_u = pred_u(f_te); e_te_u = complex_mse(s_hat_u, s_te)

    results = {"input": os.path.basename(path), "Sij": f"S{sij}","split": split,"test_points": int(len(te_idx)),
               "deg": deg,"ridge": ridge,"n_cycles": n_cycles,"gate": gate,"Z0": Z0,
               "baseline_test_MSE": e_te_b,"ufrf_test_MSE": e_te_u,
               "improvement_percent": 100.0*(e_te_b - e_te_u)/max(1e-15, e_te_b),
               "train_gain_used": params_u.get("train_gain", None),"used_ufrf": params_u.get("use_uf", False),
               "tau_est": params_u["tau"], "phi0_est": params_u["phi0"]}

    pd.DataFrame([{"Model":"Baseline (delay-aware, no ripple)","MSE_complex": e_te_b},
                  {"Model":"Delay-aware + UFRF prior","MSE_complex": e_te_u}
                 ]).to_csv(os.path.join(outdir,"metrics.csv"), index=False)

    with open(os.path.join(outdir,"params.json"),"w") as f:
        json.dump(results, f, indent=2)

    plot_test_overlays_transmission(os.path.join(outdir,"test_complex_overlay.png"),
                                    os.path.join(outdir,"test_mag_overlay.png"),
                                    f_te, s_te, s_hat_b, s_hat_u)

    with open(os.path.join(outdir,"report.md"),"w") as f:
        f.write(f"# Delay-aware S{sij} test — {os.path.basename(path)}\\n")
        f.write(f"- split: {split}, test_points: {len(te_idx)}\\n")
        f.write(f"- baseline_test_MSE: {e_te_b:.6g}\\n- ufrf_test_MSE: {e_te_u:.6g}\\n")
        f.write(f"- improvement: {results['improvement_percent']:.2f}%\\n")
        f.write(f"- tau_est: {results['tau_est']:.4e} s, phi0_est: {results['phi0_est']:.3f} rad\\n")
        f.write(f"- used_ufrf: {results['used_ufrf']} (gate={gate}, train_gain={results['train_gain_used']:.4f})\\n")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--sij", choices=["21","12"], default="21")
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--split", choices=["random","interleave","block"], default="block")
    ap.add_argument("--test-frac", type=float, default=0.2)
    ap.add_argument("--block-frac", type=float, default=0.2)
    ap.add_argument("--deg", type=int, default=3)
    ap.add_argument("--ridge", type=float, default=1e-3)
    ap.add_argument("--n-cycles", type=int, default=13)
    ap.add_argument("--gate", type=float, default=0.02)
    args = ap.parse_args()
    run_one(args.input, args.outdir, sij=args.sij, split=args.split, test_frac=args.test_frac,
            block_frac=args.block_frac, deg=args.deg, ridge=args.ridge, n_cycles=args.n_cycles, gate=args.gate)

if __name__=="__main__":
    main()
