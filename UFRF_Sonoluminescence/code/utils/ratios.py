from fractions import Fraction
def as_ratio(x, max_den=288000):
    if isinstance(x, Fraction): return x
    return Fraction(x).limit_denominator(max_den)
def fstr(x):
    r=as_ratio(x); return f"{r.numerator}/{r.denominator}"
