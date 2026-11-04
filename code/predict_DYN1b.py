# BAR-DYN1b predictions: fix the exponent family to d^-1/3 (selected post hoc by BAR-DYN1 P3: local exponent 0.339) and extrapolate the
# shear hydro critical point c0 from the blind DYN1 data at d = 512..4096 to d = 8192, 16384, 32768. Model: X(d) = L + a d^-1/3 + b d^-2/3 + c d^-1
# (4 points, 4 params -> exact; plus a 3-param variant on 1024..4096 for the bar). Bar = |4-param - 3-param| prediction difference, x3.
import json, numpy as np
R = json.load(open("data/DYN1/RESULT.json"))["track"]
cz = lambda v: complex(float(v[0]), float(v[1]))
def fit(var, ds, ncols):
    A = np.array([[d**(-k/3) for k in range(ncols)] for d in ds], dtype=complex); y = np.array([cz(R[str(d)][var]) for d in ds])
    return np.linalg.lstsq(A, y, rcond=None)[0]
out = {}
for var in ("q2", "w"):
    c4 = fit(var, [512, 1024, 2048, 4096], 4); c3 = fit(var, [1024, 2048, 4096], 3)
    out[var] = {"limit4": [c4[0].real, c4[0].imag], "limit3": [c3[0].real, c3[0].imag]}
    for d in (8192, 16384, 32768):
        p4 = sum(c4[k] * d**(-k/3) for k in range(4)); p3 = sum(c3[k] * d**(-k/3) for k in range(3))
        out[var][str(d)] = {"pred": [p4.real, p4.imag], "bar": 3 * abs(p4 - p3)}
print(json.dumps(out, indent=1)); json.dump(out, open("out/PRED-DYN1b.json", "w"), indent=1)
