
import os, numpy as np
def main():
    f = np.linspace(1e9, 5e9, 301)
    Z0 = 50.0
    R,L,C = 10.0, 1.5e-9, 1.2e-12
    w = 2*np.pi*f
    Z = R + 1j*w*L + 1/(1j*w*C)
    gamma = (Z-Z0)/(Z+Z0)

    mag = -1.0*np.ones_like(f)
    mag += -20*np.log10(1 + ((f-3e9)/(0.8e9))**4) * 0.02
    phase = -2*np.pi*f*0.3e-9
    s21 = (10**(mag/20.0)) * np.exp(1j*phase)
    theta = 2*np.pi*(np.log(f)-np.log(f.min()))/((np.log(f.max())-np.log(f.min()))/13)
    s21 *= (1 + 0.01*np.sin(theta))
    s12 = 0.1*s21*np.exp(1j*0.2)

    os.makedirs("TESTS", exist_ok=True)
    with open("TESTS/demo_twoport.s2p","w") as fh:
        fh.write("! Demo 2-port\n# Hz S RI R 50\n")
        for i in range(len(f)):
            fh.write(f"{f[i]:.0f} {gamma[i].real:.8f} {gamma[i].imag:.8f} {s21[i].real:.8f} {s21[i].imag:.8f} {s12[i].real:.8f} {s12[i].imag:.8f} {gamma[i].real:.8f} {gamma[i].imag:.8f}\n")
    print("Wrote TESTS/demo_twoport.s2p")
if __name__=="__main__":
    main()
