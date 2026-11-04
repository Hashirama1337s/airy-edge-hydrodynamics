"""Score BAR-DYN2 from DYN2/blind/RESULT.json {"pole": {"<qbar>": {"<d>": "<Im Omega string>"}}, ...}"""
import json, mpmath as mp
mp.mp.dps = 40
P = json.load(open("<lab>/NEXT-2026-11-03/dynamics/DYN2/PRED-DYN.json"))["pred"]
R = json.load(open("<lab>/NEXT-2026-11-03/dynamics/DYN2/blind/RESULT.json"))["pole"]
res = {}; allok = True; d4 = True
for q in P:
    for d in P[q]:
        if q == "1.5" and d == "3": continue
        key = f"{q}@{d}"
        if q not in R or d not in R[q]: res[key] = "VOID"; allok = False; print(key, "VOID"); continue
        x = mp.mpf(R[q][d]); p = mp.mpf(P[q][d]["im"]); bar = mp.mpf(P[q][d]["bar"])
        ok = abs(x - p) <= 3 * bar; allok &= ok
        if d == "4": d4 &= ok
        res[key] = "HOLDS" if ok else "FAILED"
        print(f"{key}: {res[key]} |diff| {mp.nstr(abs(x-p),3)} rel {mp.nstr(abs(x-p)/abs(x),3)} 3*bar {mp.nstr(3*bar,3)}")
res["ALL"] = "HOLDS" if allok else "FAILED"; res["H_d4"] = "HOLDS" if d4 else "FAILED"
print("ALL", res["ALL"], "H(d=4)", res["H_d4"])
json.dump(res, open("<lab>/NEXT-2026-11-03/dynamics/DYN2/verdict-DYN2.json", "w"), indent=1)
