import json, numpy as np, mpmath as mp
P = json.load(open("data/THEORY/PRED-THEORY.json"))["predictions"]
R = json.load(open("data/DYN1b/RESULT.json"))
cz = lambda v: complex(float(v[0]), float(v[1]))
res = {}; T = R.get("track", {})
U1 = mp.mpc("-2.790298385849104432412254", "1.094309619284491031878315")
T1 = complex(mp.airyai(U1, 1) / mp.airyai(U1))
for model, key in (("T1", "A_model_parameter_free"), ("T2", "B_model_plus_calibrated_residual")):
    ok = True
    for d in ("8192", "16384", "32768"):
        if d not in T: ok = None; break
        m = P[d][key]; eq = abs(cz(T[d]["q2"]) - cz(m["q2"])); ew = abs(cz(T[d]["w"]) - cz(m["w"]))
        good = eq <= float(m["bar_q2"]) and ew <= float(m["bar_w"]); ok &= good
        print(f"{model} d={d} |dq2| {eq:.2e} (bar {m['bar_q2']}) |dw| {ew:.2e} (bar {m['bar_w']}) -> {'ok' if good else 'MISS'}")
    res[model] = "VOID" if ok is None else ("HOLDS" if ok else "FAILED")
if all(d in T for d in ("8192", "32768")):
    r = {d: abs(cz(T[str(d)]["q2"]) + 2 + 4 * T1 * (2 * d) ** (-1/3)) for d in (8192, 32768)}
    e = -np.log(r[32768] / r[8192]) / np.log(4); res["T3"] = "HOLDS" if e >= 0.85 else "FAILED"; print("T3 exponent", e, res["T3"])
    X = {d: (cz(T[str(d)]["q2"]) + 2 - 2j * (cz(T[str(d)]["w"]) - 1j)) * d / 4 for d in (8192, 16384, 32768)}
    dev = {d: abs(X[d] - 1) for d in X}; res["T4"] = "HOLDS" if dev[32768] < dev[8192] and dev[32768] < 0.05 else "FAILED"; print("T4 (as sealed, mis-set)", dev, res["T4"])
    res["T4prime"] = "HOLDS" if dev[8192] > dev[16384] > dev[32768] and abs(dev[32768] - 0.069) < 0.01 else "FAILED"; print("T4prime", res["T4prime"])
else: res["T3"] = res["T4"] = "VOID"
res["T5"] = "HOLDS" if T.get("8192", {}).get("on_sheet") is True else ("VOID" if "8192" not in T else "FAILED"); print("T5", res["T5"])
print(res); json.dump(res, open("out/verdict-THEORY.json", "w"), indent=1)
