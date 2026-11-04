# RESULT-R: three extra Cauchy circles (blind seat, same solver as RC3)

## Method
- Solver: qnm.py with the Bessel boundary (wronskian_b), M = 1024, quadratic predictor, secant root finding. Same as cauchy3.py.
- One difference from cauchy3.py: the new script (cauchy4.py) tracks the FULL loop, angle 0 to 2pi, without using the symmetry w(conj q2) = -conj w(q2). This lets closure be tested directly.
- c_n come from the 1024 full-loop values. They are compared with my existing rho = 1.92 coefficients (cauchy_d*_r192.json) for n = 1..150.
- n = 0 is left out of the relative measure because c_0 = w(0) = 0 exactly. |c_0(new)| is reported separately as an extra check.

## Results
| circle | loop closes? | Re w(-rho) | symmetry violation | max rel diff vs 1.92 (n=1..150) | |c_0| |
|---|---|---|---|---|---|
| d=8192, rho=1.96 (P1) | yes, |w(2pi)-w(0)| = 3.3e-16 | 1.2e-16 | 2.7e-15 | 4.02e-2 (at n=138) | 5.9e-9 |
| d=2048, rho=1.95 (Cin) | yes, 3.3e-16 | 1.1e-16 | 2.5e-15 | 1.92e-3 (at n=71) | 2.1e-10 |
| d=2048, rho=1.98 (Cout) | yes, 3.3e-16 | 1.2e-16 | 2.7e-15 | 6.46e+1 (at n=25) | 9.9e-4 |

There were no failed root solves on any loop.

## Reading
- **Closure is not decisive here.** All three loops close, including d=2048 at rho = 1.98, whose coefficients change completely: O(1) relative, and c_0 = 1e-3 instead of 0. So singularities lie between rho = 1.92 and 1.98, yet the full loop still closes.
  - This is what happens when the loop encloses a conjugate PAIR of square-root points that both swap the hydro mode with the same partner: the two swaps cancel.
  - Re w(-rho) ~ 0 does not detect this either, because the full loop is symmetric.
- **Cin (d=2048, rho=1.95) is aliasing, not a singularity inside.** Relative differences at n = 10, 50, 100, 150 are 1.7e-6, 1.6e-5, 7.9e-5, 5.2e-5. Aliasing from a square-root singularity at R = 1.96303 (my RC3 fit) predicts (rho/R)^M (n/(n+M))^1.5 = 1.0e-6, 1.1e-5, 2.9e-5, 5.0e-5. The max (1.9e-3 at n=71) sits where c_n passes near a zero of its oscillation. So the dominant singularity lies between 1.95 and 1.98.
- **P1 (d=8192, rho=1.96) is also aliasing.** The differences (1e-5 to 1e-3) track the aliasing prediction for R = 1.96673, within a factor of about 2. The exceptions are spikes where c_n is near a zero (n=40: 1.3e-2; n=138: 4.0e-2, the max).
  - There is no O(1) change. So nothing with appreciable weight lies inside |q2| < 1.96 at d=8192.
  - That argues against the weaker, closer pair near R ≈ 1.951 that appeared in 4 of 10 of my RC3 ladder fits: it looks like a fit artifact.
  - The dominant singularity lies just outside 1.96, consistent with my RC3 R = 1.9667.
- **Odd things:** (1) the rho = 1.98 loop closes despite enclosing singularities, as explained above; (2) the near-zero spikes inflate every max-relative figure. For these coefficients a median or envelope-relative measure would be more informative.

## Files
cauchy4.py, compareR.py, chainR.sh, cauchyfull_d8192_r196.json, cauchyfull_d2048_r195.json, cauchyfull_d2048_r198.json, compareR.json, logR_*.txt
