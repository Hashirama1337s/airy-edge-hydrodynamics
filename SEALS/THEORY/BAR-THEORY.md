# BAR-THEORY - the derived Airy law for the hydro critical point, scored against the blind DYN1b points (registered 2026-11-03 before
# the DYN1b finishing seat has delivered RESULT.json; theory seat never had access to DYN1b/ - stated in its report)
Predictions: PRED-THEORY.json (sha256 ab758de0..., written by the theory seat, which ran no solver above d = 4096).
Derived law: qfr^2_c + 2 = -4 T1 (2d)^(-1/3) + O(1/d), wfr_c - i = 2i T1 (2d)^(-1/3) + O(1/d), T1 = Ai'(U1)/Ai(U1), U1 = first complex zero of
Ai'^2 - U Ai^2; a2 = 0; (qfr^2+2) - 2i(wfr - i) = 4/d + O(d^(-4/3)); square-root branch point on the hydro sheet.
Items (verdict_THEORY.py, hashed now):
- T1 (parameter-free model A): at d = 8192, 16384, 32768, |blind - A| <= bar (q2 and w).
- T2 (model B = A + residual calibrated on DYN1 d <= 4096): same with B's bars.
- T3 (law): local exponent of |(qfr^2+2) + 4 T1 (2d)^(-1/3)| between 8192 and 32768 >= 0.85 (it should fall like 1/d).
- T4 (4/d identity): X d/4 with X = (qfr^2+2) - 2i(wfr - i) has |X d/4 - 1| decreasing from 8192 to 32768 and < 0.05 at 32768.
- T5 (branch point): blind monodromy at d = 8192 shows a radius-independent swap (on_sheet true).
POST HOC caveat: the theory seat saw DYN1 data (d <= 4096) and calibrated model B on it; model A uses no data (only g1 identities).
