from fractions import Fraction
from .utils.ratios import as_ratio, fstr

def build_schedule(cfg):
    total_ps = cfg['ps_total']; segs = cfg['segments_ps']; kappa = cfg['kappa_time']
    segs_eff = [s/float(kappa) for s in segs]
    total_eff = sum(segs_eff)
    den = 10400
    ticks = [as_ratio(s/total_eff).limit_denominator(den) for s in segs_eff]
    b0=as_ratio(0); b1=ticks[0]; b2=ticks[0]+ticks[1]; b3=ticks[0]+ticks[1]+ticks[2]; b4=as_ratio(1)
    return {"boundaries":[fstr(x) for x in (b0,b1,b2,b3,b4)],"ticks":[fstr(x) for x in ticks],
            "kappa": fstr(kappa), "total_ps": fstr(total_ps)}

def generate_pattern(cfg):
    schedule = build_schedule(cfg)
    boundaries=[Fraction(*map(int,b.split('/'))) for b in schedule['boundaries']]
    micro=int(cfg['micro_osc_per_midpoint']); f0=int(cfg['f0'])
    subpeaks=[]; main_pulses=[]; defects=[]; invariants=[]
    dens=set([13,12,36,2*f0])
    seg_ids=['prep1','contract1','prep2','contract2']
    # 36 subpeaks per prep segment
    for si in (0,2):
        seg_name=seg_ids[si]; seg_lo=boundaries[si]; seg_hi=boundaries[si+1]
        for k in range(micro):
            tau=as_ratio(Fraction(k+1,micro+1))
            tf=seg_lo+as_ratio((seg_hi-seg_lo)*tau)
            subpeaks.append({"segment":seg_name,"midpoint":"9/2" if si==0 else "13/2","k":k+1,"t_frac":fstr(tf)})
    # Main pulses 6 then 7
    for si,P in zip((1,3),(6,7)):
        seg_name=seg_ids[si]; seg_lo=boundaries[si]; seg_hi=boundaries[si+1]
        for p in range(P):
            tau=as_ratio(Fraction(p+1,P+1)); tf=seg_lo+as_ratio((seg_hi-seg_lo)*tau)
            main_pulses.append({"segment":seg_name,"source_midpoint":"9/2" if si==1 else "13/2",
                                "land_k":"9/1" if si==1 else "13/1","index":p+1,"t_frac":fstr(tf)})
            dphi=Fraction(1,13*36*(p+1)); defects.append({"segment":seg_name,"index":p+1,"delta_phase":fstr(dphi)})
            dens.add(dphi.denominator)
            invariants.append({"t_frac":fstr(tf),"I_rest":"1/1","proj_quanta":cfg['projection_quanta']})
    # Scale lattice
    import math
    for b in schedule['boundaries']:
        d=int(b.split('/')[-1]); dens.add(d)
    beat=1
    for d in sorted(dens):
        beat=abs(beat*d)//math.gcd(beat,d)
    return {"schedule":schedule,"subpeaks":subpeaks,"main_pulses":main_pulses,
            "defects":defects,"invariants":invariants,
            "scale_lattice":{"denominators":sorted(list(dens)),"beat_LCM":beat}}
