import json, math
R = json.load(open("data/RC2/RESULT.json"))
c0 = {"512": complex(-1.854341963762, 0.691670108026), "1024": complex(-1.8901721196114076, 0.5439416103393121)}
pc = R["PC"]; a, g = float(pc["absq2_star_ours"]), float(pc["absq2_star_GKST"])
pcok = abs(a - g) / abs(g) < 5e-3 and f"{a:.3g}" == f"{g:.3g}"
print(f"PC ours {a} GKST {g} ({pc.get('locator')}) -> {'PASS' if pcok else 'FAIL'}")
for P, d in (("P1", "512"), ("P2", "1024")):
    r = R.get(d)
    if r is None: print(P, d, "NOT RUN"); continue
    Rr, th, be = float(r["R"]), float(r["theta"]), (lambda s: float(s) if s.replace(".","",1).lstrip("-").isdigit() else float("nan"))(r["beta"])
    er = abs(Rr - abs(c0[d])) / abs(c0[d]); et = abs(th - math.atan2(c0[d].imag, c0[d].real)); eb = abs(be - 0.5)
    if not pcok: v = "VOID (PC failed)"
    elif er < 2e-3 and et < 5e-3 and eb < 0.1: v = "HOLDS"
    elif er > 1e-2: v = "FAILED"
    else: v = "INCONCLUSIVE"
    print(f"{P} d={d}: relR {er:.2e} dtheta {et:.2e} dbeta {eb:.2e} -> {v}")
