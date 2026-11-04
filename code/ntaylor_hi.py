"""Taylor coefficients n_ab of the exact d=inf near-zone ratio N(t,u) = sum n_ab t^a u^b at (0,0), by a 2D Cauchy integral."""
import mpmath as mp, json, sys
sys.path.insert(0, "code")
from inner import N
mp.mp.dps = 30
M = 40; rt = mp.mpf("0.1"); ru = mp.mpf("0.1")
vals = [[N(rt*mp.expj(2*mp.pi*k/M), ru*mp.expj(2*mp.pi*l/M + mp.mpf("0.1"))) for l in range(M)] for k in range(M)]
out = {}
for a in range(5):
    for b in range(4):
        if a + 2*b > 5: continue
        s = mp.mpf(0)
        for k in range(M):
            for l in range(M):
                s += vals[k][l]*mp.expj(-2*mp.pi*k*a/M)*mp.expj(-(2*mp.pi*l/M + mp.mpf("0.1"))*b)
        co = s/(M*M)/rt**a/ru**b
        out["n%d%d" % (a, b)] = [mp.nstr(co.real, 18), mp.nstr(co.imag, 3)]
        print("n_%d%d =" % (a, b), mp.nstr(co.real, 18), " (imag", mp.nstr(co.imag, 2), ")")
json.dump(out, open("out/ntaylor_hi.json", "w"), indent=1)
