
# touchstone_any: parse .s1p/.s2p (v1-style) with MA/DB/RI; return dict of Sij
import re, numpy as np

def _hdr(tokens):
    fmt = tokens[0].upper() if tokens else "GHZ"
    kind = tokens[1].upper() if len(tokens)>1 else "S"
    rep  = tokens[2].upper() if len(tokens)>2 else "MA"
    Z0 = 50.0
    if "R" in tokens:
        try:
            i = tokens.index('R')
            Z0 = float(tokens[i+1])
        except Exception:
            pass
    return fmt, kind, rep, Z0

def _unit(u):
    return {"HZ":1.0,"KHZ":1e3,"MHZ":1e6,"GHZ":1e9}.get(u.upper(),1.0)

def parse_touchstone_any(path):
    # Returns freqs (Hz), Sdict {('1','1'): arr, ('2','1'): arr, ...}, Z0 (float)
    fmt="GHZ"; kind="S"; rep="MA"; Z0=50.0
    rows=[]; header_seen=False
    with open(path,"r",errors="ignore") as f:
        for raw in f:
            line=raw.strip()
            if not line or line.startswith("!"):
                continue
            if line.startswith("#"):
                fmt,kind,rep,Z0 = _hdr(line[1:].split())
                header_seen=True
                continue
            parts=re.split(r"[,\s]+", line)
            if parts:
                rows.append(parts)
    if not rows:
        raise RuntimeError("No numeric rows in file.")
    if not header_seen:
        fmt="GHZ"; kind="S"; rep="MA"
    unit=_unit(fmt)
    ext=path.lower().split(".")[-1]
    nports=1 if ext=="s1p" else (2 if ext=="s2p" else None)
    freqs=[]; S={}
    if nports==1:
        for r in rows:
            f=float(r[0])*unit; a,b=float(r[1]),float(r[2])
            if rep=="RI": g=a+1j*b
            elif rep=="DB": g=(10**(a/20.0))*np.exp(1j*np.deg2rad(b))
            else: g=a*np.exp(1j*np.deg2rad(b))
            freqs.append(f); S.setdefault(("1","1"),[]).append(g)
    else:
        for r in rows:
            f=float(r[0])*unit; vals=list(map(float,r[1:]))
            if len(vals) < 8:
                pairs=[vals[0:2], vals[2:4]]  # S11,S21
                keys=[("1","1"),("2","1")]
            else:
                pairs=[vals[0:2], vals[2:4], vals[4:6], vals[6:8]]  # S11,S21,S12,S22
                keys=[("1","1"),("2","1"),("1","2"),("2","2")]
            freqs.append(f)
            comp=[]
            for a,b in pairs:
                if rep=="RI": g=a+1j*b
                elif rep=="DB": g=(10**(a/20.0))*np.exp(1j*np.deg2rad(b))
                else: g=a*np.exp(1j*np.deg2rad(b))
                comp.append(g)
            for k,g in zip(keys,comp):
                S.setdefault(k,[]).append(g)
    freqs=np.array(freqs,float)
    for k in list(S.keys()):
        S[k]=np.array(S[k],complex)
    return freqs,S,float(Z0)
