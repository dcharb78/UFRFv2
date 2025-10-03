# FAQ

**Q: How do I choose `d_M`?**  
A: For η/s, start with `d_M ≈ +1`. For observables dominated by screening (e.g., α_eff), a negative `d_M`
may be appropriate. You can fit `d_M` jointly by comparing multiple techniques if needed.

**Q: What if I don’t have ratios?**  
A: You can skip the ratios CSV; the core analysis still runs.

**Q: Can α be >1?**  
A: α is defined in [0,1] for M-scaling. If your slope implies α>1, revisit S construction and knob ranges;
consider that d_M may differ from +1 for your observable.

**Q: How do I mitigate device-to-device variation?**  
A: Use device fixed effects (already in the pooled model) and replicate across devices. Cleanliness and encapsulation
should reduce intercept spread but shouldn’t change slopes for a given technique.
