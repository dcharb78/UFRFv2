# Data You Can Download (10–50+ candidates)

Put downloaded `.s1p/.s2p` files into `DATA/`. Then run `run_batch.py` or the single‑file CLI.

## 1) scikit‑rf sample data (simulated 2‑port; famous demo)
- **ring slot** example (`ring slot.s2p`), often packaged with scikit‑rf. Docs mention how to load it.
  Docs: https://scikit-rf.readthedocs.io/en/v1.6.2/tutorials/Introduction.html
  Plotting tutorial (Smith): https://scikit-rf.readthedocs.io/en/latest/tutorials/Plotting.html

## 2) Passive components (tons of .s2p/.s1p)
- **Coilcraft** S‑parameters (inductors, transformers, chokes):
  https://cps.coilcraft.com/en-us/models/spice/
- **Murata** S‑parameters (MLCCs, RF inductors, ferrites):
  https://www.murata.com/en-us/tool/data/sparameterdata
- **KYOCERA AVX** RF/microwave S‑parameters:
  https://www.kyocera-avx.com/design-tools/rf-microwave-design-tools/
- **Würth Elektronik** (many parts expose direct .s2p links on product pages):
  https://www.we-online.com/en/support/design-tools/libraries

## 3) Filters, couplers, etc.
- **Mini‑Circuits** (open a product page → Downloads → S‑parameters):
  https://www.minicircuits.com/products/RF-Filters.html

## 4) Academic/Community repos (antennas, fixtures)
- **LWA Project** antenna impedance repo (.s1p and .s2p):
  https://github.com/lwa-project/Antenna_Impedance

## 5) Format references (for sanity)
- **Touchstone v2.0 spec (IBIS)**: https://ibis.org/touchstone_ver2.0/touchstone_ver2_0.pdf
- **Keysight Touchstone notes**: https://docs.keysight.com/display/genesys2010/Touchstone%2BFormat

> Tip: You only need **a handful per category** to reach 10–50 total files. For example, from
> a single Würth or Murata family page you can grab 10+ .s2p files quickly.
