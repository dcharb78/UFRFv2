
import os, numpy as np
def main():
    f = np.linspace(0.8e9, 2.5e9, 201)
    Z0 = 50.0
    R,L,C = 5.0, 2.2e-9, 1.5e-12
    w = 2*np.pi*f
    Z = R + 1j*w*L + 1/(1j*w*C)
    ripple = 0.012*np.sin(2*np.pi*np.log10(f/f.min())/((np.log10(f.max())-np.log10(f.min()))/3.0))
    Z = Z*(1+ripple)
    g = (Z-Z0)/(Z+Z0)
    lines = ["! Demo S11", "# Hz S RI R 50"]
    for fi, gi in zip(f, g):
        lines.append(f"{fi:.0f} {gi.real:.8f} {gi.imag:.8f}")
    os.makedirs("TESTS", exist_ok=True)
    with open("TESTS/demo_oneport.s1p","w") as fh: fh.write("\n".join(lines))
    print("Wrote TESTS/demo_oneport.s1p")
if __name__=="__main__":
    main()
