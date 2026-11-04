# BAR-RC - is the Airy critical point c0 the NEAREST hydro-sheet singularity (= radius of convergence of shear hydro)? sealed 2026-11-03 13:20-13:29
Why: REFEREE-DYN-2 single next strike. Turns "a critical point obeys an Airy law" into "the radius of convergence of shear hydrodynamics
obeys an Airy law". DYN1b P5 left the annulus |c0|-0.03 < |q2| < |c0| at d = 1024 uncertified (outer control broke from root crowding).
Object: shear-channel hydro pole of the AdS_{d+1} brane, lab conventions of BAR-DYN1/DYN1b (thermal units, q2 = qfr^2), hydro sheet = radial
continuation of the hydro root from q2 ~ 0. c0 = tracked critical point (DYN1b/blind values; |c0| at 1024 = 1.9668815717309482).
Method: sector-monodromy census (DYN1b/blind/sector.py idea), with steps scaled to the local root spacing; seat may improve the code.

PREDICTIONS (each cell VOID unless its positive control passes - VOID is not HOLD and not FAILED):
P0 (positive control, each d tested): at R_out = |c0| + dr, the sector containing arg c0 lights up (mismatch > 1e-3 in both n and 2n arc runs,
   agreeing to 10%), and NO other upper-half sector lights up. Ray root-jump diagnostic reported for every ray.
P1 (d = 1024, dr = 0.005): at R_in = |c0| - 0.005, all upper-half sectors trivial: max mismatch < 1e-9 in both n and 2n runs.
P2 (d = 512, dr = 0.005): same as P1/P0 at d = 512 (control that the finer protocol reproduces the coarse 512 certificate).
P3 (stretch, d = 8192, dr = 0.002): same as P1/P0. May be reported NOT RUN.
FAIL: any lit sector at R_in with a converged mismatch > 1e-6 (a nearer singularity exists) -> logged FAILED, with its location refined.
Between 1e-9 and 1e-6 or n/2n disagreement: INCONCLUSIVE.
Scoring: lead reads RC/RESULT.json keys {d: {"R_in","R_out","in_max_mismatch_n","in_max_mismatch_2n","out_lit_sectors","sector_of_c0",
"out_mismatch_c0_n","out_mismatch_c0_2n","max_ray_jump"}} and applies the rules above verbatim. Numbers as strings.
