# BAR-RC3R - repair test for RC3 P2 (d = 8192): is there ANY singularity in 1.92 < |q2| < 1.96? Sealed 2026-11-04 before the run.
Why: REFEREE-PUB-1 / ERRATA-DYN 21 - the d = 8192 ladder fits put pairs at |q2| = 1.951, 1.964 (inside |c0| = 1.96683), which the monodromy census
excludes for branch points but not for poles. Cauchy coefficients are independent of the circle radius rho as long as no singularity lies between
the radii; a pole or branch point between them changes the coefficients by ~ (rho/R)^n.
Method: the RC3 blind seat's own solver (qnm.py, Bessel matching), M = 1024 points, same tracking.
P1 (d = 8192): c_n from rho = 1.960 vs rho = 1.92 (existing cauchy_d8192_r192.json), n = 0..150: HOLDS if max relative difference < 1e-6 AND the
   rho = 1.96 loop closes (Re w(-rho) ~ 0, end = start). FAILED if max rel diff > 1e-4 or the loop does not close. Between: INCONCLUSIVE.
C_in (control, d = 2048, |c0| = 1.9630): rho = 1.92 vs 1.95 -> must agree < 1e-6.
C_out (positive control, d = 2048): rho = 1.92 vs 1.98 (beyond c0) -> must DISAGREE (max rel diff > 1e-3) OR the 1.98 loop must fail to close.
If either control fails, P1 is VOID.
Scored by verdict_RC3R.py (hashed now) from blind/RESULT-R.json keys (strings): P1_maxrel, P1_closes ("true"/"false"), Cin_maxrel,
Cout_maxrel, Cout_closes.
