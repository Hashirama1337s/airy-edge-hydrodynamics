"""Model critical point (bessel2: exact near zone + exact Bessel far zone + N1_t = -zeta(3)) over d = 2^8..2^36,
then extraction of its large-d expansion  c(d) - c_inf = sum_k a_k lam^-k,  lam = (2d)^(1/3)."""
import mpmath as mp, json, sys
sys.path.insert(0, "code")
from critmodel import solve, R_bessel
mp.mp.dps = 40
vals = {}
seed = None
for e in range(8, 28):
    d = 2**e
    t, u, q2, w = solve(d, R_bessel, n1t=-mp.zeta(3), seed=seed)
    lam = (2*mp.mpf(d))**(mp.mpf(1)/3)
    lam2 = (2*mp.mpf(2*d))**(mp.mpf(1)/3)
    seed = (t*lam/lam2, u*(lam/lam2)**2)
    vals[e] = (q2, w)
    print(e, mp.nstr(q2, 22), mp.nstr(w, 22), flush=True)
U1 = mp.findroot(lambda U: mp.airyai(U, 1)**2 - U*mp.airyai(U)**2, mp.mpc(-2.79, 1.094))
T1 = mp.airyai(U1, 1)/mp.airyai(U1)
# least squares on e = 20..36 with K powers
out = {"model": {str(2**e): {"q2": [mp.nstr(v[0].real, 25), mp.nstr(v[0].imag, 25)], "w": [mp.nstr(v[1].real, 25), mp.nstr(v[1].imag, 25)]} for e, v in vals.items()}}
for K in [5, 6, 7]:
    for name, idx, cinf in [("q2", 0, mp.mpf(-2)), ("w", 1, mp.mpc(0, 1))]:
        es = list(range(27 - 2*K, 28))
        A = mp.matrix(len(es), K); b = mp.matrix(len(es), 1)
        for r, e in enumerate(es):
            lam = (2*mp.mpf(2**e))**(mp.mpf(1)/3)
            for k in range(K): A[r, k] = lam**(-(k + 1))
            b[r] = vals[e][idx] - cinf
        x = mp.lu_solve(A.T*A, A.T*b) if False else mp.qr_solve(A, b)[0]
        print("K=%d %s:" % (K, name), [mp.nstr(x[k], 12) for k in range(K)])
        out.setdefault("fit", {})["K%d_%s" % (K, name)] = [[mp.nstr(x[k].real, 15), mp.nstr(x[k].imag, 15)] for k in range(K)]
print("derived a1: q2", mp.nstr(-4*T1, 15), " w", mp.nstr(2j*T1, 15))
out["derived_a1"] = {"q2": mp.nstr(-4*T1, 20), "w": mp.nstr(2j*T1, 20)}
json.dump(out, open("out/asym.json", "w"), indent=1)
