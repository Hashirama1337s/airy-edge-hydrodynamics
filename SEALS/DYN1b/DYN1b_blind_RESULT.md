# DYN1b blind seat (continuation): c0 track at d = 8192 / 16384 / 32768, multi-radius monodromy, census

## Disclosures (read first)
- **Brief hygiene.** The brief defined the object (the shear-channel hydro critical point c0, in thermal units qfr^2 and
  wfr, continued in d as in DYN1/blind) and the outputs. It also suggested loop radii (0.005, 0.01, 0.02). It gave no
  target numbers, functional forms or expected verdicts. I did no fitting or extrapolation.
- **What I opened.** Only this folder and DYN1/blind/ (its RESULT.md, RESULT.json, mono_1024.log and refine_c0_B.jsonl).
  I did not open any forbidden path: BAR, AMENDMENT, PRED, predict, backtest, verdict and council files, the rest of
  NEXT-2026-11-03, or the memory files. The harness put the user's auto-memory index into my context automatically.
  I did not open any memory file, and that index contains no c0 numbers.
- **Formulation.** This finishes an interrupted seat, so I reused that seat's solver (qnmx.py/lib.py). That solver uses the
  DYN1-blind formulation: the Kovtun-Starinets gauge-invariant field, x = r^d, Taylor stepping in ln x and exact Bessel
  far-zone matching. It is not the council's Chebyshev/Pi formulation. New code from this seat: mono5.py (branch pair seeded
  at c0), mono6.py (circles reusing the stored pair), sector.py (sector-monodromy disk census), axis.py, locate.py,
  make_result.py.

## 1. Track (reused, not recomputed)
pts_*.json held only double-precision copies. The full values are in refine_A.jsonl and refine_B.jsonl. Run A used 110 bits,
step ratio 1/4, h_max 1.0 and matching radius L_m 84.9. Run B used 150 bits, ratio 1/5, h_max 0.8 and L_m 127.6. Each run
converged quadratically: the last Newton step was 1e-32 for A and 1e-44 for B.
A and B agree to at most 2.0e-32 relative at all three d, in both q2 and wfr. That covers two precisions, two step
sizes and two matching radii. I report 30 significant digits.

| d | qfr^2 | wfr |
|---|---|---|
| 8192 | -1.94836923521368989578107576084 + 0.268857905752112862699432615375 i | 0.134404901544057985895951765231 + 0.974439322506571289027013216794 i |
| 16384 | -1.95931350079439501530751430502 + 0.213104859859562672017311843833 i | 0.106542621615250006612299233082 + 0.979782600164953684078849471810 i |
| 32768 | -1.96785054944873001007274367257 + 0.169000734875074579919142930464 i | 0.0844963963452528303236871780462 + 0.983987674395950440155656485705 i |

- on_sheet is true at 8192 (see section 2).
- At 16384 and 32768 no loop was run, so on_sheet is null there, meaning unknown. Each F evaluation costs roughly in
  proportion to d, and the PC was in use.

## 2. Monodromy: c0 is a genuine square-root branch point of the hydro pole (d = 1024 and 8192)
Method (mono5.py, then mono6.py), with no mirror guesses:
1. Seed the colliding pair at c0 itself from F ~ F_s ds + (1/2) F_ww (w - w*)^2, at distance 1e-7 from c0.
2. Continue both roots outward along the ray in t = sqrt(distance), which straightens the square root, to
   s_r = c0 - r e^{i arg c0}.
3. Continue the hydro root radially from qfr^2 = 0.05 and check that it is one member of the pair.
4. Take the hydro root once around |q2 - c0| = r (320 steps).

All numbers below are in wfr.

| d | r | closure | separation (pair) | end to partner | hydro root = pair member to |
|---|---|---|---|---|---|
| 1024 | 0.005 | 4.6611730572e-3 | 4.6611730572e-3 | 1.1e-15 | 1.9e-15 |
| 1024 | 0.01 | 6.6609648084e-3 | 6.6609648084e-3 | 1.0e-15 | 3.3e-15 |
| 1024 | 0.02 | 9.6157730155e-3 | 9.6157730155e-3 | 5.6e-16 | 6e-17 |
| 8192 | 0.005 | 1.6342667686e-3 | 1.6342667686e-3 | 7.1e-16 | see note (distance match to mono3, 1e-15) |
| 8192 | 0.01 | 2.3585474248e-3 | 2.3585474248e-3 | 2.8e-17 | see note |
| 8192 | 0.02 | 3.4696660240e-3 | 3.4696660240e-3 | 1.1e-16 | 3.1e-16 |

**Verdict.** At both d and at all three radii the loop sends the hydro root to the other member of c0's pair (a different
root) to machine precision. Closure equals separation, and the separation grows close to sqrt(r): the ratios are
1.43 and 1.44 at d=1024, and 1.44 and 1.47 at d=8192. So the swap does not depend on the radius, and c0 is a genuine
branch point on the hydro sheet.

**Convergence.** mono3.py is independent: its own radial path, 160- and 320-step circles and its own Newton partner.
It gives the same closures to about 1e-15 at both d. At d=8192 its uniform-step radial hydro root lies exactly as far from
w* as the pair member (1.3643309113e-3, 2.6433384870e-3 and 5.1860983602e-3 in w units, agreeing to 1e-15). I trust 10
significant digits in closure and separation.

**Note (d=8192, r = 0.005 and 0.01).** In mono5's own radial pass the last two segments had only 4 steps each, which is
my bug, and they jumped roots. That is why radialH_to_H is 0.05-0.08 in mono6_8192.json. The hydro identity at those
radii instead rests on two things. First, the radial root agrees with the pair member at r = 0.02 to 3e-16, and the pair
path is the continuation inward along the same ray. Second, mono3's correct uniform radial gives the matching distance
to w*.

**Why the old r = 0.02 tests said "UNCLEAR".** The roots crowd near c0 at large d. The neighbour spacing is about 0.0027
in wfr near the negative axis at d=1024, and smaller at d=8192. The mirror-guess Newton partner, 2w* - w_start, converged
to a neighbouring root, not the true partner. The local expansion is also strongly lopsided: the linear drift is
comparable to the square-root split (mirror asymmetry about 1), which pushes the mirror guess off. This explains DYN1's
"partner-finder hit a third root" at d >= 1024. It is not a failure of the swap.

## 3. Census / nearest
**d = 512: nearest_in_census = true.**
- The finding stage was already complete: census_512_g1 used 37 rays with drho 0.04, and census_512_g2 used 61 rays
  with drho 0.025. Neither grid alone finds every point (g2 misses |q2| = 2.077 and 2.211, which g1 found), so the
  list in RESULT.json is their union. The smallest |q2| is c0 at 1.979139, and the next is 2.076998.
- I added an exhaustive check that does not depend on seeding, the sector-monodromy disk census (sector.py).
  - Method: hydro-root rays at 49 angles in [0, pi] (mirror symmetry covers the lower half), plus the short arcs at
    radius R between neighbouring rays. A hydro-involving branch point inside a sector, below R, makes that sector's
    arc end disagree with the next ray.
  - At R = |c0| - 0.03 = 1.9491 all 48 sectors are trivial (max mismatch 6e-14; arcs with 40 and 80 steps agree to 9e-14).
  - Positive control: at R = |c0| + 0.03 = 2.0091 exactly one sector lights up, sector 42, which contains arg c0
    (mismatch 1.08e-2, the same at 40 and 80 steps). c1 (|q2| = 1.09, on the negative real axis) is inside both radii and
    lights nothing, which confirms it is off the sheet.
  - So c0 (with its mirror) is the only hydro-sheet branch point with |q2| < 2.009 at d=512.

**d = 1024: nearest_in_census = null (unknown).** I ran no finding-stage census.
- The sector test shows no hydro-sheet branch point with |q2| < 1.9369 = |c0| - 0.03 (all 50 sectors trivial, max 6e-14).
  Together with section 2, c0 is on the sheet.
- But the outer positive control at |c0| + 0.03 failed numerically. Rays 35-50 jumped roots beyond |q2| ~ 1.94, giving
  O(1) mismatches that do not converge between step counts. So the annulus 1.937 < |q2| < 1.967 is not certified.
- axis.py shows the failure is numerical. On the negative real axis the hydro root continues smoothly to |q2| = 2.0 with
  steps 0.001 and 0.002 (jump ratio at most 4e-5, residual 1e-16), but the next root is only about 0.0027 away. That is
  near alpha = w^2 - sig ~ 1/4, where the far-zone exponents merge.
- Closing the gap needs a fine-step rerun of about 45 min, which is over the 20-minute cap, so I left it.

## Surprises
1. **The multi-radius swap is clean at d = 8192.** Earlier tests looked "UNCLEAR" only because the partner-finder picked a
   crowded neighbouring root, not because of anything at c0.
2. **Roots crowd hard near (qfr^2, wfr) ~ (-2, i) at large d.** The neighbour spacing is about 0.0027 in wfr at d=1024.
   Any continuation with steps of about 0.01 in q2 silently jumps roots there. Step counts must grow with d.
3. **The local square root is lopsided.** Both pair members sit about 1.3e-3 (w units) from w* at r=0.005, d=8192, yet
   they are only 8.2e-4 apart. A linear drift of the pair dominates the split, so mirror-guess partner finders are
   unreliable.

## Mistakes, kept visible
- mono5's first d=8192 run went NaN on the circle and saved nothing, so I added checkpoints.
- The second mono5 run exposed the 4-step radial bug. I did not rerun it; mono6 reused the stored pair.
- The first sector.py runs at d=512 and d=1024 crashed on NaN from root-jumped rays. I fixed this with a finer radial step
  (0.01), a NaN guard and dead-ray tracking.

## Files (all in this folder)
- RESULT.json
- Monodromy: mono3m_1024.json/.log, mono3m_8192.json/.log, mono5_1024.json/.log, mono5_8192.log, mono5_8192_stage.npz,
  mono6_8192.json/.log
- Sector census: sector_512.json/.log, sector_512_rays.npz, sector_1024.json/.log, sector_1024_rays.npz
- Other checks: axis_1024.json, locate_1024.json
- Scripts: mono5.py, mono6.py, sector.py, axis.py, locate.py, irr.py, digits.py, make_result.py, mk_mpts.py
- Points files: mpts_1024.json, mpts_8192.json
