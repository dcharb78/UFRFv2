# Theory Cheat‑Sheet

## Smith chart geometry (reflections)
Normalized impedance z = Z/Z0 = r + jx, reflection coefficient Γ:
\[ \Gamma = \frac{z-1}{z+1}. \]
Right‑half plane (r>0) maps inside |Γ| ≤ 1. Constant‑r and constant‑x loci are circles.

## Transmission (S21, S12) and others
Not plotted on the Smith chart (that’s for reflection), but we still evaluate **complex error**
directly in the complex plane and in |S| (dB).

## UFRF prior (lightweight, testable)
We **don’t change** the mapping; we add a **predictive prior**: a small, log‑periodic ripple
coherent across the log‑frequency span, with ~13 cycles. In this package it is implemented as:

- For **S11/S22**: baseline **series RLC** impedance model → Γ; UFRF prior modulates the **reactive** part
  with a 13‑cycle sinusoid (phase free, small amplitude with a penalty).
- For **S21/S12**: baseline smooth **complex polynomial** in log(f) (degree 3) fit by least‑squares;
  UFRF prior adds fixed‑frequency sinusoid features (sin/cos over 13 cycles) with light ridge penalty.

**Metric:** held‑out **complex** MSE on Sij, not just magnitude. We also plot |S| in dB for intuition.
