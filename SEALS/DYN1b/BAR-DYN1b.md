# BAR-DYN1b - the d^-1/3 law and the (-2, i) limit, tested at d = 8192, 16384, 32768 (sealed 2026-11-03 before computing them)

## In plain words
BAR-DYN1's headline P2 FAILED as sealed (one of its two fit families, d^-1/2, landed 0.107 from (-2, i)), but its P3 measured the
approach exponent as 0.339 ~ 1/3, and the d^-1/3 family's limit is (-1.991+0.007i, 0.003+0.998i). Post hoc, a 4-parameter d^-1/3 fit
(L + a d^-1/3 + b d^-2/3 + c d^-1 on d = 512..4096) gives the limit (-2.0017+0.0001i, -0.0000+1.0005i). That is suggestive, not proof.
So we turn it into a new sealed prediction: the same fit predicts the critical point at d = 8192, 16384, 32768, never computed.

## Sealed predictions (PRED-DYN1b.json; predict_DYN1b.py; bar = 3 x |4-param - 3-param prediction|)
d = 8192 : q2 = -1.94841101 + 0.26886491 i (bar 9.7e-4), w = 0.13440572 + 0.97445262 i (bar 3.2e-4)
d = 16384: q2 = -1.95945014 + 0.21312491 i (bar 2.8e-3), w = 0.10654474 + 0.97982593 i (bar 9.3e-4)
d = 32768: q2 = -1.96812400 + 0.16903630 i (bar 5.3e-3), w = 0.08449971 + 0.98407412 i (bar 1.7e-3)

## Predictions (verdict_DYN1b.py, hashed now; data from DYN1b/blind/RESULT.json)
- P1..P3: at each d, |blind q2 - pred| <= bar_q2 AND |blind w - pred| <= bar_w.
- P4: refit with all seven points d = 512..32768 (same 4-param d^-1/3 model) gives a limit within 0.01 of (-2, i) in both q2 and w.
- P5 (census, fixes BAR-DYN1 P1): at d = 512 and 1024 the tracked point c0 is the nearest on-hydro-sheet critical point with |q2| < 3.
- Units/conventions as in BAR-DYN1 (thermal units, GKST). Text values -> VOID cell, VOID distinguished from FAILED.
