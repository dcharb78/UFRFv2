
import argparse, os, json, numpy as np, pandas as pd
from CODE.touchstone_any import parse_touchstone_any
from CODE.fitter import (
    train_test_split,
    complex_mse,
    fit_reflection_models,
    fit_transmission_models,
    fit_transmission_models_delay,
    apply_delay,
)
from CODE.models import rlc_series_gamma, rlc_series_gamma_ufrf, predict_poly_complex_logf
from CODE.plotters import plot_reflection_overlays, plot_transmission_mag, plot_test_overlays_reflection, plot_test_overlays_transmission

def ensure_dir(p): os.makedirs(p, exist_ok=True)

def run_one(path, outdir, sij="11", prior=True, test_frac=0.2, split="random", n_cycles=13, poly_deg=3, ridge=1e-3, z0_override=None, delay=True, gate_threshold=0.02):
    freqs, Sdict, Z0 = parse_touchstone_any(path)
    if z0_override is not None: Z0 = float(z0_override)
    ij = (sij[0], sij[1])
    if ij not in Sdict: raise ValueError(f"S{sij} not found in {os.path.basename(path)}")
    s = Sdict[ij]
    ensure_dir(outdir)

    # Background plot
    if sij in ("11","22"):
        plot_reflection_overlays(os.path.join(outdir, "smith_overlay.png"), s, f"Smith overlay — {os.path.basename(path)} S{sij}")
    else:
        plot_transmission_mag(os.path.join(outdir, "mag_full.png"), freqs, s, f"|S{sij}| (dB) — {os.path.basename(path)}")

    # Split
    tr_idx, te_idx = train_test_split(freqs, s, test_frac=test_frac, mode=split)
    f_tr, s_tr = freqs[tr_idx], s[tr_idx]
    f_te, s_te = freqs[te_idx],  s[te_idx]

    results = {"input": os.path.basename(path), "Sij": f"S{sij}", "Z0": Z0,
               "train_points": len(tr_idx), "test_points": len(te_idx)}

    if sij in ("11","22"):
        (Rb,Lb,Cb), e_tr_b, (Ru,Lu,Cu,au,phiu), e_tr_u = fit_reflection_models(f_tr, s_tr, Z0, n_cycles=n_cycles)
        s_te_b = rlc_series_gamma(f_te, Rb, Lb, Cb, Z0)
        e_te_b = complex_mse(s_te_b, s_te)
        results["baseline"] = {"model":"RLC series -> Γ", "R":Rb,"L":Lb,"C":Cb, "train_MSE":e_tr_b, "test_MSE":e_te_b}
        if prior:
            s_te_u = rlc_series_gamma_ufrf(f_te, Ru, Lu, Cu, Z0, au, phiu, n_cycles=n_cycles)
            e_te_u = complex_mse(s_te_u, s_te)
            train_impr = (e_tr_b - e_tr_u)/max(1e-15, e_tr_b)
            results["train_improvement_percent"] = 100*train_impr
            results["gate_threshold_percent"] = 100*gate_threshold
            gated_ok = train_impr >= gate_threshold
            results["gated"] = bool(gated_ok)
            if gated_ok:
                results["ufrf_prior"] = {"R":Ru,"L":Lu,"C":Cu,"a":au,"phi":phiu,
                                         "train_MSE":e_tr_u,"test_MSE":e_te_u,
                                         "improvement_percent":100*(e_te_b-e_te_u)/max(1e-15,e_te_b)}
                plot_test_overlays_reflection(os.path.join(outdir,"test_smith_overlay.png"),
                                              os.path.join(outdir,"test_mag_overlay.png"),
                                              f_te, s_te, s_te_b, s_te_u)
            else:
                plot_test_overlays_reflection(os.path.join(outdir,"test_smith_overlay.png"),
                                              os.path.join(outdir,"test_mag_overlay.png"),
                                              f_te, s_te, s_te_b, s_te_b)
        else:
            plot_test_overlays_reflection(os.path.join(outdir,"test_smith_overlay.png"),
                                          os.path.join(outdir,"test_mag_overlay.png"),
                                          f_te, s_te, s_te_b, s_te_b)
    else:
        if delay:
            # Delay-aware fit: estimate tau, phi0 on training, dephase, fit models, then reapply delay to predictions
            (tau, phi0), (wr_b, wi_b), (wr_u, wi_u) = fit_transmission_models_delay(f_tr, s_tr, deg=poly_deg, n_cycles=n_cycles, ridge=ridge)
            # Predict on test (dephased amplitude), then reapply delay
            s_te_b_amp = predict_poly_complex_logf(f_te, wr_b, wi_b, deg=poly_deg, add_ufrf=False)
            s_te_b = apply_delay(f_te, s_te_b_amp, tau, phi0)
            e_te_b = complex_mse(s_te_b, s_te)
            # training errors (compute on train set):
            s_tr_b_amp = predict_poly_complex_logf(f_tr, wr_b, wi_b, deg=poly_deg, add_ufrf=False)
            s_tr_b = apply_delay(f_tr, s_tr_b_amp, tau, phi0)
            e_tr_b = complex_mse(s_tr_b, s_tr)
            results["baseline"] = {"model":f"delay+poly_complex_logf(deg={poly_deg})", "tau":tau, "phi0":phi0, "train_MSE":e_tr_b, "test_MSE":e_te_b}
            if prior:
                s_te_u_amp = predict_poly_complex_logf(f_te, wr_u, wi_u, deg=poly_deg, add_ufrf=True, n_cycles=n_cycles)
                s_te_u = apply_delay(f_te, s_te_u_amp, tau, phi0)
                e_te_u = complex_mse(s_te_u, s_te)
                # training counterpart for gating
                s_tr_u_amp = predict_poly_complex_logf(f_tr, wr_u, wi_u, deg=poly_deg, add_ufrf=True, n_cycles=n_cycles)
                s_tr_u = apply_delay(f_tr, s_tr_u_amp, tau, phi0)
                e_tr_u = complex_mse(s_tr_u, s_tr)
                train_impr = (e_tr_b - e_tr_u)/max(1e-15, e_tr_b)
                results["train_improvement_percent"] = 100*train_impr
                results["gate_threshold_percent"] = 100*gate_threshold
                gated_ok = train_impr >= gate_threshold
                results["gated"] = bool(gated_ok)
                if gated_ok:
                    results["ufrf_prior"] = {"model":f"delay+poly+UF(deg={poly_deg},13-cycles)", "ridge":ridge,
                                             "train_MSE":e_tr_u, "test_MSE":e_te_u,
                                             "improvement_percent":100*(e_te_b-e_te_u)/max(1e-15,e_te_b)}
                    plot_test_overlays_transmission(os.path.join(outdir,"test_complex_overlay.png"),
                                                    os.path.join(outdir,"test_mag_overlay.png"),
                                                    f_te, s_te, s_te_b, s_te_u)
                else:
                    plot_test_overlays_transmission(os.path.join(outdir,"test_complex_overlay.png"),
                                                    os.path.join(outdir,"test_mag_overlay.png"),
                                                    f_te, s_te, s_te_b, s_te_b)
            else:
                plot_test_overlays_transmission(os.path.join(outdir,"test_complex_overlay.png"),
                                                os.path.join(outdir,"test_mag_overlay.png"),
                                                f_te, s_te, s_te_b, s_te_b)
        else:
            (wr_b, wi_b), (wr_u, wi_u) = fit_transmission_models(f_tr, s_tr, deg=poly_deg, n_cycles=n_cycles, ridge=ridge)
            s_te_b = predict_poly_complex_logf(f_te, wr_b, wi_b, deg=poly_deg, add_ufrf=False)
            e_te_b = complex_mse(s_te_b, s_te)
            results["baseline"] = {"model":f"poly_complex_logf(deg={poly_deg})", "train_MSE":None, "test_MSE":e_te_b}
            if prior:
                s_te_u = predict_poly_complex_logf(f_te, wr_u, wi_u, deg=poly_deg, add_ufrf=True, n_cycles=n_cycles)
                e_te_u = complex_mse(s_te_u, s_te)
                results["ufrf_prior"] = {"model":f"poly+UF(deg={poly_deg},13-cycles)", "ridge":ridge,
                                         "train_MSE":None, "test_MSE":e_te_u,
                                         "improvement_percent":100*(e_te_b-e_te_u)/max(1e-15,e_te_b)}
                plot_test_overlays_transmission(os.path.join(outdir,"test_complex_overlay.png"),
                                                os.path.join(outdir,"test_mag_overlay.png"),
                                                f_te, s_te, s_te_b, s_te_u)
            else:
                plot_test_overlays_transmission(os.path.join(outdir,"test_complex_overlay.png"),
                                                os.path.join(outdir,"test_mag_overlay.png"),
                                                f_te, s_te, s_te_b, s_te_b)

    rows=[{"Model":"Baseline (test)","MSE_complex":results["baseline"]["test_MSE"]}]
    if "ufrf_prior" in results:
        rows.append({"Model":"UFRF prior (test)","MSE_complex":results["ufrf_prior"]["test_MSE"]})
    import pandas as pd
    pd.DataFrame(rows).to_csv(os.path.join(outdir,"metrics.csv"), index=False)

    with open(os.path.join(outdir,"params.json"),"w") as f:
        json.dump(results, f, indent=2)

    rep=[f"# S-parameter Predictive-Prior Test — {os.path.basename(path)} (S{sij})",
         f"- Z0: {Z0:.2f} Ω",
         f"- Train points: {len(tr_idx)}  |  Test points: {len(te_idx)}",
         "",
         "## Baseline",
         f"- {results['baseline']}"]
    if "ufrf_prior" in results:
        rep += ["","## UFRF Prior", f"- {results['ufrf_prior']}",
                f"**Held-out improvement:** {results['ufrf_prior']['improvement_percent']:.2f}%"]
    with open(os.path.join(outdir,"report.md"),"w") as f:
        f.write("\n".join(rep))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=False, default="TESTS/demo_twoport.s2p", help="Touchstone .s1p/.s2p file")
    ap.add_argument("--sij", default="11", help="Which Sij to fit: 11,21,12,22")
    ap.add_argument("--outdir", required=False, default="results/demo", help="Output directory")
    ap.add_argument("--prior", choices=["on","off"], default="on", help="Enable UFRF prior")
    ap.add_argument("--test-frac", type=float, default=0.2)
    ap.add_argument("--split", choices=["random","interleave"], default="random")
    ap.add_argument("--n-cycles", type=int, default=13)
    ap.add_argument("--poly-deg", type=int, default=3)
    ap.add_argument("--ridge", type=float, default=1e-3)
    ap.add_argument("--z0", type=float, default=None)
    ap.add_argument("--delay", choices=["on","off"], default="on", help="Enable delay-aware transmission modeling (S21/S12)")
    ap.add_argument("--gate-threshold", type=float, default=0.02, help="Gating threshold on train improvement (fraction, e.g., 0.02 = 2%)")
    args = ap.parse_args()
    run_one(args.input, args.outdir, sij=args.sij, prior=(args.prior=="on"),
            test_frac=args.test_frac, split=args.split, n_cycles=args.n_cycles,
            poly_deg=args.poly_deg, ridge=args.ridge, z0_override=args.z0,
            delay=(args.delay=="on"), gate_threshold=args.gate_threshold)

if __name__ == "__main__":
    main()
