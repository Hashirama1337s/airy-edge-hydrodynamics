# BAR-DYN3 - sound channel: does the divergent 1/d series predict the propagating sound pole at d = 3..6? (sealed 2026-11-03 before
# any blind exact sound pole at d < 8 is computed)
Predictions: PRED-SOUND.json, "pred" = recipe A (Pade [12/12] in 1/d, recipe hashed 10:36 before coefficients existed), copied here; sha256
of this copy 1e85f6c0... (NOTE: the builder reported b29f041c... for the file - the file on disk at sealing time is what is sealed; the
builder's figure is disclosed as a mismatch, likely a final rewrite after its hash). Builder ran no solver at d < 8 (exact.py refuses d < 8)
except a d = 4 small-q control (qfr <= 0.3).
Object: hydrodynamic sound pole omega_+ (Re > 0) of the planar AdS_{d+1} Schwarzschild brane; r_h = 1, T = d/(4 pi), qbar = q/sqrt(d), Omega = omega.
Scored cells = recipe A "usable" (bar < 1% of |value|): qbar 0.5 at d = 3, 3.5, 4, 4.5, 5, 6; qbar 1.0 at d = 3, 3.5, 4, 4.5, 5, 6; qbar 1.5 at
d = 4.5, 5, 6; qbar 3 at d = 6 (16 cells). Non-fresh: (qbar 1, d 4) - builder read Kovtun-Starinets' d = 4, qfr = 1 value 4 min after recipe A
was hashed (recipe unchanged). Unusable cells (incl. d = 4 at qfr = 3, 5) carry no claim.
Predictions (verdict_DYN3.py, hashed now): P(cell): |blind Omega - pred Omega| <= 3 x bar (complex distance; bar as in PRED-SOUND.json).
HOLDS iff all 16. Headline H: all usable d = 4 cells hold. Text value -> VOID cell (VOID distinguished from FAILED).
Descriptive: recipe B ("pred_B") scored the same way; d = 4 qfr = 3, 5 blind values recorded (for the 1502.02820 sentence: does
Re omega/q -> 1 and |Im omega| fall at large momentum at d = 4?).
