# The Airy edge of shear hydrodynamics: a large-d law for the critical point of the AdS_{d+1} black brane, with a numerical radius bound at d = 512, 1024 and 8192

Moki & Julio (AI-assisted)

This repository will hold the preprint (paper.md), the data, the code that regenerates the headline numbers, and the sealed-test
records for Paper II. It is archived at Zenodo from release v1.0 of https://github.com/Hashirama1337s/airy-edge-hydrodynamics (the DOI is
listed on that page). Companion paper (Paper I): doi:10.5281/zenodo.23940227.

## In plain words

A hot plasma of the kind studied with holography (a black brane in anti-de Sitter space) behaves like a fluid at long wavelengths.
The fluid description is a series in powers of the wavenumber, and like many series it only converges up to some size. Past that
size the series stops working. Where it stops is set by a point where the slow fluid mode collides with one of the fast modes. At
four dimensions that point was found in 2019.

We followed the same point from three dimensions up to 32768 dimensions. As the number of dimensions d grows, it creeps towards a
fixed point, at a rate of one over the cube root of d. The coefficient of that approach is set by the first complex zero of a simple
combination of Airy functions, Ai'^2 - U Ai^2. The formula was derived from the equations, without fitting, but by an approximation
method that gives no error bounds.

We then tested it. A model built from the derivation predicted where the point sits at d = 8192, 16384 and 32768, and the computed
values agreed to within 0.000008 at d = 8192, shrinking to 0.0000008 at d = 32768 (in a quantity of size about 2). The model's form
had been tuned while looking at d up to 4096, and the computed answers were already on disk when the predictions were written, so
this test rests on the theory seat's word that it did not look. The leading term of the formula alone is off by 0.0014 at d = 8192.

We also checked that this point really is the nearest obstacle, which is what makes it set the size limit. At d = 512, 1024 and 8192
a map of the complex plane showed nothing closer (up to a thin band and two kinds of feature the map cannot see). A second solver
family, with exponent and fit model supplied in advance, was consistent at d = 2048. At d = 8192 that second method was ambiguous, and an attempt to settle it was itself badly
designed, so it counts as void.

The fixed point the edge creeps towards is also where a known "pole-skipping" point of the sound channel ends up at infinite d. The
two points meet only in that limit, and at different speeds. A 2019 paper concluded from two other examples that pole skipping is
not directly related to where the fluid series stops. We do not claim a link; we flag the coincidence as an open question.

Below the edge, the same kind of 1/d series predicted how the plasma diffuses momentum and carries sound at 3 to 6 dimensions, within
the error bars written down beforehand, in every one of 33 sealed cells.

Every scored prediction was written down and hashed before the answer was read, except where the scorecards below flag otherwise.
Some predictions failed; they are listed as failures.

## Scorecard

HOLDS means the prediction passed the bar written before the data; FAILED and VOID are reported as such. Errors are absolute in
qfr^2 for the critical point and relative for the poles.

### The law and its forward tests

| Test | Prediction (short) | Verdict | Realised numbers / disclosure |
|---|---|---|---|
| BAR-DYN1 C1 | d = 4 control | HOLDS | all 8 published digits; published value was the Newton seed |
| BAR-DYN1 P1 | census at every d | FAILED | census only at d = 256 |
| BAR-DYN1 P2 | limit within 0.05 of (-2, i), two fit families | FAILED | 0.011 and 0.107 |
| BAR-DYN1 P3, P4 | approach exponent; \|q2\| < 2 by d = 1024 | HOLD | 0.339; 1.967 |
| BAR-DYN1 N1 | null | HOLDS (cannot fail) | - |
| BAR-DYN1b P1-P4 | fit predictions at d = 8192, 16384, 32768; refit limit | HOLD | 4.2e-5 .. 2.8e-4, about 20x inside bars |
| BAR-DYN1b P5 | census at d = 512, 1024 | FAILED | d = 1024 annulus uncertified |
| BAR-DYN1b P6 | closer to d^(-1/3) family than rival | HOLDS | sealed after blind values were on disk |
| BAR-THEORY T1 | parameter-free model A | HOLDS | 8.1e-6 .. 8.2e-7; independence by self-report; form shaped on d <= 4096 |
| BAR-THEORY T2, T3, T5 | calibrated model; residual exponent; on-sheet branch point | HOLD | 9.7e-8 .. 1.8e-8; 1.02; swap at 8192 |
| BAR-THEORY T4 / T4' | 4/d relation within 0.05 / monotone, near 0.069 | FAILED (mis-set before data) / HOLDS | 0.0688 at d = 32768 |

### The radius

| Test | Prediction (short) | Verdict | Realised numbers / disclosure |
|---|---|---|---|
| BAR-RC P0 | positive control just outside c0 | PASS at all d | 8192 margin 1.6x |
| BAR-RC P1-P3 | nothing inside \|c0\| - dr at d = 1024, 512, 8192 | HOLD | <= 9.2e-14; scorer written after data; three code versions |
| BAR-RC2 P1, P2 | free-exponent radius = \|c0\| to 1% | FAILED | 1.05e-2, 1.68e-2 |
| BAR-RC3 SPC, P1 | synthetic control; radius at d = 2048 | PASS; HOLDS | 6.5e-6; 1.1e-5; exponent and model supplied |
| BAR-RC3 P2 | radius at d = 8192 | HOLDS as printed; nearest-pair reading FAILED | 5.3e-5 reported pair; 7.95e-3 nearest pair |
| BAR-RC3R | third-circle check at d = 8192 | VOID (inner control FAILED) | bar ignored aliasing; descriptive reading post hoc |

### Below the edge (appendix)

| Test | Prediction (short) | Verdict | Realised numbers / disclosure |
|---|---|---|---|
| BAR-DYN2 | shear diffusion pole, 17 cells at d = 3..6 | 17/17 HOLD | 16 fresh; 2.2-17 digits; independence medium |
| BAR-DYN3 | sound pole, 16 cells at d = 3..6 | 16/16 HOLD | 15 fresh + 1 control; all within 1 x bar |
| BAR-SHEAR P1, P2 | two shear coefficients vs published estimates | HOLD | closed forms identified (descriptive) |
| BAR-SHEAR C1 | controls | printed FAILED/INCOMPLETE | scorer key bug |

The disclosures behind each row are stated next to each test in the paper (Sections 4-5, Appendices B-D).

## Release contents

- paper.md: the preprint.
- data/: the blind tracked critical points (d = 4..32768, the d = 3 continuation and the high-precision refinements); the theory
  seat's model files and predictions; the monodromy-census results at d = 512, 1024 and 8192; the Cauchy coefficients, ladder fits and
  results of the coefficient route (RC2, RC3, RC3R); the predictions and blind poles of the two pole tests. data/REDACTED.md lists the
  data files changed by redaction.
- code/: the critical-point solver (qnmx.py, lib.py), continuation and refinement drivers (track.py, down.py, refine.py); the
  theory seat's model-A generator (inner.py, ntaylor*.py, critmodel.py, asym.py, predict_THEORY.py); the census code (rc*.py,
  sector.py, make_result_RC.py); the predictors and scorers of every sealed test; code/rc3/ with the coefficient-route seat's
  scripts; and three scripts written for this deposit: airy_constants.py, table4.py and rc3_pairs.py. Lab scripts are copies in which
  only file paths were changed.
- SEALS/: for each sealed test, the files listed in its seal, the seal files, and SEALS/HASHES.md (sealed hash, whether the lab
  original still matches, hash of the deposited copy, redacted or not).
- REPRODUCE.md: commands, captured outputs and run times. MANIFEST.sha256: hashes of all files.
- LICENSE (CC BY 4.0, everything except code/), LICENSE-CODE (MIT, code/), CITATION.cff, .zenodo.json.
