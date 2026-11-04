# The Airy edge of shear hydrodynamics: a large-d law for the critical point of the AdS_{d+1} black brane, with a numerical radius bound at d = 512, 1024 and 8192

Moki & Julio (AI-assisted)

---

## Abstract

The radius of convergence of the shear hydro series of the AdS_{d+1} black brane is set by a level-crossing critical point, c0.
We track it as one continuous branch from d = 3 to d = 32768. It approaches (qfr^2, wfr) = (-2, i), the d -> infinity limit of
the published sound-channel pole-skipping point, as d^-1/3, with a coefficient fixed by the first zero (Im U > 0) of
Ai'^2 - U Ai^2, derived by formal matched asymptotics (no error bounds): c0 is an Airy turning point where the hydro mode meets
the non-decoupled tower of modes, and (qfr^2 + 2) - 2i(wfr - i) = 4/d + O(d^-4/3). A parameter-free matched model predicted c0 at
d = 8192-32768 to 8e-6 down to 8e-7 in qfr^2, with its form shaped on d <= 4096 and the blind values already on disk
(independence by the theory seat's self-report); the leading law alone misses by 1.36e-3 at d = 8192. A monodromy census places
the radius in [|c0| - dr, |c0|] at d = 512, 1024 and 8192 (dr = 0.005, 0.005, 0.002), barring a pole or a cancelling branch-point
pair within one sector; a coefficient route with a second solver family is consistent with radius = |c0| at d = 2048 only.
Pade-resummed 1/d series agree with blind exact shear diffusion poles (17 of 17 sealed cells, 16 fresh) and sound poles (16 of 16,
one a control) at d = 3..6 within sealed bars. Every scored prediction was written and hashed before its target was read, except
where flagged; failures are reported as failures.

---

## 1. Introduction

Hydrodynamics is a series in powers of momentum. In holographic plasmas its radius of convergence is set by critical points of
the spectral curve, which are level crossings in the quasinormal spectrum at complex momentum [GKST19a; GKST19b]. For
the shear mode of the AdS_5 black brane (d = 4) the nearest critical point is at qfr^2 = 1.8906469 +- 1.1711505i [GKST19b eq. (16a);
GKST19a s.4.2, eq. (4.20)]; for d = 3 it is the point z1 of [GL22 eq. (4.13)]. [GKST19a s.6] lists extending this work to holographic
models in the large-D limit as a direction for the future.

This paper follows that critical point, which we call c0, from d = 3 to d = 32768 and states one result:

> The critical point that limits shear hydrodynamics approaches (qfr^2, wfr) = (-2, i) as d^-1/3, with a coefficient fixed by the
> first zero of Ai'^2 - U Ai^2.

The law was derived by formal matched asymptotics, without error bounds (Section 3). Its physical content is that the critical
point is an Airy turning point where the hydro mode meets the non-decoupled tower of modes. It was tested forward, at dimensions
the theory seat had not computed (Section 4), and the critical point was checked to be the nearest singularity of the hydro
sheet at several large d (Section 5). Table 1 collects the headline numbers. The Airy layer of the AdS black brane at zero momentum
is known [CHM18 App. B], as is the Airy turning point for non-decoupled modes of large-D black holes [EST14 eq. (4.1); ET14] and the
large-d location qfr^2 = -2 as the singularity of a partially resummed series [GLP23]. What we add is the extension to complex
momentum and to the hydro/non-hydro collision, and a nearest-singularity statement at large d (Section 9).

**Table 1.** Headline results. Errors are absolute in qfr^2 unless stated.

| Item | Result | Status (section) |
|---|---|---|
| Airy law | qfr_c^2 + 2 = A d^(-1/3) + O(1/d), wfr_c - i = B d^(-1/3) + O(1/d); A = 1.021165 + 5.400669i, B = 2.700334 - 0.510583i | derived, formal (3) |
| 4/d relation | (qfr_c^2 + 2) - 2i(wfr_c - i) = 4/d + O(d^(-4/3)) | derived, formal (3) |
| No-fit forward test | matched model A: 8.1e-6, 2.6e-6, 8.2e-7 at d = 8192, 16384, 32768 | sealed, held; blind values on disk, self-report (4.3) |
| Leading law alone | misses by 1.36e-3 (d = 8192) and 3.3e-4 (d = 32768) | not a test (4.3) |
| Radius, monodromy | lies in [\|c0\| - dr, \|c0\|] at d = 512, 1024, 8192 | sealed, held; scorer written after data (5.1) |
| Radius, coefficients | consistent with \|c0\| at d = 2048 (relative 1.1e-5); not confirmed at d = 8192 | sealed; d = 8192 nearest-pair reading FAILED (5.3) |
| Track | one continuous branch d = 3..32768; all 8 published d = 4 digits reproduced; at d = 3 it is z1 of [GL22] | tracked continuation; census at d = 4, 256, 512, 1024, 8192 only (6) |
| Below the edge | shear diffusion pole 17/17 cells (16 fresh), sound pole 16/16 (15 fresh + 1 control), d = 3..6 | sealed, held (App. B) |

The limit point (-2, i) is also the d -> infinity limit of the published sound-channel pole-skipping point [BDGL18 eq. (2.4);
GSS17 eq. (10) at d = 4; GKST19a s.1]. Pole-skipping points have been compared with convergence radii before, at d = 3 and 4
[GKST19a s.1; JP20 s.6; AK21]; [GKST19a s.1] concluded from two models that pole skipping is "not directly related to the
convergence radius of the derivative expansion in hydrodynamics". What we add is the large-d behaviour: the two points coincide
only in the limit, and they approach it at different rates, d^(-1/3) for the critical point and 1/d for the pole-skipping point
(Section 7).

A companion paper [MJ26a] treats the static Gregory-Laflamme threshold series; the two share only the sealed-test protocol
(Appendix A). Pole predictions below the edge and two shear coefficients are supporting material (Appendices B, C).

---

## 2. Setup and conventions

We study the shear channel of the planar AdS_{d+1} Schwarzschild black brane. The critical-point work uses thermal units
qfr = q/(2 pi T), wfr = omega/(2 pi T), as in [GKST19a] and [GL22]; we write q2 = qfr^2. The hydro sheet is the radial continuation
of the hydro root from q2 ~ 0. A critical point is a point (q2, wfr) where two quasinormal frequencies collide; c0 denotes the one
tracked continuously in d from the published d = 4 point. The lower half q2-plane holds the mirror images; we quote the
upper-half point. Throughout, "radius of convergence" means that of the series of the dispersion relation wfr(q2) about q2 = 0,
not of the constitutive relations of the fluid; the two can differ, since modes can collide where the relation between densities and
fluxes stays analytic [Ga26, abstract]. The pole predictions of Appendix B use the conventions of [GLP23]: r_h = 1, T = d/(4 pi),
qbar = q/sqrt(d), Omega = omega.

At d = infinity the leading 1/d correction to the hydro pole is known in closed form. With sigma = q^2/d^2 = qfr^2/4 it is
g1 = sigma(psi(1 + 2 sigma) + gamma), the harmonic-number form of [GLP23 s.III.B], whose series converges for |q^2| < d^2/2, i.e.
|qfr^2| < 2. Its first pole, at sigma = -1/2, is q2 = -2; there the leading hydro mode gives wfr = i. This is the limit point of
this paper.

Tests were sealed in the lab's usual way: predictions and pass bars written to a file and hashed (SHA-256) before the target was
computed or read, scored by a script that was usually hashed with them, against values computed by a blind seat from the physics
specification only (Appendix A). HOLDS means a prediction passed its own bar. FAILED and VOID are printed as such. Each section ends
with its scorecard.

---

## 3. The Airy law

### 3.1 Statement

Let W(U) = Ai'(U)^2 - U Ai(U)^2. It equals the integral of Ai^2 from U to infinity, so W' = -Ai^2 and its zeros are simple. Let U1
be its first complex zero with Im U > 0, and T1 = Ai'(U1)/Ai(U1):

    U1 = -2.790298 + 1.094310i,      T1 = -0.321647 - 1.701104i.

The conjugate zero gives the mirror point in the lower half-plane. A theory seat derived, by formal matched asymptotics without
error bounds,

    qfr_c^2 + 2 = -4 T1 (2d)^(-1/3) + O(1/d),      wfr_c - i = 2i T1 (2d)^(-1/3) + O(1/d),

so that qfr_c^2 + 2 = A d^(-1/3) + O(1/d) and wfr_c - i = B d^(-1/3) + O(1/d) with

    A = 1.021165 + 5.400669i,      B = 2.700334 - 0.510583i,      A = 2iB.

The derivation also gives: no d^(-2/3) term; the relation

    (qfr_c^2 + 2) - 2i(wfr_c - i) = 4/d + O(d^(-4/3)),

in which the leading terms cancel because A = 2iB; a square-root branch point of the hydro pole on the hydro sheet; and pole order
3p - 2 at q2 = -2 for the p-th 1/d correction of the hydro pole.

### 3.2 Where it comes from

The derivation uses three regions in x = r^d. In the near zone (d = infinity) the shear equation is hypergeometric, and the
ingoing solution connects to the boundary through Gamma functions. In the far zone the solution is an exact Bessel function,
y = J_{d/2}(d sqrt(alpha) e^{-L/d}) with L = ln x and alpha = w^2 - sigma, w = omega/d. Near alpha = 1/4 the far-zone potential
becomes linear in L. With lambda = (2d)^{1/3} and U = lambda^2 u/4 (u = 1 - 4 alpha), the equation reduces to y'' = (U + xi) y, whose
decaying solution is Ai(U + xi), so the far zone imposes the boundary ratio h(U)/lambda with h = Ai'/Ai. A collision of the hydro
root with its neighbour requires h'(U) = 0. Since h obeys the Riccati equation h' = U - h^2, this is W(U) = 0. At the next order the
quadratic terms of the near-zone function vanish at a zero (U = T^2 there), which is why there is no d^(-2/3) term. At order
lambda^-3 the zero shifts to U = U1 + 2/lambda, and in the combination (qfr^2 + 2) - 2i(wfr - i) every t-dependent term cancels,
leaving 8/lambda^3 = 4/d. This outline summarises the theory seat's write-up, which is not covered by the seal; an internal
referee re-checked the near-zone closed form, the absence of the d^(-2/3) term and X = 4/d, but the reduction to the Airy equation
and the collision condition were not re-derived independently.

The other zeros of W (U2 = -4.457445 + 1.026505i, U3 = -5.846242 + 0.979174i, ...) give a ladder of further critical points;
at leading order rung 1 has the smallest |qfr^2|; the theory seat places the whole ladder on the hydro sheet for radial paths (not
independently checked). The full matched model used in
Section 4 (model A) adds the first 1/d correction N1 of the near-zone function, fixed from the exact g1 with no data, and keeps the
exact Bessel far zone. One of its inputs, the slope N1_t = -zeta(3), rests on Taylor identities that were identified numerically.

### 3.3 Checks

An internal referee recomputed U1, T1, A and B to 20 digits, confirmed the absence of the d^(-2/3) term, the relation X = 4/d and
the pole order, and checked the closed form of the near-zone boundary ratio against the ODE to 1e-9..3e-12. The pole order 3p - 2
and the leading Laurent coefficients -1/32, 5/256, -11/512, 539/16384 (p = 2..5) were compared with the lab's exact 1/d coefficients
of the hydro pole. The predicted loop closures of the square-root branch point, 0.0090 (d = 256) and 0.00234 (d = 4096), compare
with the measured 0.0096 and 0.00243. Against the tracked data at d <= 4096, model A misses by 2.6e-5 at d = 4096, with a residual
falling as d^(-5/3). These comparisons with d <= 4096 are post hoc: the d^(-1/3) exponent was chosen after the first sealed test
(Section 4.1), and model A was shaped while watching those residuals.

### 3.4 What is and is not claimed

The law is a formal asymptotic result: no remainder bound is proved. N1_t = -zeta(3) is numerically identified. "On the hydro
sheet" depends on the path convention (radial continuation from q2 ~ 0). The relation of the limit point to [CHM18] is discussed in
Section 9.

---

## 4. Forward tests

### 4.1 First sealed test (BAR-DYN1): headline failed

A blind seat, with its own electric-field equation in x = r^d and Bessel far-zone matching, reproduced all 8 published digits of
the d = 4 critical point [GKST19a] (the published value was also its Newton seed) and tracked c0 to d = 256..4096, values sealed
beforehand as fresh. The sealed headline P2 FAILED: of two pre-chosen fit families, the d^(-1/3) family's limit landed 0.011 from
(-2, i) and the d^(-1/2) family's 0.107 away, against a 0.05 bar for both (the bar's own FAILED line, both families beyond 0.1, was
not reached; the sealed scorer assigns FAILED to this in-between case, and the two family limits differed by 0.099, just under the
0.1 VOID line). P1 (census at every d) FAILED, since the census ran only at
d = 256, where c0 was the nearest on-sheet critical point of 24 with |q2| < 3. P3 held: the local approach exponent between d = 2048
and 4096 was 0.339, still drifting (0.358, 0.349, 0.343, 0.340 over d = 256..4096). P4 held (|q2| = 1.967 < 2 at d = 1024).
Disclosures: the target (-2, i) was named after a d = 4..192 track had shown the drift towards it (only d >= 256 was unseen), and
the null N1 could not fail as scored.

### 4.2 Fit forward test (BAR-DYN1b)

Selecting d^(-1/3) after DYN1, a four-parameter fit (limit plus d^(-1/3), d^(-2/3), d^(-1) terms) on d = 512..4096 predicted c0 at
d = 8192, 16384 and 32768. All three held, about 20 times inside the bars (Table 2). A seven-point refit gives the limit
q2 = -2.00055 - 0.00003i, wfr = 1.00017i (P4 held). P6 (blind value closer to the d^(-1/3) family than to a rival d^(-1/2) family at
d = 32768) held by factors 40 (q2) and 63 (wfr), but P6 and the rival were sealed after the blind values were on disk. P5 (census at
d = 512 and 1024) FAILED: at d = 1024 an annulus 1.937 < |q2| < 1.967 was left uncertified (closed later by BAR-RC, Section 5.1).
Monodromy at three loop radii shows a genuine square-root branch point at d = 1024 and 8192: the loop sends the hydro root to the
other member of the colliding pair, with a separation growing close to sqrt(r).

**Table 2.** BAR-DYN1b: sealed fit predictions and blind values.

| d | predicted q2 | \|dq2\| | bar | \|dwfr\| | bar |
|---|---|---|---|---|---|
| 8192 | -1.94841101 + 0.26886491i | 4.2e-5 | 9.7e-4 | 1.3e-5 | 3.2e-4 |
| 16384 | -1.95945014 + 0.21312491i | 1.4e-4 | 2.8e-3 | 4.3e-5 | 9.3e-4 |
| 32768 | -1.96812400 + 0.16903630i | 2.8e-4 | 5.3e-3 | 8.7e-5 | 1.7e-3 |

### 4.3 The no-fit forward test (BAR-THEORY)

The theory seat ran no solver above d = 4096 and reports that it never read the folder of the DYN1b test. It registered predictions
before the DYN1b blind result was delivered, but the blind d >= 8192 values were already on disk, so independence rests on its
self-report. Model A is parameter-free: the matched model of Section 3.2 with N1 fixed from g1. Its form was shaped while watching
the d <= 4096 residuals, and its bars come from the d = 4096 residual, so its d = 4096 miss of 2.6e-5 is a check, not a test. Model
B adds a residual calibrated on the DYN1 data.

**Table 3.** BAR-THEORY: absolute errors against the blind values (bars in brackets).

| d | T1: model A \|dq2\| | model A \|dwfr\| | T2: model B \|dq2\| | leading law alone \|dq2\| |
|---|---|---|---|---|
| 8192 | 8.1e-6 (1.6e-5) | 4.2e-6 (8.3e-6) | 9.7e-8 (5.0e-6) | 1.36e-3 |
| 16384 | 2.6e-6 (5.1e-6) | 1.3e-6 (2.6e-6) | 4.5e-8 (2.0e-6) | 6.7e-4 |
| 32768 | 8.2e-7 (1.6e-6) | 4.2e-7 (8.2e-7) | 1.8e-8 (7.4e-7) | 3.3e-4 |

In words: the matched model A predicted the critical point to 8e-6 down to 8e-7 in qfr^2, with the model's form shaped on d <= 4096
and the blind values already on disk; the leading law alone misses by 1.36e-3 at d = 8192. The accuracy belongs to the full matched
model, not to the leading Airy law.

T3 held: the residual after the leading law falls with local exponent 1.02 between d = 8192 and 32768, as 1/d should. T5 held: the
blind monodromy at d = 8192 shows an on-sheet, radius-independent swap. T4 as sealed ("|X d/4 - 1| < 0.05 at d = 32768", with
X = (qfr^2 + 2) - 2i(wfr - i)) FAILED. It had been shown before the data to be mis-set, because the theory's own models give 0.110,
0.087 and 0.069; the replacement T4' (monotone decrease, and the d = 32768 value within 0.01 of 0.069) held with 0.1076, 0.0861,
0.0688.

### 4.4 Scorecard: law and forward tests

| Test | Prediction (short) | Verdict | Realised numbers / disclosure |
|---|---|---|---|
| BAR-DYN1 C1 | d = 4 control vs [GKST19a] | HOLDS | all 8 published digits; published value was the Newton seed |
| BAR-DYN1 P1 | census at every d | FAILED | census only at d = 256 |
| BAR-DYN1 P2 | limit within 0.05 of (-2, i), two families | FAILED | d^(-1/3) family 0.011, d^(-1/2) family 0.107 |
| BAR-DYN1 P3, P4 | exponent in [0.28, 0.55]; \|q2\| < 2 by d = 1024 | HOLD | 0.339; 1.967 |
| BAR-DYN1 N1 | null | HOLDS (cannot fail as scored) | - |
| BAR-DYN1b P1-P3 | c0 at d = 8192, 16384, 32768 | HOLD | \|dq2\| 4.2e-5 .. 2.8e-4, about 20x inside bars |
| BAR-DYN1b P4 | 7-point refit limit within 0.01 of (-2, i) | HOLDS | q2 = -2.00055 - 0.00003i, wfr = 1.00017i; follows nearly automatically from P1-P3 |
| BAR-DYN1b P5 | census at d = 512, 1024 | FAILED | d = 1024 annulus 1.937-1.967 uncertified |
| BAR-DYN1b P6 | closer to d^(-1/3) than d^(-1/2) family at 32768 | HOLDS | 40x, 63x; sealed after blind values were on disk |
| BAR-THEORY T1 | parameter-free model A | HOLDS | 8.1e-6 .. 8.2e-7 (q2), about half-bar; self-report independence |
| BAR-THEORY T2 | calibrated model B | HOLDS | 9.7e-8 .. 1.8e-8 (q2) |
| BAR-THEORY T3 | residual exponent >= 0.85 | HOLDS | 1.02 |
| BAR-THEORY T4 | \|X d/4 - 1\| < 0.05 at 32768 | FAILED | 0.0688; mis-set, shown before the data |
| BAR-THEORY T4' | monotone, within 0.01 of 0.069 | HOLDS | 0.1076, 0.0861, 0.0688 |
| BAR-THEORY T5 | on-sheet branch point at 8192 | HOLDS | radius-independent swap |

---

## 5. The radius of convergence

### 5.1 Monodromy certificate (BAR-RC)

For each d a sector-monodromy census followed the hydro root out along rays from the origin and then along short arcs between
neighbouring rays, at radius R_in = |c0| - dr and R_out = |c0| + dr. A singularity inside a sector shows up as a mismatch between
the arc end and the next ray. The sealed rules required a positive control just outside (exactly the sector containing c0 must
light up at R_out) and a trivial disk inside (every upper-half sector below 1e-9 in two runs with different step sizes); a converged
mismatch above 1e-6 inside would have been FAILED. At d = 1024 (dr = 0.005), 512 (dr = 0.005) and 8192 (dr = 0.002) the control
passed, with only the c0 sector lit (mismatches 7.3e-3, 1.07e-2 and 1.6e-3, equal in both runs), and inside the disk the largest
mismatch was at most 9.2e-14: P1, P2, P3 HOLD. No sector at any d lies between 1e-13 and 1e-3, so any threshold choice gives the same
verdict. An extra, unsealed run at d = 1024 with dr = 0.001 was also clean.

Statement: at d = 512, 1024 and 8192 the radius of convergence of the shear hydro series in q2 lies in [|c0| - dr, |c0|]
(dr = 0.005, 0.005, 0.002), barring a pole of w(q2) or a cancelling branch-point pair within one sector.

Caveats. The census is blind to the band |c0| - dr < |q2| < |c0|, to poles and to cancelling branch-point pairs inside one sector,
and covers the lower half-plane by mirror symmetry. It uses the same solver family as DYN1b. The d = 8192 control margin is 1.6x
(mismatch 1.6e-3 against the 1e-3 line). Three code versions were used (v1 at d = 1024, v2 at d = 512, v3 at d = 8192); all accept a
step on the same Newton and predictor-error test and differ only in the detector for sudden drops in the local root spacing. Two
attempts that stalled before any arc ran produced no results. The scoring script was written and hashed after the result arrived;
it applies the sealed rules verbatim. The upper end |c0| assumes the lit-sector singularity is c0 itself (loop monodromy at d = 1024
and 8192; at d = 512 the sector test only).

### 5.2 Coefficient route, first attempt (BAR-RC2): FAILED as sealed

A second solver family (a separately derived equation, used later in RC3) computed Taylor coefficients of the hydro mode and fitted
their large-order behaviour with a free exponent at n <= 110. It put the radius 1.0-1.7% above |c0| (relative 1.05e-2 at d = 512,
1.68e-2 at d = 1024, bar 1e-2), inside its own error bars. The independent route neither confirms nor refutes radius = |c0| at
d = 512 and 1024. Its positive control reproduced the d = 4 point of [GKST19a] (|q2| = 2.22399). An internal referee traced the failure
to a crowded ladder of singularities plus the free exponent; a fixed-ladder re-analysis is consistent with |c0| but is post hoc and
not a test. The seat's reported "direct collisions" at d = 512 were artefacts of an aliased stencil and are withdrawn. Post hoc,
c0(512) is a double root of the second family's equation, which confirms that it is a level crossing, not that it is the nearest.

### 5.3 Coefficient route, second attempt (BAR-RC3)

At d = 2048 and 8192, where no coefficients yet existed, the same second solver family (now with a Bessel boundary match) computed
Cauchy coefficients on circles of radius 1.85 and 1.92, and fitted them with a fixed square-root exponent (beta = 1/2) and a ladder
of up to four conjugate square-root pairs. The exponent and the ladder model were supplied by the sealed brief; free single-pair fits
give beta = -1.8 (d = 2048) and -1.0 (d = 8192) and describe the data far worse. A synthetic-ladder positive control, run first with
the same window and code, recovered R to 6.5e-6 and the angle to 8.2e-6.

At d = 2048 (P1) the fitted radius agrees with |c0|: R = 1.9630256953 against 1.9630044924 (relative 1.1e-5; angle error 3.2e-6),
under both the reported-pair and nearest-pair readings of the scored fit. Over ten fits (windows and circles) R spans 8.5e-5, more
than the control error, and in 3 of 10 fits an extra weak pair appears inside |c0| (R = 1.904-1.959), at a different place each time.
The coefficient route is consistent with radius = |c0| at d = 2048.

At d = 8192 (P2) the fixed-exponent ladder fit is ambiguous. The reported pair agrees with |c0| to 5.3e-5 (R = 1.9667280547 against
1.9668317798; angle error 8.5e-5), but 7 of 10 fits also place weaker square-root pairs inside |c0| (down to 1.912), which the
monodromy census excludes. The seat reported the pair with the largest contribution at the end of the window, whereas its own
synthetic control and fit driver used the nearest pair. In the scored fit the nearest pair sits at R = 1.95119, relative 7.95e-3 from
|c0|, beyond the sealed 5e-3 FAILED line; 2 of 10 fits also break the angle tolerance. Under the nearest-pair rule used by the
synthetic control, P2 would read FAILED. We treat d = 8192 as not confirmed by the coefficient route.

### 5.4 Repair attempt (BAR-RC3R): VOID

To settle the d = 8192 pairs we sealed a third-circle check: Cauchy coefficients are the same on any two circles with no
singularity between them, so coefficients on rho = 1.960 should match those on rho = 1.92 if nothing lies in 1.92 < |q2| < 1.96,
poles included. The test required an inner control at d = 2048 (rho = 1.92 against 1.95, agreement below 1e-6) and an outer control
(rho = 1.92 against 1.98, beyond c0, which must disagree). The outer control passed (maximum relative difference 64.6). The inner
control FAILED (1.9e-3), so the test is VOID as sealed. The bar was mis-designed: it ignored aliasing of the M = 1024-point
transform, of size (rho/R)^M, for circles close to R, and near-zero coefficients produce spikes in a maximum-relative measure. At
d = 8192 the maximum relative difference was 4.0e-2, at such a spike. The seat's descriptive reading, that the differences track the
aliasing expected for R = 1.9667 within about a factor 2, with no order-one change, argues that the inner pairs are a fit artefact,
but it is post hoc and not a test. Loop closure does not decide the question either, because swaps of a conjugate pair cancel.

### 5.5 Statement and open range

At d = 512, 1024 and 8192 the radius of convergence of the shear hydro series in q2 lies in [|c0| - dr, |c0|] (numerical monodromy certificate,
one solver family), barring a pole or a cancelling branch-point pair within one sector. A coefficient route with a second solver
family is consistent with radius = |c0| at d = 2048; at d = 8192 it does not confirm it. Whether c0 remains the nearest hydro-sheet
singularity at every 4 < d < 512 is open: it is the nearest at d = 4 [GKST19a] and at d = 256 (census, Section 4.1), and the track in
between is a continuation, not a census. The values of |c0| are 1.9791 (d = 512), 1.9669 (1024), 1.9630 (2048) and 1.9668 (8192); we
do not quote a radius of 2 at finite d.

### 5.6 Scorecard: radius

| Test | Prediction (short) | Verdict | Realised numbers / disclosure |
|---|---|---|---|
| BAR-RC P0 | only the c0 sector lit at \|c0\| + dr | PASS at all d | 1.07e-2, 7.3e-3, 1.6e-3 (d = 512, 1024, 8192); 8192 margin 1.6x |
| BAR-RC P1-P3 | no singularity inside \|c0\| - dr (d = 1024, 512, 8192) | HOLD | max mismatch <= 9.2e-14; scorer written after data; three code versions |
| BAR-RC2 PC | d = 4 radius of [GKST19a] | PASS | 2.22399 |
| BAR-RC2 P1, P2 | free-exponent radius = \|c0\| to 1% | FAILED | 1.05e-2, 1.68e-2 |
| BAR-RC3 SPC | synthetic ladder recovered | PASS | 6.5e-6 (R), 8.2e-6 (angle) |
| BAR-RC3 P1 | radius at d = 2048 | HOLDS | 1.1e-5; beta and ladder supplied; inner pairs in 3 of 10 fits |
| BAR-RC3 P2 | radius at d = 8192 | HOLDS as printed; nearest-pair reading FAILED | reported pair 5.3e-5; nearest pair 7.95e-3; selection rule changed after the control |
| BAR-RC3R C_out | coefficients change across c0 | PASS | 64.6 |
| BAR-RC3R C_in | inner control agrees < 1e-6 | FAILED | 1.9e-3 (aliasing; bar mis-designed) |
| BAR-RC3R P1 | nothing in 1.92 < \|q2\| < 1.96 at d = 8192 | VOID | 4.0e-2 at a near-zero spike; descriptive reading post hoc |

---

## 6. The track from d = 3 to d = 32768

c0 was followed continuously in d. A blind seat reproduced all 8 published digits of the d = 4 point [GKST19a], and the branch is one
continuous track from d = 3 to d = 32768: a tracked continuation with maximum jump 0.013, with censuses only at
d = 4 [GKST19a], 256, 512, 1024 and 8192. For 4 < d < 256 it is a track, not a census. Its real part changes sign once, near
d ~ 11.2, and Im wfr near d ~ 8.3, so the same branch moves from Re q2 > 0 (d = 3, 4) to Re q2 < 0 (large d).

At d = 3 the tracked point is c0 = 1.725047791406603 + 0.340135868692162i (the reverse track returns to the d = 4 point to 2e-13). It is
the critical point z1 of [GL22 eq. (4.13)] (units identical), not their negative-axis point z-1 = -1.88524.[^z1] At d = 3 and 4, c0 is
therefore the published nearest shear critical point; at large d it is the point of the Airy law.

[^z1]: [GL22 eq. (4.13)] prints z1 = 1.72557 + 0.340429i and states 10-digit accuracy. Our value differs by 6.0e-4 in qfr^2 and 1.4e-3 in wfr (5.2e-4 and
1.2e-3 in the real parts). A separate solve of their equation (4.11) from their seed converges to our value to 1e-11. The cause is not known. This
comparison is unsealed and has not been checked by an internal referee.

**Table 4.** c0 at selected d (qfr^2; values from the tracked solutions).

| d | c0 = qfr^2 | \|c0\| | source of the value |
|---|---|---|---|
| 3 | 1.725047791406603 + 0.340135868692162i | 1.75826 | track (unsealed) |
| 4 | 1.8906468611525056 + 1.171150523650781i | 2.22399 | sealed control (DYN1 C1) |
| 512 | -1.85434196376243291 + 0.69167010802565605i | 1.97914 | DYN1b blind |
| 1024 | -1.89017211961140767 + 0.54394161033931206i | 1.96688 | DYN1b blind |
| 2048 | -1.9154981851895594 + 0.42924741091280705i | 1.96300 | DYN1 blind |
| 8192 | -1.94836923521368989578 + 0.26885790575211286270i | 1.96683 | DYN1b blind |
| 16384 | -1.95931350079439501531 + 0.21310485985956267202i | 1.97087 | DYN1b blind |
| 32768 | -1.96785054944873001007 + 0.16900073487507457992i | 1.97509 | DYN1b blind |

Along the track |c0| dips below 2 before the limit (Table 4), after which |c0| rises towards 2 as
2 - Re(A) d^(-1/3) + (Im A)^2 d^(-2/3)/4 + O(1/d) = 2 - 1.02 d^(-1/3) + 7.3 d^(-2/3) + ..., the d^(-2/3) term producing the dip. The
two-term form gives 1.9673 at d = 8192 (data: 1.9668) and a minimum of 1.964 near d ~ 2900.

---

## 7. A contrast with pole skipping

The limit point (-2, i) is the d -> infinity limit of the published sound-channel pole-skipping point. In our units that point sits
at qfr^2 = -2(d - 1)/d, wfr = +i (from [BDGL18 eq. (2.4)], converted to our d); at d = 4 it is (-3/2, i), the point of [GSS17 eq. (10)]
quoted in [GKST19a s.1].
It approaches the limit as 1/d: qfr^2 + 2 = 2/d exactly, with wfr = i at every d. The shear critical point approaches the same limit
as d^(-1/3), with both qfr^2 and wfr moving. At d = 8192, for example, |qfr^2 + 2| is 0.274 for c0 and 2.4e-4 for the pole-skipping
point. The shear critical point does not coincide with it at any d we computed, and the two points belong to different channels
(shear, and sound/energy density).

Comparing the pole-skipping point with the radius of convergence is not new. [GKST19a s.1] did it in strongly coupled N = 4 SYM
(d = 4), where the pole-skipping point lies inside the convergence disk, and in a model with broken translations, where it lies
outside, and concluded from these two models that pole skipping "is not directly related to the convergence radius of the
derivative expansion in hydrodynamics"; [GKST19a s.6] adds that "in general, the critical points and the pole-skipping points are
different". [JP20 s.6] found for charged branes at d = 3 and 4 that the pole-skipping point can lie inside or outside the radius,
depending on the charge. [AK21] observed, for gapped modes at d = 4, that the critical point always lies inside the circle through the
nearest pole-skipping point in the (Im wfr, Im qfr^2) plane. Our data do not contradict any of these at finite d. The new element is the large-d
behaviour: for the shear channel of this brane, the critical point c0 (radius-setting at the d where we checked) and the sound-channel pole-skipping point merge
as d -> infinity, at different rates (d^(-1/3) against 1/d). We read this as a coincidence in the limit, not as evidence of a
mechanism linking the two; no sealed test of the contrast has been run, and we leave it as an open question.

The same point (-2, i) is also the first pole of the exact correction g1 (Section 2), the singularity location of [GLP23], and,
by arithmetic, a point on the momentum continuation wfr^2 - qfr^2 = 1 of the zero-momentum Airy threshold of [CHM18] (Section 9).

---

## 8. Limits

- The Airy law comes from formal matched asymptotics without error bounds. N1_t = -zeta(3) is numerically identified, and "on the
  hydro sheet" depends on the path convention.
- The forward-test accuracy (8e-6 down to 8e-7) is that of the full matched model A, shaped on d <= 4096, not of the leading law;
  independence rests on the theory seat's self-report, since the blind values were on disk.
- The radius statement holds only at the listed d (monodromy at 512, 1024, 8192 with the caveats of Section 5.1; coefficient route
  consistent at 2048 only; at 8192 not confirmed, and the repair test was VOID). Nearest-singularity status for 4 < d < 512 is open
  except at d = 256.
- One channel (shear) and one background (the neutral planar AdS_{d+1} Schwarzschild brane). A sound-channel analogue of the law has
  been derived; its forward test is not yet evaluable.
- Below the edge (Appendix B): one diffusive shear pole and one sound pole, at real momentum; agreement within sealed bars, not
  exactness; Pade convergence is not proved; reach beyond the hydro radius is not established.
- Process: several tests carry disclosed slips, each stated next to its test (minor ones in Appendix D). None changed a printed
  verdict; some reduce a test's weight, and one (BAR-RC3 P2) reads FAILED under the control's rule.

---

## 9. Prior art and credit

That a level-crossing critical point sets the radius of convergence of hydrodynamics is due to [GKST19a; GKST19b], with
d = 4 in [GKST19a; GKST19b] and d = 3 in [GL22]; charged branes at d = 3 and 4 are treated in [JP20]. The large-d location qfr^2 = -2 is in [GLP23], as the singularity of a partially resummed
series; [GLP23] also states that the convergence properties of the 1/d series "are for the moment not well understood", a remark
about the series of each q^(2j) coefficient that we do not claim to contradict. The Airy turning point for non-decoupled modes at
large D is in [EST14 eq. (4.1)] and its source [ET14]. The Airy layer of the AdS black brane at zero momentum is in [CHM18 App. B,
eqs. (B.12)-(B.26)], the closest precedent. Our law extends [CHM18] (and [EST14], [GLP23]) to complex momentum and to the
hydro/non-hydro collision; its coefficient comes from a collision condition, W(U) = 0, rather than from a zero of Ai.

Two prior-art searches (432 INSPIRE citers of the key papers screened, then every newer citer of the papers above, plus INSPIRE
full text, the arXiv API, Zenodo and web searches; floor: INSPIRE to 2026-11-02, arXiv to 2026-11-04, Zenodo to 2026-11-04) found no
d^(-1/3) law with Ai'^2 - U Ai^2 and no condition (qfr^2 + 2) - 2i(wfr - i) = 4/d, no large-d nearest-singularity certificate, no
published shear critical point at any d > 4, and no statement that the shear critical point and the sound-channel pole-skipping
point merge at large d at different rates. The comparison of pole-skipping points with convergence radii at d = 3 and 4 is prior
work (Section 7).

The gate notes, as its own arithmetic, that the limit point satisfies wfr^2 - qfr^2 = 1, the momentum continuation of the
zero-momentum Airy threshold of [CHM18], and that our 4/d relation is the linearisation of wfr^2 - qfr^2 = 1 - 4/d about that point.
Only the linearised form holds: writing wfr = i + delta, wfr^2 - qfr^2 - 1 = -X + delta^2, and delta^2 is of order d^(-2/3), so the
critical point does not lie on wfr^2 - qfr^2 = 1 - 4/d at order 1/d. We have not checked the [CHM18] connection beyond this.

The monodromy diagnostic is that of [GKST19a s.4.2]; the coefficient route follows [GL22] (Darboux). Other singularity-location
methods are the implicit-function-theorem prescription of [HSSSW20 eq. (40)] and the branch-point analysis of [JP20 s.3]. The
closest active neighbours are [AKRS26], who apply uniform-WKB and Airy turning-point methods to the shear mode of AdS_{p+2} branes at
large imaginary momentum (a different limit), and [Ar26], who lists contact with the large-d expansion as open. The sound-channel
pole-skipping point at d = 4 is due to [GSS17], and at general d to [BDGL18].

---

## 10. Data and code availability

The data and code for this paper are archived at Zenodo from release v1.0 of
https://github.com/Hashirama1337s/airy-edge-hydrodynamics (the DOI is listed on that page). The deposit contains:

- data/: the blind tracked critical points (d = 4..32768, with the d = 3 continuation and the high-precision refinements); the
  theory seat's model files and predictions; the monodromy-census results at d = 512, 1024 and 8192; the coefficient-route Cauchy
  coefficients, ladder fits and results (RC2, RC3, RC3R); and the predictions and blind poles of the two pole tests.
- code/: the critical-point solver and the continuation and refinement drivers; the model-A generator of the theory seat; the
  census code; the predictors and scorers of every sealed test in the scorecards; and three short scripts written for this deposit,
  which print the Airy constants and leading-law misses, regenerate the d = 4 control and Table 4, and list the per-fit pair readings
  of BAR-RC3. Lab scripts are copies in which only file paths were changed.
- SEALS/: for each sealed test, the files listed in its seal (prediction, scorer, verdict, blind result, addenda) with a table of
  hashes. Where a sealed file contained a lab-machine path, a personal name or a hand-typed approximate time, the deposited copy is
  redacted; the table then lists both hashes, and only the latter can be checked by a reader.
- REPRODUCE.md, with the commands, their outputs and run times, and MANIFEST.sha256 over all files.

Not included: the solvers and coefficient builders of the pole tests (Appendix B), the earlier (RC2) version of the second
solver family, and the theory seat's Laurent-coefficient and sheet checks.

---

## Appendix A. Methods

### A.1 Seats and sealed tests

A "seat" is one separately briefed computation or derivation, with stated access restrictions (for example, barred from another
seat's code, numbers and sealed files). An internal referee is a separately briefed seat of the same lab that re-checks a result;
this is not external peer review. Each test was written as a short file with its predictions and pass bars and hashed (SHA-256)
before the data that score it were computed or read; from 3 November the scoring script was usually hashed with it. A blind seat
then computed the target from the physics specification only. Disclosures written before results were read (addenda, amendments)
are noted with each test. Where a scorer was written after the data, that is stated. Bars were often far looser than the realised
errors, so we quote the errors themselves. The same protocol is described in [MJ26a, App. A].

### A.2 Solvers

Tracking and the monodromy census used an electric-field equation in x = r^d (the gauge-invariant field of [KS05]) with Taylor
stepping in ln x and exact Bessel far-zone matching (DYN1, DYN1b, RC). The coefficient routes (RC2, RC3, RC3R) used a second solver
family: a separately derived equation and solver, with a Bessel boundary match added in RC3; this is the second family, not a third.
The shear-pole blind seat used a Schwarzschild-gauge equation with two-sided Frobenius series and a Wronskian (DYN2). The sound blind
seat used the Kodama-Ishibashi master equation [KI03 eqs. (3.5)-(3.8)], cross-checked against a corrected form of the Z_S equation of
[MCKS09]; this is one solver with two equations (DYN3). Pade approximants are diagonal, in 1/d at fixed qbar: [21/21] for the shear
diffusion pole from 902 coefficients to order 42, [12/12] for the sound pole to order 32.

---

## Appendix B. Pole predictions below the edge (BAR-DYN2, BAR-DYN3)

### B.1 Shear diffusion pole

A builder computed the shear-channel diffusive pole as a 1/d series at fixed qbar (902 coefficients, orders to 42), found it
divergent (alternating, roughly factorial; Borel singularity on the negative axis), and resummed it with diagonal Pade [21/21]. It
ran no solver below d = 8. Predictions for d = 3..6 were sealed; a blind seat computed the exact poles. Pade [21/21] agrees with the
exact pole within the sealed bars in all 17 scored cells. One cell, qbar = 1 at d = 4, is not fresh: the builder had read the
6-digit published value -1.196132i [KS05] before resumming (nothing was fitted to it). Relative errors:

| qbar | d = 3 | 3.5 | 4 | 4.5 | 5 | 6 |
|---|---|---|---|---|---|---|
| 0.5 | 5.1e-11 | 1.7e-12 | 9.1e-14 | 6.6e-15 | 6.0e-16 | 8.7e-18 |
| 1.0 | 5.1e-5 | 3.4e-7 | 8.4e-9 (non-fresh) | 3.9e-10 | 2.8e-11 | 3.0e-13 |
| 1.5 | no claim | 6.0e-3 | 1.1e-4 | 3.8e-6 | 2.2e-7 | 2.2e-9 |

Range: 16 fresh cells, 2.2-17 digits overall, 3.9-17 at d = 4..6, 2.2-12 at d = 3..3.5 (worst fresh: qbar 1.5, d 3.5, relative
6.0e-3). Scope: one purely damped (diffusive) shear pole, one channel, real qbar <= 1.5. Independence is medium: the blind seat
changed gauge, variable and algorithm, but its method is of the same family as the builder's coefficient solver. The blind seat's
own non-integer-d cross-check never ran; an internal referee's check agrees to <= 3.5e-13 at three cells. At (d = 3, qbar = 1) the exact
value -3i/2 is the known n = 1 shear pole-skipping point [GLP23 s.III.B]; it is not new.

### B.2 Sound pole

The propagating sound pole was expanded to order 32 in 1/d (also divergent, Borel poles on the negative axis) and resummed with
Pade [12/12]; the recipe was hashed before the coefficients were aggregated. All 16 usable cells held at 3 x bar, and all 16 also
within 1 x bar (error/bar 0.07-0.50). These are 15 fresh cells plus one control, (qbar 1, d 4), whose published value the builder
and the blind brief had seen; the d = 4 result rests on one fresh cell (qbar 0.5, relative 3.2e-8). Relative errors:

| qbar | d = 3 | 3.5 | 4 | 4.5 | 5 | 6 |
|---|---|---|---|---|---|---|
| 0.5 | 2.5e-6 | 2.5e-7 | 3.2e-8 | 4.9e-9 | 9.0e-10 | 4.5e-11 |
| 1.0 | 1.2e-3 | 2.4e-4 | 4.4e-5 (control) | 8.1e-6 | 1.6e-6 | 9.0e-8 |
| 1.5 | - | - | - | 5.0e-3 | 8.8e-4 | 3.0e-5 |
| 3 | - | - | - | - | - | 4.1e-3 (branch-defined) |

The cell (qbar 3, d 6) is branch-defined: the pole is continued from d = infinity, and a collision between d = 5.5 and 5.75 is
inferred from a track flip, without locating the exceptional point. An internal referee's own solver reproduces the blind d = 4
values at qfr = 0.5, 1 and 3 to 25 digits. At d = 4 and large momentum (qfr = 3, 5) the resummation was not usable and no claim was
made. Whether the builder's reading of the published d = 4 value exposed a code bug that was fixed shortly afterwards is an open
question; it affects the control cell only.[^ks]

[^ks]: [KS05] prints Re wfr = 0.741420 for the d = 4 sound pole at qfr = 1. Two separate solves give 0.7414299654586609 -
0.2862800072464654i, and the table of [MCKS09] prints 1.48286, which is 0.74143 in the units of [KS05]. This is consistent with a
one-digit typo; a numerical error cannot be excluded.

### B.3 Relation to [EST15]

[EST15 s.5] argues that the 1/D expansion for decoupling modes "does not converge but is instead only asymptotic". Our coefficient
growth confirms divergence for these two modes, and their non-perturbative floor matches the bare-series optimal truncation at
d = 8 for the shear pole (truncation errors 2.5e-5..4.5e-2); the resummation beats that floor, and for this mode it is unambiguous
(Borel poles on the negative axis). [EST15 s.6] notes that the large-n expansion "does not afford a larger regime of applicability"
than hydrodynamics; our data do not address that statement beyond the cells above.

### B.4 Scorecard: pole predictions

| Test | Prediction (short) | Verdict | Realised numbers / disclosure |
|---|---|---|---|
| BAR-DYN2 | 17 cells within 3 x bar | 17/17 HOLD | 16 fresh; 2.2-17 digits; (qbar 1, d 4) non-fresh; independence medium |
| BAR-DYN2 H | all three qbar at d = 4 | HOLDS | 9.1e-14, 8.4e-9 (non-fresh), 1.1e-4 |
| BAR-DYN3 | 16 usable cells within 3 x bar | 16/16 HOLD | 15 fresh + 1 control; all within 1 x bar |
| BAR-DYN3 H | all usable d = 4 cells | HOLDS | rests on one fresh cell (qbar 0.5, 3.2e-8) |

---

## Appendix C. Two shear coefficients (BAR-SHEAR)

[GLP23] estimated the shear-channel coefficient c_{5,3} two ways, -15.814 and -15.502 (in units of 16 zeta(5)), 2% apart, and c_{5,4}
at -15.548, and could not exclude c_{5,3} = c_{5,4}. Our values are c_{5,3}/(16 zeta(5)) = -15.8137745672048... and
c_{5,4}/(16 zeta(5)) = -15.5363300880724... (P1, P2 HOLD; the P1 window is a sanity test only). Identified by guarded integer-relation
search (found on 66 digits, holding on the rest to 110): c_{5,3} = -192 zeta(5) - 32 zeta(2) zeta(3) and c_{5,4} = -132 zeta(5) -
48 zeta(2) zeta(3) - 24 zeta(4); c_{5,4} - c_{5,3} = 60 zeta(5) - 16 zeta(2) zeta(3) - 24 zeta(4). A second implementation (different master
field and method) reproduced the same closed forms for c_{5,3}, c_{5,4}, c_{6,3}, c_{6,4}, c_{6,5} and agrees numerically to
4e-51..3e-48. The identification is descriptive, not a sealed prediction. The control item C1 printed FAILED/INCOMPLETE because the
scorer read the wrong key name; no corrected scorer was sealed, so the controls (all at or above 120 digits) count only post hoc.
Our value of c_{5,3} agrees with the first published estimate and not the second, and c_{5,3} != c_{5,4}.

| Test | Prediction (short) | Verdict | Realised numbers / disclosure |
|---|---|---|---|
| BAR-SHEAR P1, P2 | c_{5,3}, c_{5,4} within 2-3% of published estimates | HOLD | -15.81377..., -15.53633... (x 16 zeta(5)); P1 a sanity window |
| BAR-SHEAR C1 | controls to >= 30 digits | printed FAILED/INCOMPLETE | scorer key bug; controls >= 120 digits post hoc |

---

## Appendix D. Further disclosures

Disclosures that change a test's weight are stated next to the test (Sections 4.1-4.3, 5.1-5.4, Appendices B, C). Minor ones:
BAR-RC2 was scored with an instrument fix (a non-numeric exponent mapped to NaN) that does not affect FAILED, which is set by R; for
BAR-DYN1 the brief allowed reading the method scripts and gave the published d = 4 location, and P1 was self-graded by the blind seat;
for BAR-DYN2 the lab already held exact d = 4 shear solves at complex qbar^2 ~ 0.4 (the builder ran none); for BAR-DYN3 the sealed
prediction file's hash differs from the builder's reported value only by line endings, recipe B was chosen after A's validation and is
descriptive, and the blind brief named the published d = 4 control value and hinted the leading small-q sound branch. The errata,
gate and referee files that fix the wording of this paper are working documents without seals of their own; their state at banking
is frozen by a manifest.

---

## References

- [AK21] N. Abbasi, M. Kaminski, "Constraints on quasinormal modes and bounds for critical points from pole-skipping", JHEP 03 (2021)
  265, arXiv:2012.15820, doi:10.1007/JHEP03(2021)265.
- [AKRS26] I. Aniceto, P. Kovtun, A. Ratcliffe, M. Spalinski, "Shear viscosity from complex light-cone expansion", arXiv:2610.32892
  (2026).
- [Ar26] P. Arnaudo, "Shear mode transport coefficients from multiple polylogarithms", Phys. Rev. D 113 (2026) 126011,
  arXiv:2602.06120, doi:10.1103/db8h-1slc.
- [BDGL18] M. Blake, R. A. Davison, S. Grozdanov, H. Liu, "Many-body chaos and energy dynamics in holography", JHEP 10 (2018) 035,
  arXiv:1809.01169, doi:10.1007/JHEP10(2018)035.
- [CHM18] J. Casalderrey-Solana, C. P. Herzog, B. Meiring, "Holographic Bjorken flow at large-D", JHEP 01 (2019) 181,
  arXiv:1810.02314, doi:10.1007/JHEP01(2019)181.
- [EST14] R. Emparan, R. Suzuki, K. Tanabe, "Decoupling and non-decoupling dynamics of large D black holes", JHEP 07 (2014) 113,
  arXiv:1406.1258, doi:10.1007/JHEP07(2014)113.
- [EST15] R. Emparan, R. Suzuki, K. Tanabe, "Quasinormal modes of (Anti-)de Sitter black holes in the 1/D expansion",
  JHEP 04 (2015) 085, arXiv:1502.02820.
- [ET14] R. Emparan, K. Tanabe, "Universal quasinormal modes of large D black holes", Phys. Rev. D 89 (2014) 064028,
  arXiv:1401.1957, doi:10.1103/PhysRevD.89.064028.
- [Ga26] L. Gavassino, "The causal diamond of relativistic hydrodynamics", arXiv:2610.02416 (2026); cited for its abstract only.

- [GKST19a] S. Grozdanov, P. K. Kovtun, A. O. Starinets, P. Tadic, "The complex life of hydrodynamic modes", JHEP 11 (2019) 097,
  arXiv:1904.12862, doi:10.1007/JHEP11(2019)097.
- [GKST19b] S. Grozdanov, P. K. Kovtun, A. O. Starinets, P. Tadic, "Convergence of the gradient expansion in hydrodynamics", Phys.
  Rev. Lett. 122 (2019) 251601, arXiv:1904.01018, doi:10.1103/PhysRevLett.122.251601.
- [GL22] S. Grozdanov, T. Lemut, "Reconstruction of spectra and an algorithm based on the theorems of Darboux and Puiseux", JHEP 02
  (2023) 131, arXiv:2209.02788, doi:10.1007/JHEP02(2023)131.
- [GLP23] S. Grozdanov, T. Lemut, J. F. Pedraza, "Reconstruction of the quasinormal spectrum from pole skipping", Phys. Rev. D 108
  (2023) L101901, arXiv:2308.01371, doi:10.1103/PhysRevD.108.L101901.
- [GSS17] S. Grozdanov, K. Schalm, V. Scopelliti, "Black hole scrambling from hydrodynamics", Phys. Rev. Lett. 120 (2018) 231601,
  arXiv:1710.00921, doi:10.1103/PhysRevLett.120.231601.
- [HSSSW20] M. P. Heller, A. Serantes, M. Spalinski, V. Svensson, B. Withers, "Convergence of hydrodynamic modes: insights from kinetic
  theory and holography", SciPost Phys. 10 (2021) 123, arXiv:2012.15393, doi:10.21468/SciPostPhys.10.6.123.
- [JP20] A. Jansen, C. Pantelidou, "Quasinormal modes in charged fluids at complex momentum", JHEP 10 (2020) 121, arXiv:2007.14418,
  doi:10.1007/JHEP10(2020)121.
- [KI03] H. Kodama, A. Ishibashi, "A master equation for gravitational perturbations of maximally symmetric black holes in higher
  dimensions", Prog. Theor. Phys. 110 (2003) 701-722, arXiv:hep-th/0305147, doi:10.1143/PTP.110.701.
- [KS05] P. K. Kovtun, A. O. Starinets, "Quasinormal modes and holography", Phys. Rev. D 72 (2005) 086009, arXiv:hep-th/0506184,
  doi:10.1103/PhysRevD.72.086009.
- [MCKS09] J. Morgan, V. Cardoso, A. S. Miranda, C. Molina, V. T. Zanchin, "Gravitational quasinormal modes of AdS black branes in d
  spacetime dimensions", JHEP 09 (2009) 117, arXiv:0907.5011, doi:10.1088/1126-6708/2009/09/117.
- [MJ26a] Moki & Julio (AI-assisted), "The Gregory-Laflamme threshold to order 1/n^12 and its resummation to AdS screening masses",
  preprint (2026), doi:10.5281/zenodo.23940227, https://github.com/Hashirama1337s/large-d-gregory-laflamme.
