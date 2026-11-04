# RC3 blind seat: shear hydro mode at d = 2048 and d = 8192

## Brief hygiene
- This brief hands me the singularity exponent (beta = 1/2) and the model form (a ladder of square-root pairs). I used them because the brief asks for them. As requested, I also give a free-exponent single-pair fit, for description only.
- I opened only my own RC2/blind files and this folder. I took the referee's warning on board and did not use crit.py at large d.

## Method
- **Object and units:** same object and units as RC2: w(q2) in thermal units, Taylor coefficients c_n = i r_n.
- **Solver:** my RC2 solver (qnm.py), with one change. At the matching point y = -ln u = 60, u = e^-60 is negligible, so the regular boundary solution is exactly the pure-AdS Bessel function:
  - P = (kz)^-nu I_nu(kz), with nu = (d-2)/2 and k^2 = (d^2/4)(q2 - w^2).
  - It enters only through the branch-safe ratio x I_{nu+1}(x)/I_nu(x), evaluated by mpmath.
  - It matches my RC2 outward-integrated regular solution to about 1e-15 at d=512 and d=2048.
  - The d=512 mode at q2 = 0.1 is unchanged to 1e-16.
  - It is 10-50 times faster, which made d=8192 feasible.
- **Coefficients:** Cauchy FFT with M = 1024 points on two circles, rho = 1.85 and 1.92.
  - Coefficient growth (three-term recurrence) put the singularity at about 1.98 (d=2048) and 1.99 (d=8192), so these radii are 0.93 and 0.97 of R. Taking the fitted R ≈ 1.963–1.967 instead, they are 0.94 and 0.98 of R.
  - Aliasing is about (rho/R)^1024 < 1e-8.
  - The mode was tracked along the circle with a quadratic predictor; no secant failures.
  - Closure checks: Re w(-rho) ~ 1e-16 on all four circles.
- **Fit:** beta fixed at 1/2. The model is r_n = sum over K pairs of Re[zeta_k^-n (C_k [x^n](1-x)^{1/2} + D_k [x^n](1-x)^{3/2})].
  - Amplitudes are fitted by linear least squares (variable projection); positions (R_k, theta_k) by nonlinear least squares, 24 random starts per K.
  - K grows from 1 to 4, and K+1 is accepted only if the rms drops by more than 3 times.
  - The reported R and theta belong to the pair that contributes most at the window end n2.

## Synthetic positive control (done first, same window 30-200 and same code)
- Six synthetic series with 2, 2, 3, 3, 4 and 4 conjugate square-root pairs. Modulus ratios were 1.02-1.10, R1 = 1.97, theta1 = 2.92, plus (1-x)^{3/2} corrections and noise matching the Cauchy noise model.
- The ladder picked the true K in all 6 cases.
- Max relative R error is 6.5e-6 and max theta error is 8.2e-6 (spc_30_200.json).

## Convergence
- d=2048: the two radii agree, c_n relative difference 4.8e-12 (n=50), 1.6e-7 (n=200), 4.8e-6 (n=250).
- d=8192: the two radii agree, 4.8e-11 (n=50), 5.2e-8 (n=200), 2.6e-4 (n=250).
- So windows up to n = 200-220 are clean.

## Results (full digits; the spread says what is trustworthy)
- **d = 2048:** R = 1.9630256953, theta = 2.9211396480 (window 30-200, rho = 1.92, K = 4).
  - Over 5 windows and 2 radii, R spans 1.9629588 to 1.9630443 and theta spans 2.9210883 to 2.9211510. About 4 digits of R and theta are solid.
  - In 3 of 10 fits an extra weak pair appears at smaller R (1.904-1.959). It lands somewhere different each time, so I treat it as a fit artifact.
- **d = 8192:** R = 1.9667280547, theta = 3.0043821896 (window 30-200, rho = 1.92, K = 4).
  - Over the 10 fits, R spans 1.96438 to 1.96711 and theta spans 2.99794 to 3.00460. 8 of 10 fits sit within [1.96672, 1.96711] and [3.00429, 3.00460].
  - In 4 of 10 fits a weaker, closer pair appears near R ≈ 1.949-1.952, theta ≈ 2.96-2.98 (contribution at n2 of 0.07-0.43). Whether it is real is unresolved, so R at d=8192 carries an unresolved downside of about 0.015.
- **Free-exponent single-pair fits (description only):**
  - d=2048: R_free = 1.99443, beta_free = -1.797, with ranges R 1.976-2.002 and beta -2.32 to -0.99.
  - d=8192: R_free = 1.97944, beta_free = -0.997, with ranges R 1.978-1.999 and beta -2.63 to -0.99.
  - A single pair with free beta does not describe the data: residuals are 1e4 to 1e7 times worse than the ladder fit at the same window.

## Surprises / caveats
- **The data are richer than the model.** The real-data spread across windows (1e-4 at d=2048, up to 3e-3 at d=8192) is much larger than the synthetic-control error (6e-6). K = 4, the largest allowed, was selected almost everywhere, and the residual was still falling. The structure seems to be a dense cluster of singularities.
- **Trend with d:** theta rises toward pi (2.78 at d=512, 2.85 at d=1024, 2.921 at d=2048, 3.004 at d=8192). R stays near 1.96-2.0. This is consistent with my RC2 analytic observation that at d = infinity the hydro mode is exactly -i q2/2 for Re q2 > -2, with singularities collecting at Re q2 ≈ -2.
- Note: the RC2 d=512/1024 values came from single-pair fits and are not directly comparable to these ladder values.
- c2·d = -0.4109 (d=2048) and -0.4112 (d=8192): a smooth large-d limit.

## Files
- qnm.py (adds boundary_bessel and wronskian_b), cauchy3.py, ladder.py, spc.py, fitdata2.py, darboux.py, anfull.py
- cauchy_d2048_r185/r192.json, cauchy_d8192_r185/r192.json (circles and c_n), cauchy_*_s16.json (surveys)
- fits_2048.json, fits_8192.json, spc_30_200.json, log_*.txt
