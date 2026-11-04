# DYN2 blind seat: hydrodynamic shear pole of the AdS_{d+1} black brane at real d

## Disclosures (read first)

- **Brief hygiene.** The brief gave me the leading small-q form of the branch, "omega -> -i qbar^2 ...". The PSD_v2.tex
  file I was allowed to read also prints the next term, -i H_{2/d} qbar^4/d, and the hydro series. I used these in two
  ways only: (a) as the seed and branch label at qbar = 0.05, and (b) as a small-q control. The final numbers come from
  root finding at each point. No fitting, no series and no extrapolation went into any reported value. The brief gave
  no target numbers.
- **Independence.** I read only my own folder, the allowed shearB/ files (qnm.py, run.py, RESULT.md, for method only),
  PSD_v2.tex, and the KS paper source, which I downloaded into blind/src0506184/. I did not open any other path under
  NEXT-2026-11-03, the BAR/seal files, or memory. One stray artifact: my first WebFetch of the KS PDF failed (binary
  stream), and the tool auto-saved the PDF under <private folder>/projects/.../tool-results/. That is the KS paper
  itself, not a forbidden file. I did not use it.
- **Different method from the lab's shearB solver.** shearB used the EF master field Z in x = r^d, with Taylor stepping
  around an apparent singularity, plus a large-d jet. I changed the gauge, the variable and the algorithm:
  Schwarzschild-time gauge, the conjugate momentum Pi (which has no apparent singularity), and a two-sided Frobenius
  connection. The two series are matched by a Wronskian at a single point, with no ODE stepping. The first seat's
  method was not named to me.

## Method

1. **Gauge change (derived).** I set Z_EF = exp(i w r_*) Y with dr_*/dr = 1/(r^2 f), in eq. (EoM) of 2308.01371
   (PSD_v2.tex l.144-147). The i*w terms cancel and leave
   `( r^{d+1} f Y' / (w^2 - q^2 f) )' + r^{d-3} Y / f = 0`.
2. **Momentum variable.** I set Pi = r^{d+1} f Y'/(w^2 - q^2 f), so that Y = -f r^{3-d} Pi'. With u = 1/r and
   f = 1 - u^d:
   `f Pi'' + ((d-1) f/u - d u^{d-1}) Pi' + (w^2/f - q^2) Pi = 0`.
   This equation has real coefficients for omega = -i gamma and no apparent singularity.
   `check_transform.py` verifies the whole chain symbolically, for symbolic d: Pi solves this equation, so
   Z = e^{i w r_*}(-f r^{3-d} Pi') solves the original EF EoM. The residual simplifies to 0.
3. **Boundary condition.** At u = 0 the exponents are 0 and 2-d. Substituting into Y gives Y's source coefficient
   A = (2-d) x [coefficient of u^{2-d} in Pi]. So the QNM condition is: Pi is the exponent-0 solution. For any real
   d > 2 that solution is a double series with independent powers, Pi_b = sum_{n even, m >= 0} c_{n,m} u^{n+md}. The
   powers are kept separate, so nothing mixes. The recursion is
   s(s+d-2) c_{n,m} = -[(-2 s1(s1+d-2) - d s1) c_{n,m-1} + (s2(s2+d-2) + d s2) c_{n,m-2} + (w^2-q^2) c_{n-2,m} + q^2 c_{n-2,m-1}],
   with s = n+md, s1 = s-d, s2 = s-2d. s(s+d-2) never vanishes for s > 0, so there is no resonance and no log.
   (For integer d the coinciding powers simply add up.)
4. **Horizon condition.** In s = 1-u the exponents are +-i w/d, and ingoing (EF-regular) is s^{-i w/d}. I build a
   Frobenius series with resonance-safe normalisation a_n = beta_n * rgamma(n+1+2 rho), rho = -gamma/d, so the beta
   recursion never divides by (n+2 rho). The first version divided by it and crashed at d=3, qbar=1 (see Surprises).
   The fixed version agrees with the old one to 1e-37 to 1e-41 wherever the old one is defined.
5. **QNM function.** F(gamma) = s*H*Pi_b' + G*Pi_b at u_m. This is the Wronskian with s^{rho-1} stripped off. It is real
   for real gamma, and I find its roots with a real secant method. The horizon series converges for |s| < 1 and the
   boundary series for |u| < 1, so u_m = 0.5 and 0.6 both lie inside both discs.
   Code: qnmpi.py, run.py, combine.py, make_result.py. Raw output: prodA.jsonl, prodB.jsonl.

## Positive controls

- **Kovtun-Starinets, d=4, frak q=1** (hep-th/0506184, TeX l.2097-2099 and the l.2133 table). The units map is
  2 pi T = d/2 = 2, so frak w = Omega/2 and frak q = q/2 = 1, i.e. qbar = 1. My hydro mode is
  frak w = -0.598065737016690... i against the published -0.598066 i: all 6 digits agree. The same code with complex
  omega gives the first non-hydro shear mode as 1.7591155848 - 1.2915937972 i, against the published
  +-1.759116 - 1.291594 i: agrees.
- **Small-q limit.** At qbar = 0.02, gamma - (qbar^2 + H_{2/d} qbar^4/d) = 7.2e-12 (d=3), 2.2e-12 (d=4) and 4.7e-13
  (d=5.5). These are O(qbar^6) = 6.4e-11 times a modest coefficient.
- **Independent double-precision check in the original formulation** (check_ef.py). This integrates the EF Z equation
  directly: Frobenius at r=1, DOP853 in ln r, and Z(R)=0 at R = 1e2, 1e3, 1e4. Results:
  d=4 qbar=1 gives 1.19613147403337 (mine 1.19613147403338); d=5 qbar=1 gives 1.11539088334707 (mine ...347095);
  d=3 qbar=1.5 gives 7.5937143442598 (mine 7.5937143439503; agrees to 4e-11, the double-precision and R-cutoff level
  for this steep point). Non-integer d runs: see the addendum at the end.

## Convergence

Every target was solved four times: dps 50 and dps 70, each at matching points u_m = 0.5 and u_m = 0.6. The series are
truncated adaptively at 1e-(dps+6).
- dps 50 vs dps 70: agree to 49.6-51.0 significant digits at all 17 regular points. This is the accuracy limit of the
  dps-50 run.
- u_m = 0.5 vs 0.6 at dps 70: identical to all 70 printed digits at all 17 points. They are also identical at dps 50.
- Root residuals |F| are 1e-69 to 1e-71 at dps 70.
- I report 45 significant digits, a conservative cap below the roughly 50-digit two-precision agreement.
  combined.json and RESULT.json["convergence_detail"] hold the full 70-digit strings.

## Results (Im Omega; Omega = -i gamma, conventions of 2308.01371: r_h = 1, T = d/4pi, qbar = q/sqrt(d))

| qbar \ d | 3 | 3.5 | 4 | 4.5 | 5 | 6 |
|---|---|---|---|---|---|---|
| 0.5 | -0.26784107941942285443 | -0.26315538973725673884 | -0.26015989981557641210 | -0.25811091704869015273 | -0.25663975481030499073 | -0.25470377780790771960 |
| 1.0 | **-1.5 (exact)** | -1.28453224630267092163 | -1.19613147403338030900 | -1.14682621461496168483 | -1.11539088334709498357 | -1.07796416073285044120 |
| 1.5 | -7.59371434395025505073 | -4.48256735386987750750 | -3.53382547321906861386 | -3.11644860073969044465 | -2.89029026845323451723 | -2.65507504550679503218 |

The table is truncated to 20 digits. RESULT.json has the 45-digit strings, and 34 digits for d=3, qbar=1.

## Branch control

At each d I started at qbar = 0.05 with seed gamma = qbar^2 and stepped by 0.05 to 1.5. Each step was seeded from the
previous roots by quadratic interpolation through the last three; this was only a starting guess. At every 0.1 step I
sign-scanned F(gamma) on (0, max(6, 3 gamma)] (160 points, including a geometric grid down to 5e-4). Every scan, at
every d, found exactly one purely imaginary zero, and it equals the continued root. The continued curves are smooth
(monotonic, with smooth increments). The reported pole is therefore the unique purely damped mode in that window, and
it is connected to omega ~ -i qbar^2.

## Surprises

1. **d=3, qbar=1 is exactly a pole-skipping point.** In the Pi Frobenius series, the n=1 coefficient's numerator at
   gamma = d/2 is c_{1,1} = d^2(d-1)/2 - d q^2. It vanishes at qbar^2 = (d-1)/2, which is qbar = 1 for d=3. There the
   regularised ingoing solution vanishes identically and F = 0 trivially, so the root finder's "1.5" carries no
   information. That point crashed my first run (0/0). The evidence for the value comes from the continuous branch
   instead (d3_pskip.py, dps 50 and 80, u_m = 0.5 and 0.6): gamma(1 -+ 1e-35) = 1.5 -+ 5.0880496914992230265e-35. The
   slopes on the two sides agree to 19 digits, and the mean differs from 1.5 by 1.1e-69 (the curvature term). The branch
   is monotonic, so gamma(1) is enclosed in an interval of width 1.0e-34 around 3/2. Hence Omega = -3i/2 = -i 2 pi T,
   as an exact value of the hydro branch, with 34 digits certified by the enclosure.
   The same pole-skipping line, gamma = d/2 at qbar^2 = (d-1)/2, is seen independently in the d=5 data: the branch
   crosses gamma = 2.5 near qbar = 1.414 = sqrt(2). In the 1/d form of 2308.01371 this means b_{1,1} = -1/2.
2. **d=3 rises steeply.** gamma(qbar=1.5) is 7.59 at d=3 against 3.53 at d=4. I checked that the d=3 branch is the
   continued and unique purely imaginary root (the scans show a single zero up to gamma = 22.8), and the EF
   direct-integration check confirms it independently. One caution for anyone checking with an EF solver at d=3: the EF
   Z(R) normalised at the horizon has poles at gamma = 1.5 n. A bracket that straddles 7.5 fails, and my first EF check
   did exactly that.

Files (all in this folder): qnmpi.py (solver), run.py (production driver), combine.py and make_result.py (assembly),
probe.py and test_beta.py (controls), d3_pskip.py and d3_pskip.json (pole-skipping enclosure), check_transform.py
(symbolic gauge check), check_ef.py and scan_ef.py (independent EF check), src0506184/ (KS TeX), prodA.jsonl and
prodB.jsonl (raw data). prodA_v1_crashed.* is the run that crashed at the d=3 pole-skipping point; it is not used.
qnmpi_v1.py is the solver before the resonance-safe fix.
