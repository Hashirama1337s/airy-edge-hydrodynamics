import json
R = json.load(open("data/RC/RESULT.json"))
def f(x): return float(x)
out = []
for d, P in (("1024", "P1"), ("512", "P2"), ("8192", "P3")):
    r = R.get(d)
    if r is None: out.append(f"{P} d={d} NOT RUN"); continue
    lit = r["out_lit_sectors"]; lit = json.loads(lit) if isinstance(lit, str) else lit
    lit = [int(x) for x in lit]; c0s = int(r["sector_of_c0"])
    on, o2n = f(r["out_mismatch_c0_n"]), f(r["out_mismatch_c0_2n"])
    p0 = on > 1e-3 and o2n > 1e-3 and abs(on - o2n) <= 0.1 * max(on, o2n) and lit == [c0s]
    i1, i2 = f(r["in_max_mismatch_n"]), f(r["in_max_mismatch_2n"])
    if not p0: v = "VOID (P0 failed)"
    elif i1 < 1e-9 and i2 < 1e-9: v = "HOLDS"
    elif max(i1, i2) > 1e-6: v = "FAILED"
    else: v = "INCONCLUSIVE"
    out.append(f"{P} d={d}: P0 {'PASS' if p0 else 'FAIL'} (lit {lit}, c0 sector {c0s}, c0 mism {on:.3e}/{o2n:.3e}); in max {i1:.2e}/{i2:.2e}; max ray jump {r['max_ray_jump']} -> {v}")
print("\n".join(out))
