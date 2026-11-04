"""Write PRED-THEORY.json: derived predictions for the shear hydro critical point c0 at d = 8192, 16384, 32768.
(A) parameter-free matched model (crit_bessel2 / asym.json values): exact near zone (d=inf) + N1 = -zeta(3) t (from exact g1)
    + exact Bessel far zone.  Expected error O(d^-5/3).
(B) = (A) + residual (data - model) fitted at d = 256..4096 with c5 lam^-5 + c6 lam^-6 [+ c7 lam^-7]   (numerically calibrated).
Also the bare truncated series: leading law and leading + a3 (a2 = 0)."""
import json, mpmath as mp
mp.mp.dps = 30
A = json.load(open("data/theory/asym.json"))
R = json.load(open("data/DYN1/RESULT.json"))
cz = lambda p: mp.mpc(mp.mpf(p[0]), mp.mpf(p[1]))
lamf = lambda d: (2*mp.mpf(d))**(mp.mpf(1)/3)
a1q = cz(["1.28658749453695", "6.80441632726015"]); a1q = mp.mpc(*[mp.mpf(x) for x in A["derived_a1"]["q2"].strip("()j").replace("+", " ").split()]) if False else a1q
# recompute a1 exactly
U1 = mp.findroot(lambda U: mp.airyai(U, 1)**2 - U*mp.airyai(U)**2, mp.mpc(-2.79, 1.094))
T1 = mp.airyai(U1, 1)/mp.airyai(U1)
a1q, a1w = -4*T1*2**(-mp.mpf(1)/3), 2j*T1*2**(-mp.mpf(1)/3)        # coefficients of d^(-1/3)
a3w_l = cz(A["fit"]["K7_w"][2]); a3q_l = cz(A["fit"]["K7_q2"][2])  # coefficients of lam^-3 = 1/(2d)
res = {}
for ds in ["256", "512", "1024", "2048", "4096"]:
    m = A["model"][ds]; d = R["track"][ds]
    res[int(ds)] = (cz(d["q2"]) - cz(m["q2"]), cz(d["w"]) - cz(m["w"]))
fits = {}
for K in [2, 3]:
    for idx, name in [(0, "q2"), (1, "w")]:
        ds = sorted(res)
        M = mp.matrix(len(ds), K); b = mp.matrix(len(ds), 1)
        for r, d in enumerate(ds):
            for k in range(K): M[r, k] = lamf(d)**(-(5 + k))
            b[r] = res[d][idx]
        x = mp.qr_solve(M, b)[0]
        fits[(K, name)] = [x[k] for k in range(K)]
out = {"object": "shear-channel hydro critical point c0 of AdS_{d+1} black brane (tracked DYN1 point, Im qfr^2 > 0 copy), frak units qfr^2 = 4 sigma, wfr = 2 omega/d",
       "derived_law": {"exponent": "d^(-1/3) exactly (a2 = 0; next term d^(-1))",
                       "qfr2_plus_2": "-4 T1 (2d)^(-1/3) + (8 - 4 t3)/(2d) + O(d^(-4/3))",
                       "wfr_minus_i": "2 i T1 (2d)^(-1/3) + 2 i t3/(2d) + O(d^(-4/3))",
                       "U1": [mp.nstr(U1.real, 25), mp.nstr(U1.imag, 25)], "T1=Ai'(U1)/Ai(U1)": [mp.nstr(T1.real, 25), mp.nstr(T1.imag, 25)],
                       "A (coef of d^-1/3 in qfr^2+2)": [mp.nstr(a1q.real, 20), mp.nstr(a1q.imag, 20)],
                       "B (coef of d^-1/3 in wfr-i)": [mp.nstr(a1w.real, 20), mp.nstr(a1w.imag, 20)],
                       "t3 (model, numerical)": [mp.nstr((a3w_l/(2j)).real, 10), mp.nstr((a3w_l/(2j)).imag, 10)],
                       "X = (qfr^2+2) - 2i(wfr-i)": "4/d + O(d^(-4/3))"},
       "predictions": {}}
for d in [8192, 16384, 32768]:
    m = A["model"][str(d)]
    qA, wA = cz(m["q2"]), cz(m["w"])
    lam = lamf(d)
    qB = qA + sum(c*lam**(-(5 + k)) for k, c in enumerate(fits[(3, "q2")]))
    wB = wA + sum(c*lam**(-(5 + k)) for k, c in enumerate(fits[(3, "w")]))
    qB2 = qA + sum(c*lam**(-(5 + k)) for k, c in enumerate(fits[(2, "q2")]))
    wB2 = wA + sum(c*lam**(-(5 + k)) for k, c in enumerate(fits[(2, "w")]))
    barA_q = abs(res[4096][0])*(mp.mpf(4096)/d)**(mp.mpf(5)/3)*2
    barA_w = abs(res[4096][1])*(mp.mpf(4096)/d)**(mp.mpf(5)/3)*2
    barB_q = max(3*abs(qB - qB2), abs(qB - qA)/5)
    barB_w = max(3*abs(wB - wB2), abs(wB - wA)/5)
    lead_q = -2 + a1q*mp.mpf(d)**(-mp.mpf(1)/3); lead_w = 1j + a1w*mp.mpf(d)**(-mp.mpf(1)/3)
    s3_q = lead_q + a3q_l/(2*d); s3_w = lead_w + a3w_l/(2*d)
    f = lambda z, n=16: [mp.nstr(z.real, n), mp.nstr(z.imag, n)]
    out["predictions"][str(d)] = {
        "A_model_parameter_free": {"q2": f(qA), "w": f(wA), "bar_q2": mp.nstr(barA_q, 2), "bar_w": mp.nstr(barA_w, 2)},
        "B_model_plus_calibrated_residual": {"q2": f(qB), "w": f(wB), "bar_q2": mp.nstr(barB_q, 2), "bar_w": mp.nstr(barB_w, 2)},
        "leading_law_only": {"q2": f(lead_q, 10), "w": f(lead_w, 10)},
        "series_a1_plus_a3": {"q2": f(s3_q, 10), "w": f(s3_w, 10)},
        "abs_q2_A": mp.nstr(abs(qA), 12)}
    print(d, json.dumps(out["predictions"][str(d)]))
out["pass_rule_suggested"] = ("A passes if |q2_exact - q2_A| <= bar_q2 and |w_exact - w_A| <= bar_w; B likewise with its bars. "
                              "The law itself fails if (q2_exact+2) - (-4 T1 (2d)^-1/3) does not shrink like d^-1 (local exponent of the residual < 0.85 between 8192 and 32768), "
                              "or if X*d/4 does not approach 1 (|X d/4 - 1| growing with d).")
out["residual_fits"] = {"K%d_%s" % k: [[mp.nstr(c.real, 8), mp.nstr(c.imag, 8)] for c in v] for k, v in fits.items()}
json.dump(out, open("out/PRED-THEORY.json", "w"), indent=1)
