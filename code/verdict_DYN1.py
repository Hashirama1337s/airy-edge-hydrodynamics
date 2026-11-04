"""Score BAR-DYN1 from DYN1/blind/RESULT.json:
{"d4": {"q2": [re, im], "w": [re, im]}, "track": {"<d>": {"q2": [re, im], "w": [re, im], "on_sheet": bool, "nearest_in_census": bool}},
 "c1": {"<d>": {"q2": [re, im], "w": [re, im]}} (optional)}"""
import json, numpy as np
R = json.load(open("data/DYN1/RESULT.json"))
cz = lambda v: complex(float(v[0]), float(v[1]))
res = {}
q4, w4 = cz(R["d4"]["q2"]), cz(R["d4"]["w"])
okc = abs(q4 - (1.8906469 + 1.1711505j)) < 2e-7 * 3 and abs(w4 - (1.4436414 - 1.0692250j)) < 2e-7 * 3
res["C1"] = "HOLDS" if okc else "FAILED"; print("C1", res["C1"], q4, w4)
T = R["track"]; ds = [256, 512, 1024, 2048, 4096]
res["P1"] = "HOLDS" if all(str(d) in T and T[str(d)].get("on_sheet") and T[str(d)].get("nearest_in_census") for d in ds) else "FAILED"
print("P1", res["P1"])
fd = [512, 1024, 2048, 4096]
def fit(var, p):
    A = np.array([[1, d**-p, d**(-2*p)] for d in fd], dtype=complex); y = np.array([cz(T[str(d)][var]) for d in fd])
    c, *_ = np.linalg.lstsq(A, y, rcond=None); return c[0]
lim = {(v, fam): fit(v, p) for v in ("q2", "w") for fam, p in (("A", 1/3), ("B", 1/2))}
for k, v in lim.items(): print("limit", k, v)
dA = max(abs(lim[("q2","A")] + 2), abs(lim[("w","A")] - 1j)); dB = max(abs(lim[("q2","B")] + 2), abs(lim[("w","B")] - 1j))
fam_diff = max(abs(lim[("q2","A")] - lim[("q2","B")]), abs(lim[("w","A")] - lim[("w","B")]))
if fam_diff > 0.1: res["P2"] = "VOID"
elif dA < 0.05 and dB < 0.05: res["P2"] = "HOLDS"
elif dA > 0.1 and dB > 0.1: res["P2"] = "FAILED"
else: res["P2"] = "FAILED (partial: one family within 0.05-0.1)"
print("P2", res["P2"], "dist A", dA, "dist B", dB, "family diff", fam_diff)
e = -(np.log(abs(cz(T["4096"]["q2"]) + 2)) - np.log(abs(cz(T["2048"]["q2"]) + 2))) / np.log(2)
res["P3"] = "HOLDS" if 0.28 <= e <= 0.55 else "FAILED"; print("P3", res["P3"], "exponent", e)
res["P4"] = "HOLDS" if any(abs(cz(T[str(d)]["q2"])) < 2 for d in (256, 512, 1024) if str(d) in T) else "FAILED"; print("P4", res["P4"])
C = R.get("c1")
if C and "4096" in C:
    dist = max(abs(cz(C["4096"]["q2"]) + 2), abs(cz(C["4096"]["w"]) - 1j)); res["N1"] = "HOLDS" if dist > 0.3 else "FAILED"; print("N1", res["N1"], dist)
else: res["N1"] = "VOID"; print("N1 VOID")
json.dump(res, open("out/verdict-DYN1.json", "w"), indent=1)
