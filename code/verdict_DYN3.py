import json, mpmath as mp
mp.mp.dps = 40
P = json.load(open("data/DYN3/PRED-SOUND.json"))
R = json.load(open("data/DYN3/RESULT.json"))["pole"]
cells = [("0.5", d) for d in ("3","3.5","4","4.5","5","6")] + [("1.0", d) for d in ("3","3.5","4","4.5","5","6")] + [("1.5", d) for d in ("4.5","5","6")] + [("3", "6")]
def get(dct, q, d):
    for qk in (q, str(float(q)), q.rstrip('0').rstrip('.')):
        if qk in dct:
            for dk in (d, str(float(d)), d.rstrip('0').rstrip('.') if '.' in d else d):
                if dk in dct[qk]: return dct[qk][dk]
    return None
def score(predset, tag):
    res = {}; allok = True; d4 = True; void = False
    for q, d in cells:
        p = get(P[predset], q, d); b = get(R, q, d)
        key = f"{q}@{d}"
        try:
            x = mp.mpc(mp.mpf(b["re"]), mp.mpf(b["im"])) if isinstance(b, dict) else None
        except Exception: x = None
        if x is None or p is None: res[key] = "VOID"; void = True; print(tag, key, "VOID"); continue
        pv = mp.mpc(mp.mpf(p["re"]), mp.mpf(p["im"])); bar = mp.mpf(p["bar"]); e = abs(x - pv)
        ok = e <= 3 * bar; allok &= ok
        if d == "4": d4 &= ok
        res[key] = "HOLDS" if ok else "FAILED"; print(f"{tag} {key}: {res[key]} |diff| {mp.nstr(e,3)} rel {mp.nstr(e/abs(x),3)} 3*bar {mp.nstr(3*bar,3)}")
    res["ALL"] = "VOID-PARTIAL" if void else ("HOLDS" if allok else "FAILED"); res["H_d4"] = "HOLDS" if d4 else "FAILED"
    print(tag, "ALL", res["ALL"], "H(d=4)", res["H_d4"]); return res
out = {"A": score("pred", "A"), "B_descriptive": score("pred_B", "B")}
print("descriptive d=4 large momentum:", {q: get(R, q, "4") for q in ("3", "5")})
json.dump(out, open("out/verdict-DYN3.json", "w"), indent=1)
