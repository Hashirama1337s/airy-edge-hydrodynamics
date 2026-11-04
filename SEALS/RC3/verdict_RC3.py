import json, math
R = json.load(open("blind/RESULT.json"))
c0 = {"2048": complex(-1.9154981851895594, 0.42924741091280705), "8192": complex(-1.94836923521368989578, 0.26885790575211286270)}
def num(s):
    try: return float(s)
    except Exception: return float("nan")
s = R["SPC"]; e1, e2 = num(s["max_rel_R_err"]), num(s["max_theta_err"])
spc = e1 < 1e-3 and e2 < 2e-3
print(f"SPC rel R err {e1} theta err {e2} -> {'PASS' if spc else 'FAIL'}")
for P, d in (("P1", "2048"), ("P2", "8192")):
    r = R.get(d)
    if not isinstance(r, dict): print(P, d, "NOT RUN"); continue
    Rr, th = num(r["R"]), num(r["theta"])
    er = abs(Rr - abs(c0[d])) / abs(c0[d]); et = abs(th - math.atan2(c0[d].imag, c0[d].real))
    if not spc: v = "VOID (SPC failed)"
    elif er < 2e-3 and et < 5e-3: v = "HOLDS"
    elif er > 5e-3: v = "FAILED"
    else: v = "INCONCLUSIVE"
    print(f"{P} d={d}: R {Rr} vs {abs(c0[d]):.10f} rel {er:.2e}; theta {th} vs {math.atan2(c0[d].imag, c0[d].real):.6f} err {et:.2e} -> {v}")
