# BAR-DYN1 - does hydrodynamics break down at the chaos point in infinite dimensions? (sealed 2026-11-03 before any d >= 256 is computed)

## In plain words
Grozdanov-Kovtun-Starinets-Tadic (1904.12862, l.1316, OPENED) state: "In general, the critical points and the pole-skipping points are
different." The council tracked the shear-channel hydro critical point (the one that sets the convergence radius of hydrodynamics) from
GKST's d = 4 value up to d = 192: it drifts toward the large-d point qfr^2 = -2, wfr = +i (thermal units; the n = 1 pole of the exact 1/d
correction g1 = sigma(psi(1+2 sigma)+gamma)). We predict, before computing d >= 256, that it converges there.

## Object
Critical point (double root of the dispersion relation, on the hydrodynamic sheet) of the shear channel of the planar AdS_{d+1}
Schwarzschild black brane, continued from GKST's d = 4 point (qfr^2, wfr) = (1.8906469 + 1.1711505i, 1.4436414 - 1.0692250i), in GKST's
thermal units (qfr = q/(2 pi T), wfr = omega/(2 pi T)).

## Predictions (scored by verdict_DYN1.py, hashed now, from DYN1/blind/RESULT.json)
- C1 control: the blind seat's d = 4 point matches GKST's to >= 7 digits.
- P1: at d = 256, 512, 1024, 2048, 4096 the tracked point stays on the hydro sheet (small-loop monodromy swaps the hydro pole) and is the
  nearest on-sheet critical point found in a census with |qfr^2| < 3.
- P2 (headline): fits of qfr^2_c(d) and wfr_c(d) on d in {512, 1024, 2048, 4096} with family A: L + a d^-1/3 + b d^-2/3 and family B:
  L + a d^-1/2 + b d^-1 (complex least squares, exact 4-point solve for 3 params via least squares) give limits within 0.05 of
  qfr^2 = -2 AND within 0.05 of wfr = i. FAILED if both families put the limit > 0.1 away (in either variable). VOID if the families'
  limits differ by > 0.1.
- P3: local exponent -dln|qfr^2_c + 2| / dln d between d = 2048 and 4096 lies in [0.28, 0.55]. (Second route via exact jets: descriptive.)
- P4: |qfr^2_c| < 2 at some computed d <= 2000 (i.e. at 256, 512 or 1024).
- N1 null: the council's off-sheet point c1 (tracked by the blind seat from its d = 8 location if the brief supplies it) does NOT approach
  (-2, i): its distance at d = 4096 > 0.3. (If the blind seat cannot track c1: N1 VOID.)
- Descriptive: a second on-sheet point near (-4, 2i) at d = 256; radius-vs-d curve; d = 3 control.
