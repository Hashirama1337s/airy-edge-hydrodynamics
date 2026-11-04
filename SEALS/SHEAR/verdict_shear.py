"""Score BAR-SHEAR (sealed 3c36dbb65f1d0a6b) from shear/RESULT.json. Scorer hashed BEFORE the shear seat reports (amendment A1).
Expected keys (strings): controls {name: digits_matched}, c53_over_16z5, c54_over_16z5, c53_equals_c54 (difference), identifications.
Descriptive success criteria fixed now (A1): an identification counts only if it reports find digits, holdout residual on unused
digits >= 10 digits beyond find, and a perturbation null that kills it; c53 = c54 counts as 'equal' only if |difference| /
|c53| < 1e-25 with >= 30 trusted digits each, 'different' if the difference exceeds 100x the combined stated error."""
import json
import mpmath as mp
mp.mp.dps = 60
R = json.load(open("<lab>/NEXT-2026-11-02/zeta-k5/shear/RESULT.json"))
res = {}
ctrl = R.get("controls", {})
need = ["c22", "c32", "c42", "c52", "c62", "c43", "c44"]
def digits_of(v):
    try: return float(v if not isinstance(v, dict) else v.get("digits", 0))
    except Exception: return 0.0
found = {k: digits_of(v) for k, v in ctrl.items()}
ok = all(any(n in k.replace("_", "").replace(",", "") for k in found) for n in need) and all(v >= 30 for v in found.values()) and found
res["C1"] = "HOLDS" if ok else "FAILED/INCOMPLETE"
print("C1", res["C1"], found)
for key, name, lo, hi in (("c53_over_16z5", "P1", -16.13, -15.19), ("c54_over_16z5", "P2", -16.01, -15.08)):
    if key not in R: res[name] = "VOID"; print(name, "VOID"); continue
    x = mp.mpf(str(R[key]).split()[0])
    res[name] = "HOLDS" if lo <= x <= hi else "FAILED"
    print(name, res[name], mp.nstr(x, 20), f"window [{lo}, {hi}]")
print("DESCRIPTIVE c53 vs c54:", R.get("c53_equals_c54"))
print("DESCRIPTIVE identifications:", json.dumps(R.get("identifications"), indent=1)[:3000])
json.dump(res, open("<lab>/NEXT-2026-11-02/zeta-k5/verdict-SHEAR.json", "w"), indent=1)
