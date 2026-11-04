# ADDENDUM-DYN2 - written BEFORE blind/RESULT.json is read (scribe pass 06:45 + lead), 2026-11-03
1. Units (as in PRED-DYN.json / BUILD.md): 2308.01371 conventions, r_h = 1, T = d/(4 pi), qbar = q/sqrt(d), Omega = omega (NOT frak w);
   Im Omega < 0. Scoring normalisation declared now: keys compared as numbers (e.g. "4.0" == "4"); if the blind seat reports magnitudes
   (positive) with an explicit statement that values are |Im Omega| or -Im Omega, the sign is restored before comparison; text values ->
   that cell VOID (not FAILED), and the summary distinguishes VOID from FAILED. No other change.
2. Positive control (declared now, scored descriptively): the blind seat's d = 4, qbar = 1 value vs Kovtun-Starinets -1.196132 i (6 digits;
   frak q^2 = 4 qbar^2/d = qbar^2 at d = 4; Omega = 2 frak w). A units slip shows here first.
3. Freshness: the d = 4, qbar = 1 cell is NOT fresh (builder saw KS's 6 digits and used them to prefer Pade over Borel-Pade, which differ
   by 4.6e-5 there vs bar 9e-8). The other 16 cells are fresh with respect to the builder (no solver run at d < 8; exactd.py asserts d >= 8).
   The lab DID hold earlier exact d = 4 shear solves at complex qbar^2 ~ 0.4 (zeta-k5/shearB/d4control.py) - "no exact pole at d < 8
   existed" is wrong; "the builder ran none" is right.
4. Bar recipe: fixed in conv.py which printed d >= 8 and d < 8 together; unchanged afterwards (convM.json byte-identical to convA.json);
   the honesty test's qbar = 1.5 coverage failures did not change it. Recipe includes an inert Borel-Pade term (rejected in all 33 entries).
5. Wording: "level-crossing branch points" = Pade pole-zero pairs (quadratic-Pade check unstable, dropped) - not established singularities;
   "EST15 floor absent" -> "resummation beats the bare-series floor (the builder's own truncation errors at d = 8, 2.5e-5..4.5e-2, are of the
   size EST15 estimates)"; 2308.01371 l.263 concerns each q^(2j) coefficient's 1/d series (consistent with our mechanism) - the fixed-qbar
   series is a different object, so no contradiction.
