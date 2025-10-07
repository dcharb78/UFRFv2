
import math
import numpy as np

PHI = (1 + 5 ** 0.5) / 2
SQRT_PHI = PHI ** 0.5

def fibonacci(n):
    F=[0,1]
    for _ in range(2,n+1):
        F.append(F[-1]+F[-2])
    return F

def phi_ladder(max_n=15):
    F = fibonacci(max_n+1)
    ratios = []
    for n in range(2, max_n):
        if F[n+1] != 0:
            ratios.append(F[n]/F[n+1])
    return np.array(sorted(set(ratios)))

def nearest_phi_distance(q, ladder=None):
    q = np.asarray(q)
    if ladder is None:
        ladder = phi_ladder(20)
    ladder = np.unique(np.concatenate([ladder, np.array([1/PHI])]))
    ladder = ladder[(ladder>0) & (ladder<=1)]
    d = np.min(np.abs(q[:,None] - ladder[None,:]), axis=1)
    nearest = ladder[np.argmin(np.abs(q[:,None] - ladder[None,:]), axis=1)]
    return d, nearest

def enrichment_test(q, delta=0.05, ladder=None):
    # Binomial enrichment with exact union coverage over [0,1]
    q = np.asarray(q)
    if ladder is None:
        ladder = phi_ladder(20)
    targets = np.unique(np.concatenate([ladder, np.array([1/PHI])]))
    intervals = []
    for t in targets:
        a, b = max(0.0, float(t-delta)), min(1.0, float(t+delta))
        if b>a: intervals.append((a,b))
    intervals.sort()
    merged = []
    for a,b in intervals:
        if not merged or a>merged[-1][1]:
            merged.append([a,b])
        else:
            merged[-1][1] = max(merged[-1][1], b)
    union_len = sum(b-a for a,b in merged)
    p0 = min(1.0, union_len)
    hits = int(np.any(np.abs(q[:,None]-targets[None,:])<=delta, axis=1).sum())
    n = len(q)
    from math import comb
    pval = 0.0
    for x in range(hits, n+1):
        pval += comb(n, x) * (p0**x) * ((1-p0)**(n-x))
    frac = hits/n if n>0 else 0.0
    return {"n": int(n), "hits": int(hits), "frac": float(frac), "p0": float(p0), "pval": float(pval), "delta": float(delta), "k": int(len(targets))}

def af_ufrf(q, chi1, chi2):
    q = np.asarray(q); chi1=np.asarray(chi1); chi2=np.asarray(chi2)
    return (chi1*q + chi2) / (PHI ** 0.5)

def af_baseline(q, chi1, chi2):
    q = np.asarray(q); chi1=np.asarray(chi1); chi2=np.asarray(chi2)
    w = q/(1+q)
    return w*chi1 + (1-w)*chi2

def rmse(y_true, y_pred):
    y_true=np.asarray(y_true); y_pred=np.asarray(y_pred)
    e = y_true - y_pred
    return float(np.sqrt(np.mean(e*e)))

def aic(n, rss, k):
    return n * math.log(max(rss/n, 1e-12)) + 2*k

def bic(n, rss, k):
    return n * math.log(max(rss/n, 1e-12)) + k * math.log(max(n, 1))

def rayleigh_test(phases):
    phases = np.asarray(phases) % (2*math.pi)
    z = np.exp(1j*phases)
    R = np.abs(np.sum(z))
    n = len(phases)
    Rbar = R/n if n>0 else 0.0
    p = math.exp(-n * Rbar*Rbar) if n>0 else 1.0
    return {"R": float(R), "Rbar": float(Rbar), "n": int(n), "p": float(p)}

def map_to_13_gates(phases):
    gates = 2*math.pi*np.arange(13)/13.0
    phases = np.asarray(phases) % (2*math.pi)
    dmin = []
    for th in phases:
        diff = np.angle(np.exp(1j*(th - gates)))
        dmin.append(np.min(np.abs(diff)))
    return np.array(dmin)

def gate_enrichment(phases, tol=None):
    if tol is None:
        tol = 2*math.pi*(1/13)/4
    phases = np.asarray(phases) % (2*math.pi)
    d = map_to_13_gates(phases)
    hits = int(np.sum(d <= tol))
    n = len(phases)
    p0 = min(1.0, 13*(2*tol)/(2*math.pi))
    from math import comb
    pval = 0.0
    for x in range(hits, n+1):
        pval += comb(n, x) * (p0**x) * ((1-p0)**(n-x))
    return {"n": int(n), "hits": int(hits), "frac": float(hits/max(n,1)), "p0": float(p0), "pval": float(pval), "tol": float(tol)}
