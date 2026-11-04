# BAR-SHEAR - exact large-d shear-channel coefficients c_{5,3}, c_{5,4} (sealed 2026-11-02 before the seat starts)

## In plain words
A 2023 paper (Grozdanov-Lemut-Pedraza, arXiv:2308.01371) expanded the shear "sound" of a strongly coupled plasma (the AdS black
brane) in 1/d. It computed one coefficient, c_{5,3}, two ways and got -15.814 and -15.502 (x 16 zeta5), 2% apart, and could not
rule out c_{5,3} = c_{5,4}. Our engine (high-precision eigenvalues at large d, fit, guarded identification) should settle both.

## Object (conventions of 2308.01371, eqs. near l.182-260 of PSD_v2.tex)
omega = -i qbar^2 - i sum_{m>=2} d^-m sum_j c_{m,j} qbar^(2j) for the shear channel of the AdS_{d+1} Schwarzschild black brane.
Published exact: c_{m,2} = (-1)^m 2^(m-1) zeta(m); c_{m,m} = c_{m,2}; c_{4,2} = 8 zeta4, c_{4,3} = 7 x 8 zeta4, c_{4,4} = 8 zeta4.
Published estimates: c_{5,3} ~ -15.814 x 16 zeta5 (integral), ~ -15.502 x 16 zeta5 (pole-skipping Pade); c_{5,4} ~ -15.548 x 16 zeta5.

## Predictions (scored by the lead from shear/RESULT.json; FAILED is a result)
- C1 (control): the seat's pipeline reproduces c_{m,2} for m = 2..6 and c_{4,3}, c_{4,4} to >= 30 digits.
- P1: c_{5,3}/(16 zeta5) lies in [-16.13, -15.19] (within 2% of at least one published estimate).
- P2: c_{5,4}/(16 zeta5) lies in [-16.01, -15.08] (within 3% of -15.548).
## Descriptive (reported, not scored)
Whether c_{5,3} = c_{5,4} (difference and digits); exact identification of c_{5,3}, c_{5,4} (guarded PSLQ, holdout + null);
c_{6,3}, c_{6,4}, c_{6,5}; the mirror-symmetry question.
