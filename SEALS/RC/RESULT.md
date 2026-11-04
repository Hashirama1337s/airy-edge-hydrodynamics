# RC seat: is c0 the nearest hydro-sheet singularity? (computation only; the lead scores the BAR)

Date 2026-11-03. Folder: <lab>/NEXT-2026-11-03/dynamics/RC/. BAR-RC.md was read and not edited. Its sha256 still
matches SEAL-RC.sha256 (117a0f79...3556) at the end of the work.

## What I opened
- BAR-RC.md and SEAL-RC.sha256.
- From DYN1b/blind/: sector.py, lib.py, qnmx.py (copied here; qnmx.py and lib.py unchanged), sector_512/1024 .json/.log,
  RESULT.md, RESULT.json (head), refine_c0_B.jsonl, track_c0.jsonl (tail), axis.py, axis_1024.json, mpts_*.json.
- I did not open dynamics/soundcrit/ or any memory file.

## Inputs (c0 from DYN1b/blind, not recomputed)
| d | c0 = qfr^2 (source) | abs c0 | arg c0 |
|---|---|---|---|
| 512 | -1.85434196376243291 + 0.69167010802565605 i (refine_c0_B.jsonl, 150 bits) | 1.9791391201496016 | 2.7845762968724563 |
| 1024 | -1.89017211961140767 + 0.54394161033931206 i (refine_c0_B.jsonl) | 1.9668815717309482 (= BAR value) | 2.8613901499233068 |
| 8192 | -1.94836923521368990 + 0.26885790575211286 i (DYN1b RESULT.md table) | 1.9668317798461032 | 3.0044673886944393 |

## Method (rc.py)
The idea is the same as DYN1b's sector.py:
- Follow the hydro root out along K+1 rays at angles 0 to pi, from |q2| = 0.02 to R_in and on to R_out.
- Then follow it along the K short arcs at radius R between neighbouring rays.
- mismatch_k = |arc end - ray value| at the next ray. It is measured in the solver's w units (wfr = 2 w), as in DYN1b.
- Mirror symmetry covers the lower half-plane.

What changed:
1. **Adaptive steps tied to the local root spacing.** Each path takes its own step.
   - The predictor is a polynomial through the last 4 accepted points. It handles unequal steps correctly.
   - A step is accepted only if three things hold. (a) Newton converged: |dw| < 1e-10 within 8 iterations. (b) The
     predictor error is at most min(tol, 0.05 * sp), where sp = |F_w / (F_ww/2)| is the local distance to the nearest
     other root. (c) sp did not suddenly drop by more than 3x (the jump detector).
   - Otherwise the step is halved and redone.
   - The step then grows or shrinks with the error. Fine steps therefore appear only where the roots crowd, near arg c0
     and the negative axis. No hand-placed fine grid was used.
2. **Batching.** All rays (and later all arcs) share one solver call per Newton iteration, which made it about 3x cheaper.
3. **Two independent runs.** Run A uses tol 1e-6 and ray hmax 0.05. Run B uses tol 1e-6/16 and ray hmax 0.025.
   - The "n" arcs (hmax = dtheta/40) start from run A rays. The "2n" arcs (hmax = dtheta/80) start from run B rays.
   - Comparing ray A with ray B at R_in and R_out is a root-jump check that does not rely on the jump detector.
4. **Code versions (disclosed).** All three versions accept a step only on the same Newton and predictor-error test.
   They differ only in the spacing-change detector:
   - v1 (rc_v1.py) rejected any 3x change in sp. Used for d=1024 (rc_1024.json).
   - v1 got stuck at d=512 on a ray at |q2| ~ 0.23, where F_ww crosses zero and sp goes very large. That is harmless.
     So v2 (rc_v2.py) rejects only a 3x drop. Used for d=512 and the extra d=1024 run at dr = 0.001.
   - At d=8192, v2 got stuck at |q2| ~ 0.07 on the real-axis rays. There, sp is noise-dominated (it swings between
     0.03 and 0.7). So v3 (rc.py) applies the drop test only in the crowded regime, sp < 0.02.
   - The two stuck attempts were aborted before any arcs ran and produced no results.

**Probable cause of the old d=1024 failure (from reading sector.py; not proven by a rerun).**
- sector.py's predictor 3W[-1] - 3W[-2] + W[-3] assumes equal steps. Its radial grid changes step at R_in, from 0.00998
  to 0.005.
- So the first step past R_in overshoots by about |dw/drho| * 0.005, roughly 0.235 * 0.005 = 1.2e-3 in w.
- That is about the root spacing on rays 35-50 (sp 1.9e-3 down to 1.3e-3; my ray table).
- This matches the reported jumps "beyond |q2| ~ 1.94", since R_in was 1.937.

## Controls
- **Probe (2-minute rule).** One fine ray at d=1024 on the negative axis (the most crowded) ran to |q2| = 1.97188 in
  57 s with 50 steps, 6 rejections, max jump 2.8e-4 and min spacing 1.33e-3. It ended at w = 0.4879647i.
  - DYN1b's independent axis continuation (axis_1024.json, steps 0.001) gives wfr = 0.97596i at 1.97195, i.e.
    w = 0.48798i.
  - These agree within the 7e-5 difference in radius.
  - Full-run cost estimated from this probe: about 5 min per d. Actual: 5.2, 5.1 and 7.7 min.
- **P0 positive control, every d.** At R_out, exactly one upper-half sector lights up, and it is the sector containing
  arg c0. Its n and 2n mismatches agree to about 1e-13 relative. Every other sector is at 1e-14 to 1e-13.
- **Ray A vs B.** They agree to at most 8.3e-14 at R_in and R_out on every ray at every d, including rays 35-50 at d=1024,
  which DYN1b lost. No ray jumped.
- **n vs 2n arcs.** Arc end points agree to at most 9.4e-14 in all non-c0 sectors and to 2e-16 to 4e-16 in the c0
  sector.
- **Reproduces DYN1b at d=512.** DYN1b's coarse run (dr 0.03) lit only sector 42, with mismatch 1.084e-2. The fine run
  (dr 0.005) lights only sector 42, with 1.0652e-2. The small difference is expected: the arc radius differs.

## Verdict inputs (RESULT.json holds the BAR keys as strings; RESULT_diag.json has the extras)
| d | dr | R_in | R_out | in max mismatch n / 2n | out lit sectors | c0 sector | out mismatch c0 n / 2n | max ray jump |
|---|---|---|---|---|---|---|---|---|
| 512 (K=48) | 0.005 | 1.97413912 | 1.98413912 | 6.6e-14 / 6.0e-14 | [42] | 42 | 1.065220e-2 / 1.065220e-2 | 3.0e-4 |
| 1024 (K=50) | 0.005 | 1.96188157 | 1.97188157 | 6.4e-14 / 7.4e-14 | [45] | 45 | 7.278183e-3 / 7.278183e-3 | 5.8e-4 |
| 8192 (K=50) | 0.002 | 1.96483178 | 1.96883178 | 5.5e-14 / 9.2e-14 | [47] | 47 | 1.621117e-3 / 1.621117e-3 | 5.3e-3 |

Notes on these numbers:
- "Lit" means mismatch > 1e-6. No sector anywhere sits between 1e-13 and 1e-3.
- The max ray jump is |w - w_pred| / sp over accepted steps, the same quantity as DYN1b's "jump". The acceptance rule caps
  it at 0.05 by construction. Every per-ray value is in the rc_<d>.log ray tables.
- Run B ray jumps are 2.0e-5, 4.7e-5 and 3.6e-4 (for 512, 1024, 8192).
- In wfr units every mismatch is 2x the value shown. At d=8192 the c0 mismatch is 1.62e-3 in w units, 3.24e-3 in wfr.

**Extra (not in the BAR).** d=1024 at dr = 0.001, code v2 (rcx_1024_dr0.001.json):
- R_in = 1.96588: max mismatch 6.1e-14 (n) and 8.0e-14 (2n).
- R_out = 1.96788: only sector 45 lit, with 7.319396e-3 in both runs.
- Rays A vs B agree to 8.6e-14 and the max ray jump is 5.3e-4.

## Anything odd
- **No second lit sector at any d, and no nearer singularity.** Nothing other than c0 lights up at R_out, and nothing at
  all lights up at R_in. That rules out any hydro-root branch point (in the upper half plane, or by mirror symmetry the
  lower) with |q2| < |c0| - dr: 0.005 at d = 512 and 1024, 0.002 at d = 8192, and 0.001 at d = 1024 in the extra run.
- **Real-axis rays never come close to a collision.** Their minimum spacing is 1.3e-3 (d=1024) and 1.6e-4 (d=8192), so
  no branch point sits on the boundary rays theta = 0 or pi.
- **Root crowding scales like 1/d.** The minimum over all rays of |F_w/(F_ww/2)| (w units) is:

  | d | min spacing (w units) | d x spacing |
  |---|---|---|
  | 512 | 2.15e-3 | 1.10 |
  | 1024 | 1.13e-3 | 1.15 |
  | 8192 | 1.45e-4 | 1.19 |

  Even the positive real axis crowds at d=8192 (spacing 5.4e-4). The adaptive steps handled this with no change in
  settings: at most 66 accepted steps per ray in run A and 132 per arc.
- **Rejections.** The 509 arc rejections at d=8192 are all start-up halvings, 3 to 7 per arc, on the first step from a
  constant predictor. None came from the jump detector mid-arc.
- **Limits of the method (not tested here).**
  - The annulus |c0| - dr < |q2| < |c0| (shrunk to 0.001 at d=1024).
  - Singularities that leave the hydro root single-valued around a loop, such as a pole of w(q2), or two branch points
    in one sector whose monodromies cancel. K is 48 to 50 sectors, each 0.063 to 0.065 rad.
  - The lower half plane relies on the exact mirror symmetry of the real equation.

## Wall time
- Measured run times: d=1024 310 s; d=512 308 s; d=8192 463 s; extra d=1024 (dr 0.001) 338 s.
- Aborted stuck attempts: d=512 159 s; d=8192 242 s.
- Probe, timing and debugging: about 3 min.
- Total compute about 32 min. At most 2 heavy jobs ran at once. All Python ran under memcap (peak 0.4 GB).

## Files (all here)
- rc.py (v3), rc_v1.py, rc_v2.py, make_result.py, timing.py, plus copies of lib.py, qnmx.py and sector.py.
- rc_512.json/.log, rc_1024.json/.log, rc_8192.json/.log, rcx_1024_dr0.001.json/.log.
- RESULT.json (BAR keys) and RESULT_diag.json (extra diagnostics).
