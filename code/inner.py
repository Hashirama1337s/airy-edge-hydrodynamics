"""Inner (boundary-layer) model of the large-d shear hydro critical point near (qfr^2, wfr) = (-2, i).
Derivation in THEORY-DYN.md.  Variables: t = -1/2 - i w, u = delta^2 = 1 - 4 w^2 + 4 sig, lam = (2d)^(1/3).
Near zone (d = inf, exact hypergeometric):  N(t,u) = Q/P of y = x^(1/2) E at large x.
Far zone (Airy):                          Q/P = h(U)/lam,  h = Ai'/Ai,  U = lam^2 u / 4.
QNM:   G = lam N(t,u) - h(lam^2 u/4) = 0.   Branch point of t(sig): G_t/4 + G_u (1+2t) = 0   (sig = -1/2 + u/4 - t - t^2).
"""
import mpmath as mp, json, sys
mp.mp.dps = 40

def N(t, u):
    dl = mp.sqrt(u)
    if abs(dl) < mp.mpf(10)**-12:
        dl = mp.mpf(10)**-12  # N is even in delta; tiny delta fine at this precision
    Ap = (1 + dl) * mp.gamma(dl) * mp.rgamma(t + dl/2) * mp.rgamma(2 + t + dl/2)
    Bp = (1 - dl) * mp.gamma(-dl) * mp.rgamma(t - dl/2) * mp.rgamma(2 + t - dl/2)
    return (dl/2) * (Ap - Bp) / (Ap + Bp)

def h(U):
    return mp.airyai(U, 1) / mp.airyai(U)

def W(U):
    a, ap = mp.airyai(U), mp.airyai(U, 1)
    return ap**2 - U*a**2

def system(t, u, lam):
    G = lam*N(t, u) - h(lam**2*u/4)
    Gt = mp.diff(lambda tt: lam*N(tt, u) - h(lam**2*u/4), t)
    Gu = mp.diff(lambda uu: lam*N(t, uu) - h(lam**2*uu/4), u)
    return G, Gt/4 + Gu*(1 + 2*t)

def crit(lam, t0, u0):
    f = lambda t, u: system(t, u, lam)
    t, u = mp.findroot(f, (t0, u0))
    return t, u

def to_frak(t, u):
    sig = -mp.mpf(1)/2 + u/4 - t - t*t
    w = 1j*(mp.mpf(1)/2 + t)
    return 4*sig, 2*w

if __name__ == "__main__":
    out = {}
    # 1. zeros of W(U) = Ai'^2 - U Ai^2 (W' = -Ai^2): seeds on a grid in the upper half plane near the negative axis
    zs = []
    for re in [x*0.5 for x in range(-24, 2)]:
        for im in [0.3, 0.8, 1.3, 1.8]:
            try:
                z = mp.findroot(W, mp.mpc(re, im))
            except Exception:
                continue
            if abs(W(z)) < 1e-25 and all(abs(z - y) > 1e-8 for y in zs) and abs(z) < 14:
                zs.append(z)
    zs.sort(key=lambda z: abs(z))
    out["W_zeros"] = [[mp.nstr(z.real, 25), mp.nstr(z.imag, 25), mp.nstr(h(z).real, 25), mp.nstr(h(z).imag, 25)] for z in zs]
    for z in zs:
        print("U_n =", mp.nstr(z, 20), " T_n = h(U_n) =", mp.nstr(h(z), 20), " check T^2-U:", mp.nstr(h(z)**2 - z, 3))
    # 2. Taylor coefficients of N(t,u) at (0,0)
    Nt = mp.diff(lambda t: N(t, mp.mpf(10)**-30), 0)
    Ntt = mp.diff(lambda t: N(t, mp.mpf(10)**-30), 0, 2) / 2
    Nu = mp.diff(lambda u: N(mp.mpf(0), u), mp.mpf(10)**-3) # placeholder (refined below by fit)
    # N is analytic in u: get N_u from a symmetric finite difference around u = 0 using complex u
    hh = mp.mpf(10)**-8
    Nu = (N(mp.mpf(0), hh) - N(mp.mpf(0), -hh)) / (2*hh)
    N0 = N(mp.mpf(0), mp.mpf(10)**-30)
    out["N_taylor"] = {"N0": mp.nstr(N0, 15), "N_t": mp.nstr(Nt, 25), "N_tt": mp.nstr(Ntt, 25), "N_u": mp.nstr(Nu, 25)}
    print("N(0,0) =", mp.nstr(N0, 5), " N_t =", mp.nstr(Nt, 20), " N_tt =", mp.nstr(Ntt, 20), " N_u =", mp.nstr(Nu, 20))
    json.dump(out, open("out/inner_basics.json", "w"), indent=1)
