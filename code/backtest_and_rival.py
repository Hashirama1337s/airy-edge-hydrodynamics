# (1) BACKTEST of the sealed DYN1b recipe on KNOWN data: fit on d = 256..2048 (4-param d^-1/3) and 512..2048 (3-param), predict d = 4096,
#     compare with the blind DYN1 value and the recipe's bar. (2) RIVAL family B (d^-1/2 ladder: L + a d^-1/2 + b d^-1 + c d^-3/2) predictions
#     at d = 8192, 16384, 32768 from d = 512..4096 - sealed as AMENDMENT-DYN1b before blind values are read.
import json, numpy as np
R = json.load(open("data/DYN1/RESULT.json"))["track"]
cz = lambda v: complex(float(v[0]), float(v[1]))
def fitpred(var, ds, ncols, step, dpred):
    A = np.array([[d**(-k*step) for k in range(ncols)] for d in ds], dtype=complex); y = np.array([cz(R[str(d)][var]) for d in ds])
    c = np.linalg.lstsq(A, y, rcond=None)[0]; return sum(c[k] * dpred**(-k*step) for k in range(ncols)), c[0]
print("BACKTEST (predict known d=4096):")
for var in ("q2", "w"):
    p4, _ = fitpred(var, [256, 512, 1024, 2048], 4, 1/3, 4096); p3, _ = fitpred(var, [512, 1024, 2048], 3, 1/3, 4096)
    true = cz(R["4096"][var]); bar = 3 * abs(p4 - p3)
    print(f"  {var}: pred {p4:.8f} true {true:.8f} |err| {abs(p4-true):.3e} recipe bar {bar:.3e} covered {abs(p4-true) <= bar}")
rival = {}
for var in ("q2", "w"):
    rival[var] = {}
    for d in (8192, 16384, 32768):
        p, L = fitpred(var, [512, 1024, 2048, 4096], 4, 1/2, d); rival[var][str(d)] = [p.real, p.imag]; rival[var]["limit"] = [L.real, L.imag]
print("RIVAL family B (d^-1/2 ladder):", json.dumps(rival, indent=1))
json.dump(rival, open("out/PRED-DYN1b-rivalB.json", "w"), indent=1)
