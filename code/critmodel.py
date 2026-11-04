"""Critical point of the matched model  N(t,u) [+ n1/d] = R_d(u)  (no fitted parameter).
N: exact d=inf near-zone ratio (hypergeometric).  R_d: exact far zone, -sqrt(alpha) J'_nu(2 nu sqrt(alpha))/J_nu(...), nu = d/2,
alpha = (1-u)/4.  n1 = N1(0,0) = -n11 - zeta(2)/2 (from exact g1); n11 = -zeta(2)/2 numerically -> n1 = 0.
mode bessel2: adds N1_t = -zeta(3) (from the delta^1 term of exact g1, using 8 n02 + n21 = zeta(2) numerically).
Branch point of t(sig):  G = 0,  G_t/4 + G_u (1+2t) = 0.  frak: qfr^2 = -2 + u - 4t - 4t^2, wfr = i(1+2t).
usage: critmodel.py d1 d2 ...   (also 'airy' variant R = h(U)/lam for comparison)"""
import mpmath as mp, json, sys
sys.path.insert(0, "code")
from inner import N
mp.mp.dps = 30

def R_bessel(d, u):
    # J'_nu/J_nu = J_{nu-1}/J_nu - nu/k, ratio rho_nu = J_nu/J_{nu-1} by backward recurrence rho_m = 1/(2m/k - rho_{m+1})
    nu = mp.mpf(d)/2
    sa = mp.sqrt((1 - u)/4)
    k = 2*nu*sa
    depth = int(15*float(nu)**(1.0/3) + 100)
    rho = mp.mpf(0)
    for m in range(depth, -1, -1):
        rho = 1/(2*(nu + m)/k - rho)
    return -sa*(1/rho - nu/k)

def R_airy(d, u):
    lam = (2*mp.mpf(d))**(mp.mpf(1)/3)
    U = lam**2*u/4
    return mp.airyai(U, 1)/mp.airyai(U)/lam

def solve(d, R, n1=0, n1t=0, seed=None):
    lam = (2*mp.mpf(d))**(mp.mpf(1)/3)
    U1 = mp.findroot(lambda U: mp.airyai(U, 1)**2 - U*mp.airyai(U)**2, mp.mpc(-2.79, 1.094))
    T1 = mp.airyai(U1, 1)/mp.airyai(U1)
    if seed is None:
        seed = (T1/lam, 4*U1/lam**2 + 8/lam**3)
    G = lambda t, u: N(t, u) + (n1 + n1t*t)/mp.mpf(d) - R(d, u)
    def F(t, u):
        g = G(t, u)
        gt = mp.diff(lambda x: G(x, u), t)
        gu = mp.diff(lambda x: G(t, x), u)
        return g, gt/4 + gu*(1 + 2*t)
    t, u = mp.findroot(F, seed)
    return t, u, -2 + u - 4*t - 4*t*t, 1j*(1 + 2*t)

if __name__ == "__main__":
    R = json.load(open("data/DYN1/RESULT.json"))
    mode = sys.argv[1]
    res = {}
    for ds in sys.argv[2:]:
        d = int(ds)
        if mode == "bessel2":
            t, u, q2, w = solve(d, R_bessel, n1t=-mp.zeta(3))
        else:
            t, u, q2, w = solve(d, R_bessel if mode == "bessel" else R_airy)
        line = {"q2": [mp.nstr(q2.real, 20), mp.nstr(q2.imag, 20)], "w": [mp.nstr(w.real, 20), mp.nstr(w.imag, 20)]}
        if ds in R["track"]:
            q2d = mp.mpc(*map(mp.mpf, R["track"][ds]["q2"])); wd = mp.mpc(*map(mp.mpf, R["track"][ds]["w"]))
            line["dq_data_minus_model"] = mp.nstr(q2d - q2, 8); line["dw_data_minus_model"] = mp.nstr(wd - w, 8)
            line["dq*d^(4/3)"] = mp.nstr((q2d - q2)*mp.mpf(d)**(mp.mpf(4)/3), 8)
            line["dw*d^(4/3)"] = mp.nstr((wd - w)*mp.mpf(d)**(mp.mpf(4)/3), 8)
            line["dq*d^(5/3)"] = mp.nstr((q2d - q2)*mp.mpf(d)**(mp.mpf(5)/3), 8)
            line["dw*d^(5/3)"] = mp.nstr((wd - w)*mp.mpf(d)**(mp.mpf(5)/3), 8)
        res[ds] = line
        print(mode, ds, json.dumps(line), flush=True)
    json.dump(res, open("out/crit_%s.json" % mode, "w"), indent=1)
