import json, numpy as np
P = json.load(open("<lab>/NEXT-2026-11-03/dynamics/DYN1b/PRED-DYN1b.json"))
R = json.load(open("<lab>/NEXT-2026-11-03/dynamics/DYN1b/blind/RESULT.json"))
R0 = json.load(open("<lab>/NEXT-2026-11-03/dynamics/DYN1/blind/RESULT.json"))["track"]
cz = lambda v: complex(float(v[0]), float(v[1]))
res = {}
for i, d in enumerate(("8192", "16384", "32768"), start=1):
    try:
        q, w = cz(R["track"][d]["q2"]), cz(R["track"][d]["w"])
    except Exception:
        res[f"P{i}"] = "VOID"; print(f"P{i} d={d} VOID"); continue
    eq, ew = abs(q - cz(P["q2"][d]["pred"])), abs(w - cz(P["w"][d]["pred"]))
    ok = eq <= P["q2"][d]["bar"] and ew <= P["w"][d]["bar"]
    res[f"P{i}"] = "HOLDS" if ok else "FAILED"
    print(f"P{i} d={d} {res[f'P{i}']} |dq2| {eq:.3e} (bar {P['q2'][d]['bar']:.2e}) |dw| {ew:.3e} (bar {P['w'][d]['bar']:.2e})")
pts = {int(d): R0[str(d)] for d in (512, 1024, 2048, 4096)}
for d in ("8192", "16384", "32768"):
    if d in R.get("track", {}): pts[int(d)] = R["track"][d]
ds = sorted(pts)
lim = {}
for var in ("q2", "w"):
    A = np.array([[d**(-k/3) for k in range(4)] for d in ds], dtype=complex); y = np.array([cz(pts[d][var]) for d in ds])
    lim[var] = np.linalg.lstsq(A, y, rcond=None)[0][0]
ok4 = len(ds) == 7 and abs(lim["q2"] + 2) < 0.01 and abs(lim["w"] - 1j) < 0.01
res["P4"] = "HOLDS" if ok4 else ("VOID" if len(ds) < 7 else "FAILED"); print("P4", res["P4"], lim)
C = R.get("census", {})
ok5 = all(C.get(d, {}).get("nearest_in_census") is True for d in ("512", "1024"))
res["P5"] = "HOLDS" if ok5 else ("VOID" if not C else "FAILED"); print("P5", res["P5"], C)
json.dump({k: str(v) for k, v in res.items()}, open("<lab>/NEXT-2026-11-03/dynamics/DYN1b/verdict-DYN1b.json", "w"), indent=1)
