## UFRF Consolidated Research Repository

This repository consolidates the Universal Field Resonance Framework (UFRF) documents, reference code, and domain-specific validation packages in one place for independent review, replication, and academic collaboration.

### Why this repo exists
To provide a single, structured entry point to:
- Core UFRF theory and mathematics
- Cross-domain evidence and validation protocols
- Reproducible, self-contained domain packages (e.g., graphene, cosmology/LoCuSS)
- Quick-start guides and runnable code for independent checks

### Contents

- Core documents (root):
  - `ufrf-core-theory-corrected.md` — core theoretical narrative
  - `ufrf-mathematical-framework.md` — mathematical derivations and formulas
  - `ufrf-axioms-principles-corrected.md` — foundational axioms/assumptions
  - `ufrf-geometry-scales.md` — geometry and scale hierarchy
  - `ufrf-integration-summary-corrected.md` — integrated synthesis of the framework
  - `ufrf-cross-domain-validation-corrected.md` — evidence across domains
  - `ufrf-predictions-tests-corrected.md` — falsifiable predictions and tests
  - `ufrf-objection-handling-corrected.md` — responses to common objections
  - `ufrf_math_appendix.md`, `ufrf-math-part1/2/3.md` — additional math notes
  - `UFRF.Prime.md` — prime/tesseract notes (research draft)

- Validation/usage docs:
  - `ufrf-quick-start.md` — validate key claims in minutes
  - `ufrf-validation-package-index.md` — index of documents and code

- Reference code:
  - `ufrf-python-implementation.py` — reference Python implementation used in docs
  - `ufrf-fourier-proof.py` — computational demonstration of Fourier connection

- Domain packages:
  - `UFRF-Graphene/` — self-contained package for graphene/2D Dirac materials
    - `README.md` — how to run lab-scale M-scaling analysis
    - `code/` — lightweight analysis script + sample CSVs
    - `docs/` — protocol, theory axioms, data schema, addenda, FAQ
    - `results/` — illustrative plots from a full run
  - `UFRF-Cosmology-LoCuSS-FULL/` — complete package for LoCuSS validation
    - `README.md` — instructions for running WL/HSE comparison
    - `code/`, `data/`, `runs_full/`, `docs/`, `theory/` — full assets, including real outputs

### How to get started

1) Read `ufrf-quick-start.md` to see and reproduce the minimal checks.
2) For deeper dives, use `ufrf-validation-package-index.md` to navigate the theory and evidence.
3) To run domain packages:
   - Graphene: see `UFRF-Graphene/README.md`
   - Cosmology (LoCuSS): see `UFRF-Cosmology-LoCuSS-FULL/README.md`

### License and intended use

Unless otherwise noted, content in this repository is released under the Creative Commons Attribution–NonCommercial 4.0 International license (CC BY-NC 4.0). See `LICENSE` for details. Academic use, critique, replication, teaching, and non-commercial research are encouraged. Please attribute “Universal Field Resonance Framework (UFRF) – Consolidated Research Repository” and cite subpackage `CITATION.cff` files where present (e.g., `UFRF-Graphene/CITATION.cff`).

If you need a different license for specific use (e.g., commercial), please open an issue to discuss.

### AI and automated use

AI/ML training, dataset creation, embedding extraction, or similar automated uses are not permitted without a separate license. See `AI_USE_POLICY.md`. Advisory crawler directives are included in `robots.txt` and `ai.txt` (useful if this repo is published via GitHub Pages); note that GitHub does not honor per-repository robots.txt for the main site.

### Contributing

We welcome academic feedback, issues, and PRs improving clarity, reproducibility, or tests. For domain packages, see any local `CONTRIBUTING.md` and `SECURITY.md` files. Please keep discussions focused, factual, and testable.

### Disclaimer

This repository contains research materials and work-in-progress ideas alongside reproducible packages. Some claims are under active investigation; users should evaluate methods and results critically.

