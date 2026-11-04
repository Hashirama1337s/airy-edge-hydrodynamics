# RC2 blind seat: shear hydrodynamic QNM of planar AdS_{d+1} Schwarzschild, d = 4, 512, 1024

## Brief hygiene / independence
- The brief gives the object's leading behaviour (w -> -i D q^2). That defines the object; it gives no target numbers. I did not assume a value for D. c1 = -1/2 came out of the solver.
- My auto-loaded memory index (injected into context, not opened by me) has a one-line note: "large-D series resums to exact AdS screening masses". It contains no RC2 numbers. I opened no forbidden path.
- The GKST paper was opened only for the positive control, after my d=4 solver existed. I fitted forms freely; beta was never fixed.

## Equation (derived, not transcribed)
- Background: ds^2 = r^2(-f dt^2 + dx^2) + dr^2/(r^2 f), with f = 1 - (r0/r)^d, L = 1, T = d r0/(4 pi).
- Shear perturbation: h_xt = r^2 A_t(r) e^{-i w t + i q z} and h_xz = r^2 A_z(r) e^{...}, in the gauge h_xr = 0.
- These do not depend on x. Kaluza-Klein reduction along x (G_xx = phi^2 = r^2) makes A_a = h^x_a a Maxwell field. Its coupling is sqrt(-g_d) phi^3 = r^{d+1} =: N.
- The equations are d_a(N F^{ab}) = 0. Define the radial "momentum" P = N A_t' / (g_tt g_rr) = r^{d+1} A_t'. The t-equation and the r-constraint then give
  (f r^{3-d} P')' = (q^2 f - w^2) P / (r^{d+1} f).
- The gauge invariant Z = q A_t + w A_z satisfies Z proportional to f r^{3-d} P'.
- With u = (r0/r)^d and thermal units (2 pi T = d r0/2) this becomes the master equation:

  d/du[ (1-u) u^{2-2/d} dP/du ] = [ q2/4 - w^2 / (4(1-u)) ] P,   q2 = (q/2piT)^2,  w = omega/(2piT).

  Note that d enters only through the exponent 2 - 2/d.
- Boundary conditions:
  - Horizon: ingoing, P ~ (1-u)^{-i w/2}.
  - Boundary: the two branches are P -> const and P ~ u^{2/d - 1} (that is, r^{d-2}). Z(boundary) is proportional to Q(0) = [(1-u) u^{2-2/d} P_u](0), which vanishes iff the r^{d-2} branch is absent. So a QNM is the ingoing solution that is regular at the boundary.
- Boundary series in z = r0/r, used for the regular solution:
  m(m+d-2) a_m = (m-d)(2m+d-4) a_{m-d} - (m-2d)(m-2) a_{m-2d} + (q^2-w^2) a_{m-2} - q^2 a_{m-d-2}, with q^2 = (d^2/4) q2.
- Validation of the derivation: the positive controls below, and the d=4 critical point, which GKST computed with a different master equation (Kovtun-Starinets Z1, their eq. 4.18).

## Solver (own code: qnm.py)
- Horizon Frobenius series in x = 1-u, 70 terms, evaluated at x0 = 0.5.
- DOP853 (rtol 1e-13) in y = -ln u for the pair (P, S), where S = Q e^{(1-2/d)y}. This scaling avoids overflow.
- Regular boundary solution: the z-series is summed in mpmath (40 digits) only at small z0, where term cancellation is below about e^4. It is then integrated outward to y_m = 60.
- Root condition: the Wronskian P_in S_reg - S_in P_reg = 0, solved by secant iteration.
- A bug I caught: at large d, summing the z-series directly near z ~ 1 cancels by 1e40 to 1e99 (the regular solution is exponentially small there). My first version gave noise there. The fixed version matches a 200-digit direct sum to 1e-12.
- Taylor coefficients: Cauchy FFT of w on circles |q2| = rho with M = 256 points. I used the exact symmetry w(conj q2) = -conj w(q2), which holds because c_n is i times a real number. Checks: Re w(-rho) ~ 1e-16 on every circle, and max |Re c_n| ~ 1e-18.
- Direct critical points: Newton on {W = 0, dW/dw = 0} (crit.py).

## Positive controls
- c1 = -0.5000000000000 for d = 4, 512 and 1024. This is D = 1/(4 pi T), the universal eta/s result.
- d=4: c2 = -0.07671320486001, against -(1-ln2)/4 = -0.07671320486001. They agree to 1e-14.
- GKST arXiv:1904.12862, sec. 4.2, eq. (4.20), p. 24: q_c^2 ~ 1.8906469 +/- 1.1711505 i, w_c ~ +/-1.4436414 - 1.0692250 i, |q_c| ~ 1.49131. The text on p. 25 says "|q^2_c| ~ 2.224".
  - My direct critical-point solve gives q2_c = 1.8906468612 + 1.1711505237 i and w_c = 1.4436414084 - 1.0692249776 i. Every printed GKST digit is reproduced.
  - My Darboux fit of my own d=4 coefficients gives |q2_*| = 2.22399. GKST's printed components give 2.223991.

## Convergence evidence
- d=4: two radii (rho = 1.8 and 2.0) agree: c_n relative difference is 6e-9 at n=60. Two tolerances (rtol 1e-13 vs 1e-11) give fitted R and theta equal to 1e-6. Varying y_m, x0 and the series cut changes w by at most 1e-14.
- d=512: two radii (rho = 1.75 and 1.85) agree: c_n relative difference is 1e-9 for n <= 50 and 1e-6 at n ~ 110. The solver is stable under rtol, dps, y_m and z0 changes at the 1e-12 level.
- d=1024: two radii (rho = 1.6 and 1.75) agree: c_n relative difference is 5e-9 at n=50 and 7e-7 at n=70. Above n ~ 80 the rho = 1.6 set is noise-limited, so fits use rho = 1.75 up to n = 110.

## Results (digits I trust)
| d | R | theta | beta | window | spread over other windows |
|---|---|---|---|---|---|
| 4 | 2.22399 (5-6 sig) | 0.554594 (6) | 0.500 (3) | 40-120, rho = 2.0 | R 2.6e-5, theta 5e-6, beta 3.5e-3 |
| 512 | 2.00 (2-3 sig, +/- 0.03) | 2.78 (+/- 0.02) | NOT DETERMINED | 20-90 | R 1.94-2.03, theta 2.756-2.791, beta -1.8 to +4.0 |
| 1024 | 2.0 (+/- 0.05) | 2.85 (+/- 0.03) | NOT DETERMINED | 20-90, rho = 1.75 | R 1.93-2.08, theta 2.82-2.88, beta -5.2 to 0 |

- d=4: the dominant singularity is a square-root branch point (beta = 1/2 within 0.002). It is the QNM level crossing at the GKST point.
- d=512 and d=1024: the c_n alternate in sign with a slow beat, so the dominant singularities form a conjugate pair near the negative real axis with |q2| ~ 2.0.
  - A single conjugate-pair Darboux form does not fit stably (rms ~ 1e-4 to 1e-3, versus 1e-9 at d=4). Beta swings with the window, so I do not report a beta.
  - Directly solved level crossings for d=512 are at q2 = -2.0066977 + 0.5340388 i (|.| = 2.07654, arg 2.88149) and at -2.0270884 + 0.7917469 i (|.| = 2.17622). Both lie just left of Re q2 = -2, and neither sits at the coefficient-asymptotic location (~2.00 at arg ~2.78).
  - Tracking along a half-circle at rho = 1.96 shows no monodromy, consistent with R > 1.96.
  - I read this as several singularities clustered near |q2| ~ 2 (Pade also shows a chain of poles there), not as one isolated square root. The level crossing at 2.07654 is reported as an unverified R2 candidate.

## Surprise (an analytic side observation; derivation only, not a claim)
- At d = infinity my master equation is Fuchsian with three singular points and solves in 2F1.
- The ingoing, boundary-regular condition then gives exactly w = -i q2/2, but only where Re q2 > -2. That is where the boundary exponent branch s_+ = -1/2 + (1/2) sqrt(1 + q2 - w^2) stays principal.
- So in thermal units the large-d hydro mode tends to -i q2/2 (c_n -> 0 for n >= 2; observed c2 ~ -0.41/d). Its singularities should pile up near the line Re q2 = -2, which suggests R -> 2 and theta -> pi as d -> infinity.
- The measured d=512 and d=1024 values (R ~ 2.0, theta rising from 2.78 to 2.85) fit that picture. This would explain why a single isolated branch point does not describe the large-d coefficients.

## Files
- qnm.py (solver), cauchy.py, crit.py, darboux.py, anfull.py, angrid.py, pade.py, halfcircle.py, ray.py
- cauchy_*.json (w on circles and the c_n), crit_d4.json, crit_d512.json, crit_d512c.json, log_*.txt
