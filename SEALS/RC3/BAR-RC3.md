# BAR-RC3 - coefficient route to the shear-hydro radius, done right, at NEW d (2048, 8192). Sealed 2026-11-03 15:50-15:59.
Why: BAR-RC2 FAILED as sealed (free-exponent fit biased ~1% by a crowded ladder of singularities; REFEREE-RC2). The referee's POST HOC
fixed-exponent fit at d = 512/1024 used existing coefficients, so it cannot be a test. RC3 uses d values with NO coefficients yet, the
RC2 seat's own (second) solver family, a fixed square-root exponent (beta = 1/2, as the primary fit), and a synthetic-ladder positive control.
Targets (DYN1 mono_2048.json / DYN1b RESULT.json track, on disk; never shown to the seat):
  d = 2048: c0 = -1.9154981851895594 + 0.42924741091280705i
  d = 8192: c0 = -1.94836923521368989578 + 0.26885790575211286270i
SPC (synthetic positive control, required): on synthetic series built from 2-4 conjugate square-root pairs with modulus ratios 1.02-1.10
  (seat's choice, known R), using the SAME n window and fit as for the real data, the beta = 1/2 fit recovers R to < 1e-3 relative and the
  angle to < 2e-3 rad. If SPC fails, the cells are VOID.
P1 (d = 2048), P2 (d = 8192; may be NOT RUN): with beta fixed at 1/2: HOLDS if |R - |c0||/|c0| < 2e-3 AND |theta - arg c0| < 5e-3.
  FAILED if |R - |c0||/|c0| > 5e-3. Otherwise INCONCLUSIVE. (Free-exponent fit reported, descriptive only.)
Scoring: verdict_RC3.py (hashed now) reads RC3/blind/RESULT.json {"SPC": {"max_rel_R_err","max_theta_err"}, "2048": {"R","theta"},
  "8192": {"R","theta"} or "NOT RUN"} (numbers as strings, full digits, no rounding to 2 digits).
