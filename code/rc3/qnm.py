"""Blind-seat shear-channel QNM solver for planar AdS_{d+1} Schwarzschild (Einstein gravity).

Master variable P (radial 'momentum' of the KK gauge field A_mu = h^x_mu), derived in RESULT.md:
    d/du[ (1-u) u^(2-2/d) dP/du ] = V P,   V = q2/4 - w^2/(4(1-u)),
    u = (r0/r)^d,  q2 = (q/2piT)^2,  w = omega/(2piT).
QNM: P ingoing at u=1 (P ~ (1-u)^(-i w/2)) and P regular (P -> const) at u=0
(equivalently the gauge-invariant Z ~ Q = (1-u)u^(2-2/d) P_u vanishes at the boundary).

First-order system in y = -ln u with rescaled momentum S = Q e^{(1-2/d) y}:
    P_y = -S/(1-u),   S_y = (1-2/d) S - e^{-2y/d} V P.
Solver: horizon Frobenius series (x=1-u) -> DOP853 to y=ym ; regular boundary solution from its
convergent z-series (z=r0/r=e^{-y/d}, summed in mpmath where cancellation is mild) then DOP853
outward to ym ; QNM <=> Wronskian W = P_in S_reg - S_in P_reg = 0 at y=ym.
"""
import numpy as np
import mpmath as mp
from scipy.integrate import solve_ivp

def horizon_series(d, q2, w, K):
    """b_n of P = x^alpha sum b_n x^n, x=1-u, alpha=-i w/2."""
    al = -0.5j * w
    p = 2.0 - 2.0 / d
    g = np.empty(K + 1, dtype=complex)
    g[0] = 1.0
    for j in range(1, K + 1):
        g[j] = g[j - 1] * (p - (j - 1)) / j * (-1.0)
    b = np.zeros(K + 1, dtype=complex)
    b[0] = 1.0
    for n in range(1, K + 1):
        s = np.dot(g[1:n + 1], b[n - 1::-1][:n] * (n - np.arange(1, n + 1) + al))
        b[n] = (q2 * b[n - 1] - 4.0 * (n + al) * s) / (4.0 * n * (n - 1j * w))
    return b, g

def horizon_start(d, q2, w, x0=0.5, K=70):
    """P, S at u=1-x0 (overall factor x0^alpha dropped; analytic & nonzero)."""
    b, g = horizon_series(d, q2, w, K)
    al = -0.5j * w
    n = np.arange(K + 1)
    P = np.sum(b * x0 ** n)
    Px = np.sum(b * (n + al) * x0 ** (n - 1.0))
    gx = (1.0 - x0) ** (2.0 - 2.0 / d)
    Q = -x0 * gx * Px
    y0 = -np.log1p(-x0)
    return P, Q * np.exp((1 - 2.0 / d) * y0), y0

def rhs_factory(d, q2, w):
    e = 1.0 - 2.0 / d
    w2 = w * w
    def rhs(y, Y):
        P, S = Y
        om = -np.expm1(-y)  # 1-u
        V = q2 / 4.0 - w2 / (4.0 * om)
        return [-S / om, e * S - np.exp(-2.0 * y / d) * V * P]
    return rhs

def boundary_series_mp(d, q2, w, y, dps=40, tol_exp=26):
    """Regular boundary solution P=sum a_m z^m (a_0=1) at z=e^{-y/d}; returns (P, S, nterms, cancellation)."""
    with mp.workdps(dps):
        q2m = mp.mpc(q2); wm = mp.mpc(w)
        K2 = mp.mpf(d) ** 2 / 4
        qq = K2 * q2m; ww = K2 * wm ** 2
        z = mp.exp(-mp.mpf(y) / d)
        tol = mp.mpf(10) ** (-tol_exp)
        a = {0: mp.mpc(1)}
        A = lambda m: a.get(m, 0) if m >= 0 else 0
        P = mp.mpc(1); zPz = mp.mpc(0)
        zm = mp.mpf(1); small = 0; m = 0; maxabs = mp.mpf(1)
        while True:
            m += 1
            zm *= z
            val = (m - d) * (2 * m + d - 4) * A(m - d) - (m - 2 * d) * (m - 2) * A(m - 2 * d) \
                + (qq - ww) * A(m - 2) - qq * A(m - d - 2)
            am = val / (m * (m + d - 2))
            if am != 0:
                a[m] = am
            t = am * zm
            P += t
            zPz += m * t
            at = abs(t)
            if at > maxabs:
                maxabs = at
            if m > 2 * d + 4 and m * at < tol * (abs(P) + abs(zPz)):
                small += 1
                if small > d + 4:
                    break
            else:
                small = 0
            if m > 400000:
                raise RuntimeError('z-series not converging')
        S = (1 - z ** d) * zPz / d
        return complex(P), complex(S), m, float(maxabs / abs(P))

def boundary_reg(d, q2, w, ym, rtol=1e-13, dps=40, cancel_exp=4.0):
    lam = abs(q2 - w * w) * d / 8.0  # largest series term ~ exp(lam z^2)
    z0 = min(np.exp(-ym / d), np.sqrt(cancel_exp / max(lam, 1e-30)))
    y0 = -d * np.log(z0)
    if y0 <= ym * (1 + 1e-12):
        P, S, nt, canc = boundary_series_mp(d, q2, w, ym, dps=dps)
        return P, S, dict(y0=ym, nterms=nt, canc=canc, nfev_reg=0)
    P0, S0, nt, canc = boundary_series_mp(d, q2, w, y0, dps=dps)
    sol = solve_ivp(rhs_factory(d, q2, w), (y0, ym), [P0, S0], method='DOP853', rtol=rtol, atol=1e-300)
    return sol.y[0, -1], sol.y[1, -1], dict(y0=y0, nterms=nt, canc=canc, nfev_reg=sol.nfev)

def wronskian(d, q2, w, ym=60.0, rtol=1e-13, x0=0.5, K=70, dps=40, cancel_exp=4.0, ret_info=False):
    P0, S0, y0 = horizon_start(d, q2, w, x0=x0, K=K)
    sol = solve_ivp(rhs_factory(d, q2, w), (y0, ym), [P0, S0], method='DOP853', rtol=rtol, atol=1e-300)
    Pin, Sin = sol.y[0, -1], sol.y[1, -1]
    Pr, Sr, inf = boundary_reg(d, q2, w, ym, rtol=rtol, dps=dps, cancel_exp=cancel_exp)
    W = Pin * Sr - Sin * Pr
    if ret_info:
        inf.update(nfev=sol.nfev, scale=abs(Pin * Sr) + abs(Sin * Pr))
        return W, inf
    return W

def find_mode(d, q2, wguess, tol=1e-14, maxit=40, **kw):
    """Secant iteration on W(w)."""
    w0 = complex(wguess)
    h = 1e-6 * (abs(w0) + 1e-3)
    w1 = w0 + h
    f0 = wronskian(d, q2, w0, **kw)
    f1 = wronskian(d, q2, w1, **kw)
    for it in range(maxit):
        if f1 == f0:
            break
        w2 = w1 - f1 * (w1 - w0) / (f1 - f0)
        w0, f0 = w1, f1
        w1 = w2
        f1 = wronskian(d, q2, w1, **kw)
        if abs(w1 - w0) < tol * max(1.0, abs(w1)):
            return w1, it
    return w1, -1

# ---- RC3: regular boundary solution in closed form (pure AdS, valid where u=e^{-y} is negligible)
# f=1:  z P'' + (d-1) P' - k^2 z P = 0,  k^2=(d^2/4)(q2-w^2)  ->  P = (kz)^{-nu} I_nu(kz), nu=(d-2)/2
# z P_z = (kz)^{-nu} (kz) I_{nu+1}(kz).  Both are entire in (kz)^2 (branch of k irrelevant).
def boundary_bessel(d, q2, w, ym, dps=30):
    with mp.workdps(dps):
        nu = mp.mpf(d - 2) / 2
        k2 = (mp.mpf(d) ** 2 / 4) * (mp.mpc(q2) - mp.mpc(w) ** 2)
        z = mp.exp(-mp.mpf(ym) / d)
        x = mp.sqrt(k2) * z
        I0 = mp.besseli(nu, x); I1 = mp.besseli(nu + 1, x)
        # common factor x^{-nu} dropped (would cancel in root condition? no: keep ratio form)
        # use P = I0 * x^{-nu}, zPz = I1 * x^{1-nu}; drop common analytic factor x^{-nu}*... only if branch-safe:
        # x^{-nu} with nu integer or half-integer: for even d, nu integer -> x^{-nu} I_nu(x) entire in x^2; we
        # return P and S divided by the common factor x^{-nu}/(something) -> use ratio R = x I1/I0 instead.
        Rr = x * I1 / I0          # = z P_z / P, even in x -> branch safe
        return complex(Rr)

def wronskian_b(d, q2, w, ym=60.0, rtol=1e-13, x0=0.5, K=70, dps=30, ret_info=False):
    """Root function using log-derivative matching: W = S_in - P_in * (zP_z/P)_reg / d  (u-terms dropped at ym)."""
    P0, S0, y0 = horizon_start(d, q2, w, x0=x0, K=K)
    sol = solve_ivp(rhs_factory(d, q2, w), (y0, ym), [P0, S0], method='DOP853', rtol=rtol, atol=1e-300)
    Pin, Sin = sol.y[0, -1], sol.y[1, -1]
    Rr = boundary_bessel(d, q2, w, ym, dps=dps)
    om = -np.expm1(-ym)
    W = Sin - Pin * om * Rr / d
    if ret_info:
        return W, dict(nfev=sol.nfev, scale=abs(Sin) + abs(Pin * Rr / d))
    return W
