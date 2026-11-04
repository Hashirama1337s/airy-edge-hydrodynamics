# BAR-DYN2 - does the 1/d series stay exact for DYNAMICS? (sealed 2026-11-03 before any exact pole at d < 8 is computed)

## In plain words
The builder computed the shear-diffusion quasinormal pole of the AdS_{d+1} black brane as a 1/d series at fixed qbar (902 coefficients,
orders to 42), found it divergent (alternating, ~m!), and resummed it by diagonal Pade [21/21] in 1/d. Validated against an exact
solver at d = 8..32 (errors 1e-12 .. 1e-39, no tuned parameter). It ran NO solver at d < 8. Its predictions for d = 3..6 are copied here
(PRED-DYN.json, sha256 9e3744e4...), hashed now, before a blind seat computes the exact poles.

## Object
Shear-channel hydrodynamic (diffusive) quasinormal pole of the planar AdS_{d+1} Schwarzschild black brane, conventions of 2308.01371
(qbar = q/sqrt(d) with their normalisation; Omega = omega in their units), purely imaginary. d real. qbar in {0.5, 1.0, 1.5}.

## Predictions (scored by verdict_DYN2.py)
- P(qbar, d): |blind Im Omega - predicted Im Omega| <= 3 x bar, for all 17 (qbar, d) pairs in PRED-DYN.json EXCEPT (1.5, 3) (no claim:
  bar 3.1). HOLDS iff all 17. Per-point results reported.
- Headline H: at d = 4 all three qbar HOLD (d = 4 = N = 4 SYM plasma).
- Disclosures: the builder had read the Kovtun-Starinets d = 4, qbar = 1 value (Omega = -1.196132i, 6 digits, hep-th/0506184) before
  resumming (nothing fitted); bars were 10-700x loose at d >= 8; bar recipe fixed before any d < 8 output.
