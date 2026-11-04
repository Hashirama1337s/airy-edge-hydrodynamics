# ADDENDUM-DYN3 - written BEFORE blind/RESULT.json is read (scribe pass 13:00-13:09), 2026-11-03
1. Hash mismatch explained: the builder's b29f041c is the LF-normalised hash of the same file; the CRLF bytes on disk hash to 1e85f6c0
   (sealed). BAR-DYN3.md's "likely a final rewrite" is wrong - it is line endings. The sealed copy is the final builder output
   (sound/PRED-SOUND.json 12:29:02); seal 12:31:23 precedes the first blind file 12:39:55.
2. Recipe timing: RECIPE.md (10:36:38) was hashed after run A started (about 10:30) and before coefficient aggregation (coefM.json 10:53:48) -
   "hashed before the coefficients were aggregated", not "before coefficients existed". Recipe B (L = 16) was chosen after A's validation
   -> B is descriptive only, and B cells it marks unusable are not counted.
3. (qbar 1, d 4) is a CONTROL, not a test: the builder read KS's value (about 10:40) before its prediction block existed (>= 10:53, after an
   ana.py fix at 10:53:45 - whether the bug was found by comparing with KS is to be asked), and the blind brief was given the same number.
   The d = 4 headline rests on one fresh cell (qbar 0.5); H is reported with that caveat.
4. Reporting: in addition to the sealed 3 x bar verdict, print each cell's error at 1 x bar and as relative error (descriptive). Bars were
   validated only at d >= 8.5 (err/bar 0.04-0.45) and are carried to d = 3..6; 3 x bar is a ~2-3% relative pass level for qbar >= 1 - only the
   qbar 0.5 cells are sharp.
5. Wording: Catalan / closed form qbar sqrt(1 + 2 qbar^2/d) "extends a 4-term pattern already printed in 1502.02820 (Rescbb, l.476-490) to
   m = 32" (prior art on the closed form at k ~ n scaling unchecked); keep "1502.02820 l.624-625 undecided at d = 4"; drop "wrong as a
   mechanism at d >= 8.5".
