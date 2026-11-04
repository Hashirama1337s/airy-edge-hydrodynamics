# DYN1 blind seat: shear-channel critical points of the AdS_{d+1} black brane, d = 4 to 4096

## Disclosures (read first)
- **Hints in the brief.** The brief gave c1's d=4 location (qfr^2 ~ -2.37737, wfr ~ -1.64659 i) and suggested the variable x = r^d.
  I used the c1 numbers only as a Newton seed. My converged d=4 value is -2.3773683702, -1.6465852010 i, which matches the
  published 6-digit value.
- **Numbers I saw before computing.** The allowed council script track.py contains the d=4 seed 1.8906469+1.1711505i /
  1.4436414-1.0692250i. These are the published GKST numbers. I used them as the d=4 Newton seed and as the control target.
- **Sources opened.** I read the GKST values from the arXiv TeX source of 1904.12862 that sits in the allowed
  shearB/src1904/ folder (GKST_ComplexLife_V3.tex, l.803-811, eq. (eq:qw-crit-shear-x); hydro series eq. (mkm) l.741-745).
  I also read the allowed method files: shear/R-SHEAR.md, shearB/qnm.py, shearB/RESULT.md, council crit.py, track.py and mono.py.
- **Forbidden paths.** I did not open COUNCIL-DYN.md, GLANCE-DATA.txt, mono.out, the SEAL/BAR/verdict files, anything in DYN1/
  outside blind/, or memory.

## Method
My formulation differs from the council's, which uses the conjugate field Pi, Chebyshev collocation in z = 1/r and a secant
on (w_a - w_b)^2.
1. **Field and equation.** Kaluza-Klein reduce h_{mu y} = r^2 A_mu to get a Maxwell field with coupling r^{d+1}. The
   gauge-invariant field E = q A_t + omega A_x (Kovtun-Starinets) then obeys
   d/dr[ r^{d+1} f E'/(omega^2 - q^2 f) ] + r^{d-3} E/f = 0, with Dirichlet E = 0 at the boundary and ingoing behaviour at the horizon.
2. **Rescaling.** With x = r^d, w = omega/d and sig = q^2/d^2 (so wfr = 2w, qfr^2 = 4 sig), every explicit d cancels
   except x^{-2/d}:
   d/dx[ x(x-1)E_x/(w^2 - sig + sig/x) ] + x^{1-2/d} E/(x-1) = 0.
3. **Solving the ODE.** I integrate in L = ln x with high-order Taylor stepping. Path: start from a Frobenius series at
   the horizon (exponent -iw), then follow a complex path around the apparent singular point.
4. **Far-zone matching.** For L >> 1, f = 1 and the far zone is solved exactly by z^{d/2} J_{d/2}(kz), with z = e^{-L/d}
   and k^2 = d^2 (w^2 - sig). I match to the normalisable Bessel branch at L_m ~ (digits) ln 10. The Bessel ratio comes
   from a backward recurrence. I multiply through by prod (2n - R_n)/2n, which is J_nu up to a non-vanishing factor. This
   removes spurious poles at the zeros of J_{d/2}; those poles crowd the real-alpha region where c1 lives at large d.
5. **Normalisation.** I normalise the horizon series by (1 - 2iw). This removes the resonance pole at wfr = -i, which c1
   crosses near d ~ 6.6.
6. **Critical points.** The spectral function F(w, sig) carries jets in w, which give F, F_w and F_ww. Critical points
   come from 2D Newton on F = F_w = 0; the Jacobian sig-column is a finite difference.
7. **Continuation in d.** Steps of 1/8 octave (c0) and 1/8 to 1/6 octave (c1), linear predictor in ln d, automatic
   halving. Max predictor-corrector jump 0.013 (c0). Both tracks land exactly on the powers of 2. Double precision was used
   for c0 up to 4096. For c1 I switched to 64, 80 and 112-bit arithmetic as w -> 0 (see Surprises). Each target d was then
   re-converged at two precisions.

## Controls (all passed)
- **GKST shear critical point, d=4.** Mine: qfr^2 = 1.890646861152505677502981003 + 1.171150523650781022093714966 i,
  wfr = 1.443641408408432121742481592 - 1.069224977597582841300126392 i.
  Published: 1.8906469 + 1.1711505 i, 1.4436414 - 1.0692250 i. All 8 published digits agree.
- **GKST c1, d=4.** -2.3773683702 and -1.6465852010 i, against the published -2.37737 and -1.64659 i.
- **d=4 hydro mode at qfr^2 = 0.1.** wfr = -0.05078481 i. The 4-term series eq. (mkm) gives -0.0507848 i.
- **Large d.** d i (w + i sig) at sig = 0.05 approaches g1 = sig(psi(1+2sig) + gamma) = 0.0076730 (form from shearB/2308.01371),
  with residual times d constant at -0.00581 for d = 256, 1024 and 4096.

## Convergence
- **c0 (and d=4).** Run A: 110 bits, step ratio 1/4, L_m = 84.8. Run B: 150 bits, step ratio 1/5, h_max = 0.8, L_m = 130.
  They differ by at most 6e-32 at every d. I report 28 significant digits.
- **c1.** Run C: 128 bits. Run D: 176 bits, different steps and L_m. q2 agrees to at least 25 digits and wfr to at least
  19 digits relative to |wfr|. I report 18 digits. Im q2 and Re wfr are zero by symmetry (computed values ~1e-26).
- **Double vs multiprecision.** The double-precision track agrees with the multiprecision values to ~1e-15 (c0).

## Results (raw, no fitting)
| d | c0 qfr^2 | c0 wfr | c1 qfr^2 | c1 wfr |
|---|---|---|---|---|
| 256 | -1.800300430324 + 0.884099830801 i | 0.440539728532 + 0.909870610149 i | -1.147526419161 | -0.019729534978 i |
| 512 | -1.854341963762 + 0.691670108026 i | 0.345107796293 + 0.931754908334 i | -1.092093161569 | -0.009781229185 i |
| 1024 | -1.890172119611 + 0.543941610339 i | 0.271645842232 + 0.947278330772 i | -1.057725896782 | -0.004864643694 i |
| 2048 | -1.915498185190 + 0.429247410913 i | 0.214484293258 + 0.958809912731 i | -1.036280589207 | -0.002424091236 i |
| 4096 | -1.934189199125 + 0.339483137435 i | 0.169683206976 + 0.967612635741 i | -1.022839081010 | -0.001209417454 i |
(Full digits are in RESULT.json. Mirror points (conj q2, -conj w) exist for c0.)

- **on_sheet.** I continued the hydro root radially from qfr^2 = 0.05 to a loop of radius 0.02 around each point, then
  went once around the loop in 160 steps.
  - c0: the hydro root does not come back at any of the five d. Closures are 9.6e-3, 6.8e-3, 4.8e-3, 3.4e-3 and 2.4e-3,
    against numerical noise of ~1e-15. They fall smoothly as d^-1/2, which fits a single square-root branch point.
  - At d = 256 the end value equals the separately converged partner root to 4e-16; at 512, to 6e-5. At 1024-4096 the
    partner-finder converged to a third, crowded root, so there on_sheet rests on the closure alone.
  - c1: not on the hydro sheet at any d. The closure is ~1e-15 (trivial), and the radially continued hydro root at the
    loop is about 0.5-0.58 away in wfr.
- **Census / nearest.**
  - d=256, full census: hydro root on 37 rays (plus mirror) out to |q2| = 3.2. Seeds came from the quadratic partner
    estimate, then 2D Newton.
  - It found 24 distinct critical points with |q2| < 3, all with |q2| >= 2.00567. The tracked point is the smallest.
  - c1 is closer (|q2| = 1.148) but is not on the sheet. So nearest_in_census = true at d=256.
  - d = 512-4096: no census was run within the time budget. nearest_in_census = null there. Only the loop tests above
    were done, and they show that c1, the one known closer point, is not on the sheet.

## Surprises
1. **c0 heads towards (qfr^2, wfr) = (-2, i).** In my variables that is alpha = w^2 - sig -> 1/4, where the two far-zone
   exponents (-1 +- sqrt(1-4 alpha))/2 merge. The point d=infinity hydro w = -i sig also passes through it. |q2| has a
   shallow minimum near d ~ 2048 (2.0057, 1.9791, 1.9669, 1.9630, 1.9638).
2. **A ladder of critical points at large d.** At d=256 the census shows a dense ladder at Re q2 ~ -1.80 to -1.87, with
   Im q2 = 0.88, 1.13, 1.31, 1.46, ... c0 is its lowest rung. At d=256 all 10 loop-tested points (the lowest 5 rungs and their mirrors, |q2| up to 2.45) show non-trivial closure
   (~1.2e-2, r = 0.03, coarse 72-step loop), so several rungs appear to touch the hydro sheet. Only the lowest rung matters
   for the radius.
3. **c1 drifts in d.** qfr^2 -> about -1.02 and wfr -> 0, roughly 5/d. Its |q2| drops below c0's from d ~ 6.3 on, but it
   never involves the hydro pole. The double-precision noise for c1 grows roughly like |w|^-4.5, so 112-176 bits were needed.
4. **Two numerical traps worth knowing.** (a) The ingoing normalisation has a pole at wfr = -i, which c1 crosses near
   d ~ 6.6; fixed with the (1-2iw) factor. (b) Naive matching to the J_{d/2} branch adds poles at the J zeros, which are
   dense near real alpha ~ 0.27-0.3 at large d; fixed by the J-product factor.
5. **Process.** I restarted c1 tracking several times as precision needs grew. The earlier partial logs are kept
   (track_c1_part*.log). The duplicates in track_c1.jsonl come from aborted runs; the refinements use the last entry at
   each exact d.

Files: qnmx.py (solver), lib.py (Newton), track.py, refine.py, census.py, mono_run.py, final.py; data in track_*.jsonl,
refine_*.jsonl, census_256.json, mono_*.json; RESULT.json.
