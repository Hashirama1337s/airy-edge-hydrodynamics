# AMENDMENT-THEORY - written BEFORE DYN1b/blind/RESULT.json is read (scribe pass 10:45), 2026-11-03
1. T4 as sealed ("|X d/4 - 1| < 0.05 at d = 32768") is mis-set: the theory's OWN models give |X d/4 - 1| = 0.110, 0.087, 0.069 at
   d = 8192, 16384, 32768 (X = (qfr^2+2) - 2i(wfr - i)), so a correct law would fail it. Replaced by T4': |X d/4 - 1| decreases
   monotonically over 8192 -> 16384 -> 32768 AND its value at 32768 is within 0.01 of the model-A value 0.069. Original T4 is reported
   as printed (expected FAILED by construction) and marked mis-set.
2. Independence: "PRED-THEORY written before any d >= 8192 data" is the theory seat's self-report; DYN1b/blind/pts_8192/16384/32768.json
   existed from 07:23 (the seat was forbidden from DYN1b/; its scripts reference only DYN1/blind/RESULT.json). THEORY-DYN.md (10:14) is
   not covered by the 10:06 seal. Model A was shaped while watching d <= 4096 residuals and its bars come from the d = 4096 residual -> the
   2.6e-5 at d = 4096 is a check, not a test. Only d >= 8192 counts as out-of-sample.
3. Wording: "derived by formal matched asymptotics; leading terms re-computed by the referee; sub-leading (t3, -zeta(3) slope) numerically
   identified".
