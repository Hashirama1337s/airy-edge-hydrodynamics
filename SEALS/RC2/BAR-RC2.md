# BAR-RC2 - independent route to the shear-hydro radius: Darboux analysis of the hydro series COEFFICIENTS. Sealed 2026-11-03 13:50-13:59.
Why: BAR-RC (monodromy census, same solver family as DYN1b) says the radius of convergence of the shear hydro series in q2 is |c0| at
d = 512, 1024. A blind seat with a different solver computes the Taylor coefficients of the hydro pole wfr(q2) = sum c_n q2^n and reads
the radius, angle and singularity type from their large-n behaviour (no monodromy, no c0 seeding). Units: GKST thermal (qfr = q/(2 pi T)).
Targets (DYN1b/blind, on disk before this seal; blind seat never sees them):
  d = 512 : c0 = -1.854341963762 + 0.691670108026i, |c0| = 1.979139120, arg c0 = atan2(0.691670108026, -1.854341963762)
  d = 1024: c0 = -1.8901721196114076 + 0.5439416103393121i, |c0| = 1.9668815717309482
PC (positive control): the seat's d = 4 radius reproduces GKST 1904.12862's published shear-channel critical point modulus |qfr2_*|
   (value as opened by the seat, quoted with locator) to 3 significant digits. If PC fails, all cells VOID.
P1 (d = 512) and P2 (d = 1024): HOLDS if |R - |c0||/|c0| < 2e-3 AND |theta - arg c0| < 5e-3 rad (theta = seat's dominant-singularity angle,
   upper half plane) AND the seat's singularity exponent beta (c_n ~ n^(-1-beta) R^-n, branch type) satisfies |beta - 1/2| < 0.1.
   FAILED if |R - |c0||/|c0| > 1e-2 (radius set by something else). Otherwise INCONCLUSIVE. Seat's own error bars reported, not used.
Scoring: verdict_RC2.py (hashed with this BAR) reads RC2/blind/RESULT.json keys {"PC": {"absq2_star_ours","absq2_star_GKST","locator"},
 "512": {"R","theta","beta"}, "1024": {...}} (strings).
