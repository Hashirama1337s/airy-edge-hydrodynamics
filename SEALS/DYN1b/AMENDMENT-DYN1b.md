# AMENDMENT-DYN1b - written BEFORE blind/RESULT.json exists (scribe pass 07:50 + lead), 2026-11-03
1. Backtest of the sealed recipe on KNOWN data (backtest_and_rival.txt): fit on d = 256..2048 predicts the known d = 4096 point to
   |err| 1.3e-4 (q2), 4.0e-5 (w); recipe bars 2.2e-3, 7.1e-4 -> covered, bars ~17x loose there. The bar is a 3-vs-4-parameter
   sensitivity, not an error estimate; exponent drift is not in it.
2. Rival family B (d^-1/2 ladder, 4 params on 512..4096) sealed now (PRED-DYN1b-rivalB.json): q2 at 8192/16384/32768 =
   -1.94808+0.27042i / -1.95833+0.21836i / -1.96583+0.17977i; w = 0.13519+0.97429i / 0.10916+0.97929i / 0.08987+0.98298i;
   its limit (-1.985+0.080i, 0.040+0.992i).
   New discriminating item P6: at d = 32768 (where A and B differ by ~1.1e-2 in q2, ~6e-3 in w) the blind value is closer to the
   family-A prediction than to family B in BOTH q2 and w. (At 8192 the families differ by only ~1.6e-3, below discrimination.)
3. Limitations restated: the exponent family, term count and window were chosen after DYN1's data; the limit is a fit parameter, so a pass
   supports but does not prove "limit = (-2, i)"; P4 follows nearly automatically from P1-P3; P5 re-tests only d = 512, 1024.
4. on_sheet concern (closure/separation 1.0, 0.99, 0.46, 0.22, 0.12 from d = 256 to 4096): the blind seat was asked (after launch, no
   prediction content) to repeat monodromy at several radii/step counts at d = 1024, 4096 and the new d. Any "radius of hydrodynamics"
   wording waits for that.
5. Wording: "Airy-type 1/3" -> "local exponent near 1/3, still drifting (0.358, 0.349, 0.343, 0.340 over d = 256..4096)". The DYN1 scorer's
   printed reason for P2 ("one family within 0.05-0.1") is mislabelled: family A was at 0.011, family B at 0.107; FAILED stands.
