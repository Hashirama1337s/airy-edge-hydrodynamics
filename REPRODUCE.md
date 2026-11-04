# Reproducing the headline numbers

Requirements: Python 3 (tested with 3.11.9), mpmath (1.3.0), numpy (2.4.4) and gmpy2 (2.3.1); scipy (1.17.1) only for code/rc3/.
Run every command from the top folder of this deposit (the folder that holds paper.md), except the two commands of Section 7, which
say where to run them. Create the output folder first: `mkdir out`. The scripts read data/ and write only to out/. Run times are
those of our check run and will vary.

| Section | Command | Run time | What it checks |
|---|---|---|---|
| 1 | `python code/airy_constants.py` | 2 s | U1-U3, T1, A, B, A = 2iB, leading-law misses (paper s.3.1, s.4.3) |
| 2 | `python code/table4.py` | 1.5 min | d = 4 control and Table 4 (s.6) |
| 2 | `python code/down.py 4 3 0.0625 out/down_4to3.jsonl` | 42 s | continuation of c0 from d = 4 to d = 3 |
| 3 | `python code/inner.py`, `python code/ntaylor.py`, `python code/ntaylor_hi.py` | 1-4 s each | inputs of the matched model |
| 3 | `python code/critmodel.py bessel2 256 512 1024 2048 4096` | 2 s | model A against the tracked points |
| 3 | `python code/asym.py` | 40 s | model A at d = 2^8..2^27 and its expansion |
| 3 | `python code/predict_THEORY.py` | 1 s | regenerates the sealed BAR-THEORY prediction file |
| 4 | `python code/verdict_DYN1.py`, `python code/predict_DYN1b.py`, `python code/backtest_and_rival.py`, `python code/verdict_DYN1b.py`, `python code/p6_check.py`, `python code/verdict_THEORY_amended.py`, `python code/verdict_THEORY.py` | seconds | forward tests (s.4) |
| 5 | `python code/rc_v2.py 512 ...`, `python code/rc_v1.py 1024 ...`, `python code/rc.py 8192 ...` (full arguments below), `python code/make_result_RC.py`, `python code/verdict_RC.py` | 3.5, 3.5, 6 min; seconds | monodromy census (s.5.1) |
| 6 | `python code/verdict_RC2_fix1.py`, `python code/verdict_RC3.py`, `python code/verdict_RC3R.py`, `python code/rc3_pairs.py` | seconds | coefficient route (s.5.2-5.4) |
| 7 | `python ../../code/rc3/fitdata2.py 8192 d8192_r192,d8192_r185` (and 2048), `python ../../code/rc3/spc.py 30 200 1.97 2.92` | 8.5 min (d = 8192), 3.5 min (d = 2048); 45 s | ladder fits and synthetic control of BAR-RC3 |
| 8 | `python code/verdict_DYN2.py`, `python code/verdict_DYN3.py` | seconds | pole tests (Appendix B) |

## 1. Airy constants

`python code/airy_constants.py` finds the first three zeros of W(U) = Ai'(U)^2 - U Ai(U)^2 with Im U > 0, forms T1, A and B, and
compares the leading law with the blind values. Output:

```
U1 = (-2.79029838585 + 1.09430961928j)   |W(U)| = 3.9e-31   |W'(U) + Ai(U)^2| = 2.8e-31
U2 = (-4.45744508148 + 1.02650548702j)   |W(U)| = 1.6e-30   |W'(U) + Ai(U)^2| = 2.0e-31
U3 = (-5.84624217011 + 0.979173782173j)   |W(U)| = 3.3e-30   |W'(U) + Ai(U)^2| = 2.5e-31
T1 = (-0.321646873634 - 1.70110408182j)
|U1 - T1^2| = 2.2e-31   (U = T^2 at a zero: no d^(-2/3) term)
A  = (1.02116517114 + 5.40066881796j)
B  = (2.70033440898 - 0.510582585569j)
|A - 2iB| = 0.0
d =  8192  leading-law miss |q2 + 2 - A d^(-1/3)| = 0.0013615
d = 16384  leading-law miss |q2 + 2 - A d^(-1/3)| = 0.00067005
d = 32768  leading-law miss |q2 + 2 - A d^(-1/3)| = 0.00033089
```

## 2. The d = 4 control, Table 4 and the continuation to d = 3

`python code/table4.py` refines c0 at 110 bits (Newton on the double root of the spectral function in code/qnmx.py). At d = 4 the seed
is the published 8-digit point; at the other d it is the double-precision point of the deposited track. The last column compares with
the deposited 150-bit values (the d = 4..4096 references in data/DYN1/RESULT.json hold 28 digits). Output:

```
d = 4 control: q2 = 1.8906468611525056775029810025887466+1.171150523650781022093714965971656j, wfr = 1.4436414084084321217424815916876428-1.0692249775975828413001263920642459j
  published (8 digits): q2 = 1.8906469 + 1.1711505i, wfr = 1.4436414 - 1.0692250i; max |diff| = 4.5e-08 (rounding < 5e-8)
  |q2| = 2.223992   (10 s)

Table 4 (q2 = qfr^2 of c0; diff = |110-bit value - deposited 150-bit value|):
d =     3  c0 = 1.72504779140660331294 + 0.340135868692161570039i   |c0| = 1.75826   diff = 1.4e-32   (9 s)
d =     4  c0 = 1.8906468611525056775 + 1.17115052365078102209i   |c0| = 2.22399   diff = 4.1e-28   (0 s)
d =   512  c0 = -1.85434196376243291296 + 0.691670108025656048947i   |c0| = 1.97914   diff = 2.2e-28   (10 s)
d =  1024  c0 = -1.89017211961140767381 + 0.543941610339312055025i   |c0| = 1.96688   diff = 1.4e-28   (10 s)
d =  2048  c0 = -1.91549818518955930752 + 0.42924741091280704365i   |c0| = 1.96300   diff = 2.4e-28   (10 s)
d =  8192  c0 = -1.94836923521368989578 + 0.268857905752112862699i   |c0| = 1.96683   diff = 4.8e-30   (11 s)
d = 16384  c0 = -1.95931350079439501531 + 0.213104859859562672017i   |c0| = 1.97087   diff = 5.0e-30   (12 s)
d = 32768  c0 = -1.96785054944873001007 + 0.169000734875074579919i   |c0| = 1.97509   diff = 3.4e-30   (15 s)
```

`python code/down.py 4 3 0.0625 out/down_4to3.jsonl` continues c0 from the published d = 4 point down to d = 3 in double precision,
with a half-step jump check at every step. out/down_4to3.jsonl is byte-identical to data/c0down/down_h16.jsonl; its last line is

```
{"d": 3.0, "q2": [1.7250477914065803, 0.34013586869216444], "w": [0.9247135585960974, -1.5242692698192817], "it": 4, ...}
```

The full continuation from d = 4 to d = 32768 (code/track.py, records in data/DYN1/track_c0.jsonl and data/DYN1b/track_c0b.jsonl) and
the 150-bit refinements (code/refine.py, setting B) were not re-run for this check; each refinement takes about 40-50 s per d.

## 3. The matched model A and the sealed BAR-THEORY predictions

```
python code/inner.py
python code/ntaylor.py
python code/ntaylor_hi.py
python code/critmodel.py bessel2 256 512 1024 2048 4096
python code/asym.py
python code/predict_THEORY.py
```

These regenerate out/inner_basics.json, out/ntaylor.json, out/ntaylor_hi.json, out/crit_bessel2.json, out/asym.json and
out/PRED-THEORY.json. Each is byte-identical to the deposited file of the same name in data/theory/. out/PRED-THEORY.json is also
byte-identical to data/theory/PRED-THEORY.json, the sealed prediction file of BAR-THEORY (SHA-256 ab758de0cd198091...; see
SEALS/HASHES.md). predict_THEORY.py prints, for example,

```
8192 {"A_model_parameter_free": {"q2": ["-1.948375023955166", "0.2688636316470298"], "w": ["0.1344073931451793", "0.9744426413946956"], "bar_q2": "1.6e-5", "bar_w": "8.3e-6"}, ...
```

predict_THEORY.py reads data/theory/asym.json; to chain it to your own run, compare out/asym.json with that file first (they are
identical in our run).

## 4. Forward tests

`python code/verdict_DYN1.py`:

```
C1 HOLDS (1.8906468611525056+1.171150523650781j) (1.4436414084084321-1.0692249775975828j)
P1 FAILED
limit ('q2', 'A') (-1.9908568566797986+0.006845147808727186j)
limit ('q2', 'B') (-1.9792967726546251+0.10530183671762892j)
limit ('w', 'A') (0.003011437284268836+0.9976268862139376j)
limit ('w', 'B') (0.05261937189329562+0.9898115022875627j)
P2 FAILED (partial: one family within 0.05-0.1) dist A 0.011421607518080185 dist B 0.10731775453586635 family diff 0.0991330173734933
P3 HOLDS exponent 0.33928518539629
P4 HOLDS
N1 HOLDS 1.0012094174537705
```

`python code/predict_DYN1b.py` and `python code/backtest_and_rival.py` regenerate out/PRED-DYN1b.json and out/PRED-DYN1b-rivalB.json,
byte-identical to the sealed files data/DYN1b/PRED-DYN1b.json (SHA-256 3e2019abfe7f1692...) and data/DYN1b/PRED-DYN1b-rivalB.json
(d588ee201a146129...). The backtest prints

```
BACKTEST (predict known d=4096):
  q2: pred -1.93430726+0.33952912j true -1.93418920+0.33948314j |err| 1.267e-04 recipe bar 2.194e-03 covered True
  w: pred 0.16969030+0.96765209j true 0.16968321+0.96761264j |err| 4.008e-05 recipe bar 7.119e-04 covered True
```

`python code/verdict_DYN1b.py` (the long P5 line, which lists the census points, is shortened here):

```
P1 d=8192 HOLDS |dq2| 4.236e-05 (bar 9.73e-04) |dw| 1.333e-05 (bar 3.19e-04)
P2 d=16384 HOLDS |dq2| 1.381e-04 (bar 2.84e-03) |dw| 4.338e-05 (bar 9.33e-04)
P3 d=32768 HOLDS |dq2| 2.758e-04 (bar 5.26e-03) |dw| 8.651e-05 (bar 1.73e-03)
P4 HOLDS {'q2': np.complex128(-2.0005500942474788-3.36679881914469e-05j), 'w': np.complex128(-1.5410433736792552e-05+1.0001684763449803j)}
P5 FAILED {'512': {'nearest_in_census': True, ... '1024': {'nearest_in_census': None, ...}}
```

`python code/p6_check.py` (P6 was added by the sealed amendment, SEALS/DYN1b/AMENDMENT-DYN1b.md item 2, and was scored by this
separate comparison; the same three lines end SEALS/DYN1b/DYN1b_verdict-DYN1b.txt):

```
q2 |x-A| 0.0002757570444933946 |x-B| 0.010952847655446706
w |x-A| 8.651135331527989e-05 |x-B| 0.005464533672405009
P6 HOLDS
```

`python code/verdict_THEORY_amended.py` (the scorer the test was scored with; `python code/verdict_THEORY.py`, the original, prints the
same T1-T3 and T5 lines and T4 without the T4' line):

```
T1 d=8192 |dq2| 8.14e-06 (bar 1.6e-5) |dw| 4.15e-06 (bar 8.3e-6) -> ok
T1 d=16384 |dq2| 2.58e-06 (bar 5.1e-6) |dw| 1.31e-06 (bar 2.6e-6) -> ok
T1 d=32768 |dq2| 8.19e-07 (bar 1.6e-6) |dw| 4.15e-07 (bar 8.2e-7) -> ok
T2 d=8192 |dq2| 9.65e-08 (bar 5.0e-6) |dw| 4.98e-08 (bar 1.2e-6) -> ok
T2 d=16384 |dq2| 4.49e-08 (bar 2.0e-6) |dw| 2.37e-08 (bar 4.8e-7) -> ok
T2 d=32768 |dq2| 1.84e-08 (bar 7.4e-7) |dw| 9.91e-09 (bar 1.8e-7) -> ok
T3 exponent 1.0204121835104674 HOLDS
T4 (as sealed, mis-set) {8192: 0.10759861222985442, 16384: 0.08610852606897454, 32768: 0.06879617219546151} FAILED
T4prime HOLDS
T5 HOLDS
{'T1': 'HOLDS', 'T2': 'HOLDS', 'T3': 'HOLDS', 'T4': 'FAILED', 'T4prime': 'HOLDS', 'T5': 'HOLDS'}
```

The printed verdicts match the sealed verdict text files in SEALS/ line for line (the out/*.json files are convenience copies; no reference copies are deposited).

## 5. Monodromy census (BAR-RC)

```
python code/rc_v2.py 512 1.9791391201496016 2.7845762968724563 0.005 48 40 1e-06 out/rc_512.json
python code/rc_v1.py 1024 1.9668815717309482 2.8613901499233068 0.005 50 40 1e-06 out/rc_1024.json
python code/rc.py 8192 1.9668317798461032 3.0044673886944393 0.002 50 40 1e-06 out/rc_8192.json
python code/make_result_RC.py
python code/verdict_RC.py
```

Arguments: d, |c0|, arg c0, dr, number of sectors K, arc steps n, tolerance. The three code versions (v1 at d = 1024, v2 at d = 512,
v3 = rc.py at d = 8192) are the ones used in the test; they differ only in the detector for sudden drops in the local root spacing.
The final lines printed by the three censuses are identical to the deposited logs (data/RC/rc_*.log), for example at d = 8192:

```
in R=1.9648317798 max_n=5.51e-14 ... lit_n=[] lit_2n=[] ...
out R=1.9688317798 max_n=1.62e-03 max_2n=1.62e-03 lit_n=[47] lit_2n=[47] >1e-9 n=[47] 2n=[47] c0sec=47 m_c0 n=1.621117e-03 2n=1.621117e-03 other max n=5.05e-14 2n=7.63e-14
done 361s
```

make_result_RC.py collects out/rc_*.json into out/RESULT.json, which is byte-identical to data/RC/RESULT.json (out/RESULT_diag.json
differs from data/RC/RESULT_diag.json only in the wall-clock times). The scorer reads the deposited data/RC/RESULT.json:

```
P1 d=1024: P0 PASS (lit [45], c0 sector 45, c0 mism 7.278e-03/7.278e-03); in max 6.36e-14/7.39e-14; max ray jump 5.756e-04 -> HOLDS
P2 d=512: P0 PASS (lit [42], c0 sector 42, c0 mism 1.065e-02/1.065e-02); in max 6.60e-14/6.00e-14; max ray jump 3.013e-04 -> HOLDS
P3 d=8192: P0 PASS (lit [47], c0 sector 47, c0 mism 1.621e-03/1.621e-03); in max 5.51e-14/9.15e-14; max ray jump 5.294e-03 -> HOLDS
```

## 6. Coefficient route (BAR-RC2, BAR-RC3, BAR-RC3R)

`python code/verdict_RC2_fix1.py`:

```
PC ours 2.22399 GKST 2.224 (GKST arXiv:1904.12862v3, sec. 4.2, eq. (4.20), printed p. 24: q_c^2 ~ 1.8906469 +/- 1.1711505 i, |q_c^shear| ~ 1.49131 (so |q_c^2| = 2.223991 from the printed components); also sec. 4.2 text p. 25: '|q^2_c| ~ 2.224') -> PASS
P1 d=512: relR 1.05e-02 dtheta 4.58e-03 dbeta nan -> FAILED
P2 d=1024: relR 1.68e-02 dtheta 1.14e-02 dbeta nan -> FAILED
```

`python code/verdict_RC3.py`:

```
SPC rel R err 6.471e-06 theta err 8.221e-06 -> PASS
P1 d=2048: R 1.9630256953 vs 1.9630044924 rel 1.08e-05; theta 2.921139648 vs 2.921143 err 3.18e-06 -> HOLDS
P2 d=8192: R 1.9667280547 vs 1.9668317798 rel 5.27e-05; theta 3.0043821896 vs 3.004467 err 8.52e-05 -> HOLDS
```

`python code/verdict_RC3R.py`:

```
C_in FAIL 1.9176e-03
C_out PASS 6.4626e+01 true
P1 VOID 4.0232e-02 true
```

`python code/rc3_pairs.py` lists, for each of the ten ladder fits, the reported pair (largest contribution), the nearest significant
pair and any weaker pair inside |c0|. Summary lines (the per-fit lines are omitted here):

```
d = 2048, |c0| = 1.9630044924, arg c0 = 2.9211428
  fits with a weaker pair inside |c0|: 3 of 10 (R from 1.904 to 1.959)
  fits whose reported pair breaks the 5e-3 angle line: 0 of 10
d = 8192, |c0| = 1.9668317798, arg c0 = 3.0044674
  d8192_r192_30_200  K=4 reported R=1.9667281 rel 5.27e-05 angle 8.52e-05 | nearest R=1.95119 rel 7.95e-03 | weaker pairs inside |c0|: 1.95119, 1.96444
  fits with a weaker pair inside |c0|: 7 of 10 (R from 1.912 to 1.965)
  fits whose reported pair breaks the 5e-3 angle line: 2 of 10
```

## 7. The BAR-RC3 ladder fits and synthetic control (optional, scipy needed)

These scripts read the Cauchy coefficients from the working folder and write their output there, so run them in a copy:

```
mkdir out/rc3
cp data/RC3/cauchy_d*_r1*.json out/rc3/
cd out/rc3
python ../../code/rc3/fitdata2.py 8192 d8192_r192,d8192_r185
python ../../code/rc3/fitdata2.py 2048 d2048_r192,d2048_r185
python ../../code/rc3/spc.py 30 200 1.97 2.92
```

fits_8192.json, fits_2048.json and spc_30_200.json are byte-identical to the deposited files in data/RC3/. The first fit line at
d = 8192 is

```
d8192_r192 30-200 K=4 dominant R=1.9511877367 theta=2.9733519741 | pairs(contrib@n2): (1.95119,2.97335;3.1e-01) (1.96444,2.94409;1.3e-02) (1.96673,3.00438;1.0e+00) (2.17592,2.94611;2.8e-10) | rms 2.5e-04 4.3e-07 1.5e-08 2.0e-11
```

("dominant" in this driver is the nearest significant pair; the result file reports the pair with the largest contribution, here
1.96673.) The synthetic control ends with

```
MAX rel R err 6.471e-06  MAX theta err 8.221e-06
```

The Cauchy coefficients themselves (code/rc3/cauchy3.py with code/rc3/qnm.py) and the third-circle comparison of BAR-RC3R
(code/rc3/compareR.py on the cauchyfull files) were not re-run for this check.

## 8. Pole tests (Appendix B)

`python code/verdict_DYN2.py` prints the 17 cells of Appendix B.1 and ends with `ALL HOLDS H(d=4) HOLDS`; `python code/verdict_DYN3.py`
prints the 16 cells of Appendix B.2 for recipe A (`A ALL HOLDS H(d=4) HOLDS`), the descriptive recipe B, and the descriptive d = 4
large-momentum values. Both printed verdicts match the sealed verdict text files in SEALS/. The solvers
and coefficient builders of the pole tests are not in this deposit.
