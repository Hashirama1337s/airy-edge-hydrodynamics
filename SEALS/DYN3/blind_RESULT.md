# DYN3 blind seat: sound-channel QNM of the planar AdS_{d+1} black brane at real d

## Brief hygiene and independence
- **The brief gave me expected values.** It stated the leading hydrodynamic form (omega ~ qbar*sqrt(d)/sqrt(d-1)) and the KS target number (frak w = 0.741420 - 0.286280 i). I used the hydro form only as the starting guess at qbar = 0.02. I wrote that guess down myself from conformal sound speed v_s^2 = 1/(d-1) and eta/s = 1/(4 pi), then checked it numerically (see Branch). I treated the KS number as a check, not a target, and **my result does not match it in the 5th digit** (see Control).
- **Files I opened:** the allowed KS TeX (`DYN2/blind/src0506184/quasisound-v2.tex`), plus two arXiv sources I downloaded into my own folder (`src/ki`, `src/morgan`). I opened nothing under `zeta-k5/`, nothing else under `NEXT-2026-11-03/`, no BAR/SEAL/verdict files and no memory files.
- **Auto-loaded memory index:** the harness put the user's memory index (MEMORY.md) in my context automatically. It holds no sound-pole numbers.

## Object and conventions
- Metric: ds^2 = r^2(-f dt^2 + dx^2) + dr^2/(r^2 f), with f = 1 - u^d and u = 1/r (so r_h = 1). T = d/(4 pi), Omega = omega, q = qbar*sqrt(d).
- Time dependence is e^{-i omega t}. The horizon condition is ingoing, (1-u)^{-i omega/d}.

## Method
I used two different master equations and solved both with the same solver, which I wrote myself in python-flint arb/acb.

1. **Primary: the Kodama-Ishibashi scalar master equation.**
   - Source: KI, hep-th/0305147, `src/ki/ZerilliEq.tex`, lines 840-879: eq. (MasterEq) and Q in eq. (Q:NonStatic).
   - Settings: K = 0, lambda = -1, n = d-1, x = u^{d-2}, y = -1/u^2, m = q^2. Then f d/du(f dPhi/du) + (omega^2 - V_S) Phi = 0, with V_S = f Q / (16 H^2) and H = q^2 + d(d-1)u^{d-2}/2.
   - **Correction 1 (a secondary source disagrees with KI):** Morgan, Cardoso, Miranda, Molina and Zanchin (arXiv:0907.5011, eq. pots) quote a Q that differs from the KI original in the q^2 u^{d-2} term. This holds even at d = 4 (`symcheck_KI.py`). I used the KI original.
2. **Cross-check: a KS-type gauge-invariant Z_S for general d.**
   - Source: 0907.5011 eq. (fund-eq-scalar), TeX lines 628-645.
   - **Correction 2 (two transcription errors in Z_S):**
     - In X, the coefficients (d_M-3) and (d_M-1) are swapped. The TeX form fails the horizon indicial equation. The swapped-back form, X = 2(d_M-2)w^2 - [(d_M-1) + (d_M-3)f]q^2, passes it.
     - In Y4, the coefficient of u^{d_M-1} must be -(d_M-3), not +(d_M-1).
   - With both fixes, the equation at d = 4 is **symbolically identical to KS eq. (Zequation)** after u_KS = u^2 and frak w = omega/2 (`symcheck_d4.py`).
   - For general d, the Y4 coefficient -(d_M-3) is a candidate that I did not derive. Its only support is that the two equations agree to about 40 digits at every d, which a wrong coefficient would not give.
3. **Boundary condition at u = 0.** For Z_S this is Dirichlet: the u^0 series coefficient vanishes. For Phi_S the exponents are (5-d)/2 and (d-3)/2, and the condition depends on d:
   - d > 4: the coefficient of u^{(5-d)/2} vanishes.
   - d = 4: the coefficient of the sqrt(u) ln u solution vanishes.
   - 3 < d < 4: again the coefficient of u^{(5-d)/2} vanishes, even though this is now the subdominant power.
   - d = 3: Robin condition, Phi'(0)/Phi(0) = -3/q^2.

   I took these choices from Morgan et al. section 4 or worked them out. **Each one is confirmed by agreement with Z_S's Dirichlet roots** at d = 3, 3.5, 4, 4.5, 5 and 6.
4. **Numerics (my own algorithm, not a spectral method):**
   - Start from the ingoing Frobenius series at u = 1.
   - Continue analytically with exact Taylor-series recursions at real centres. Each step is at most 0.5 (P1 setting) or 0.35 (P2 setting) of the distance to the nearest coefficient singularity, including the horizon.
   - At u = 0, build a two-exponent Frobenius basis in v = u^g, where g is the lattice spacing of the exponents 2j + m(d-2). Where an exponent coincides with the other root, a ln u term is added: Z_S at d = 4 and 6; Phi_S at d = 4 and 6.
   - **No mixing at non-integer d:** for non-integer d, the extra v-lattice points that coincide with the other exponent carry zero source, so there is no log and no mixing.
   - Roots in omega come from the secant method. Nothing was fitted or extrapolated.

## Controls
- **d = 4, frak q = 1:** Omega = 1.482859930917321822978577 - 0.5725600144929307091324098 i, so frak w = 0.741429965458660911489288 - 0.286280007246465354566205 i.
  - The imaginary part agrees with KS. **The real part is 0.741430, not KS's 0.741420.** I believe KS line 2100 has a one-digit typo, for three reasons:
    - (i) My Z_S at d = 4 is KS's own equation, verified symbolically.
    - (ii) The independent KI equation gives the same root to 39 digits.
    - (iii) Morgan et al. Table tab3a, at d_M = 5 and their frak q = 2 (our qbar = 1), gives 1.48286 - 0.57256 i. That is frak w = 0.74143.
- **Morgan Table check, d = 5 and 6 (weak control):** these are their power-series (PS) and time-evolution (TE) results. Their own two methods disagree with each other by 1e-4 to 1e-2, so this control can only test about 3-4 digits.

  | d | Morgan d_M | Morgan frak q | Morgan PS | Morgan TE | Ours |
  |---|---|---|---|---|---|
  | 5 | 6 | 2 | 1.19804 - 0.58389 i | (not given) | 1.197954 - 0.583867 i |
  | 6 | 7 | 2 | 1.02097 - 0.520255 i | 1.01691 - 0.533577 i | 1.016604 - 0.533450 i |
  | 5 | 6 | 10 | 10.4304 - 0.728055 i | 10.4320 - 0.730181 i | 10.43205 - 0.72349 i |

- **Hydrodynamics at every d:** Re Omega/(v_s q) - 1 and -Im Omega/(Gamma q^2) - 1 shrink exactly as qbar^2 (ratio 4.00 when qbar halves). Here v_s^2 = 1/(d-1) and Gamma = (d-2)/(d(d-1)). This tests the d-dependence of the potential (`hydro_check.log`).

## Convergence
I solved every point three ways:
- **P1:** KI equation, 40 digits, match point u0 = 0.40 r_b, step factor 0.5, horizon point 0.5 r_h.
- **P2:** KI equation, 60 digits, u0 = 0.25 r_b, step factor 0.35, horizon point 0.4 r_h. Here r_b is the convergence radius of the boundary series.
- **Z_S** at 40 digits.

Agreement is 39.4-40.6 digits at every point except d = 4 with qbar = 3 and 5. There P1 vs P2 agree to 26.5-26.8 digits (the log basis loses precision at large q at 40 digits) and P2 vs Z_S to 36.6-36.9 digits. **I report 25 significant digits everywhere and trust all 25.** The values are P2.

**Bug found and fixed during the work:** match and centre positions were floats, so rounding capped accuracy at about 16 digits. Positions are now exact (Sterbenz). The pre-fix file is kept as `polish_PHIKI_buggy_float_positions.json`.

## Results (Omega, 25 significant digits)
| qbar | d | Re Omega | Im Omega |
|---|---|---|---|
| 0.5 | 3 | 0.6557192901923586153932755 | -0.1131315514597278221482401 |
| 0.5 | 3.5 | 0.6345149587524802115829244 | -0.1425363996064302344758108 |
| 0.5 | 4 | 0.6171109876160607927824209 | -0.1623465956595927582893231 |
| 0.5 | 4.5 | 0.6030659612167260534983107 | -0.1762497469146190849238837 |
| 0.5 | 5 | 0.5917047563381561117934154 | -0.1864163077048244085178319 |
| 0.5 | 6 | 0.5747406558877578131826556 | -0.2001534356676332593529017 |
| 1.0 | 3 | 1.506912470745559931910468 | -0.3146278593470880457344863 |
| 1.0 | 3.5 | 1.509029777793171294755332 | -0.4559817825730087595322060 |
| 1.0 | 4 | 1.482859930917321822978577 | -0.5725600144929307091324098 |
| 1.0 | 4.5 | 1.442502782512497306340149 | -0.6596950774874628030573700 |
| 1.0 | 5 | 1.399876910963287960801636 | -0.7218670982183267006057261 |
| 1.0 | 6 | 1.326452482080650299116620 | -0.7985965240597486313939053 |
| 1.5 | 4.5 | 2.777060742382736299652829 | -1.178064020266308268545615 |
| 1.5 | 5 | 2.727914585381067501106008 | -1.443368281282187046783399 |
| 1.5 | 6 | 2.507256626727891823785135 | -1.766931973397985697995887 |
| 3 | 6 | 11.84880808228719903122391 | -8.218724660647282360740273 |
| 3 | 4 | 6.181987251613330211120142 | -0.7049446523131661773796944 |
| 5 | 4 | 10.22330718329242174201763 | -0.5367401203020710449752389 |

## Branch, and the main surprise
- **How I followed the branch:** for each d, natural-parameter continuation in qbar from 0.02 (the hydro guess is accepted there). The predictor is linear; the step adapts up to 0.25 and is halved whenever the corrector moves more than 25% of the previous increment. At d = 6 I re-tracked with a maximum step of 0.01 and got identical values.
- **At d = 6 the continuously followed sound pole turns strongly damped:**
  - Its path is 2.507 - 1.767 i at qbar = 1.5, then 4.608 - 3.123 i at qbar = 2, then **11.8488 - 8.2187 i at qbar = 3**.
  - At d = 6, qbar = 3 there is also a weakly damped pole at **8.135385546144508119200060026 - 1.221057085620792328184502183 i**. Its digits are confirmed by P1, P2 and Z_S.
  - That pole followed back in qbar at d = 6 becomes the **first non-hydro pole** (5.1017 - 2.5888 i at qbar = 0.5).
  - The same pole followed in **d** at fixed qbar = 3, starting from the d = 5 sound pole (7.1519 - 0.9889 i), lands on it smoothly.
- **Where it flips:** tracking in qbar gives the weakly damped branch at qbar = 3 for d = 5.25 and 5.5, and the strongly damped branch for d = 5.75 and 6. So the sound pole and the first non-hydro pole collide (an exceptional point) somewhere between d = 5.5 and 5.75, at roughly 1.5 < qbar < 3.
- **Consequence:** at qbar = 3, d = 6 the "sound pole" is a matter of definition. I report the continuous-in-qbar value, as the brief asks, and give the other pole as an extra. At d = 4 and qbar = 3 or 5 the branch is the usual weakly damped one.

## Files (all in `<lab>/NEXT-2026-11-03/dynamics/DYN3/blind/`)
- **Code:** `qnm.py` (solver, both equations), `track.py` and `track_all.py` (continuation), `polish.py` (P1/P2 runs), `symcheck_d4.py` and `symcheck_KI.py` (symbolic checks), `hydro_check.py`, `branch6b.py`, `second_pole.py`.
- **Outputs:** `polish_PHIKI_P1_P2.json`, `polish_ZS_P1.json`, `track_*.json`, `branch6b.log`, `hydro_check.log`, `second_pole.log`.
- **Sources:** in `src/`.
