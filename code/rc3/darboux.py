"""Large-n analysis of r_n = Im c_n (c_n = i r_n, r_n real).
Model (free, conjugate pair):  r_n = 2 Re[ C n^(-g) x^n (1 + sum_k a_k / n^k) ],  x = exp(-i theta)/R,  g = 1 + beta.
Also a three-term-recurrence estimator (pair => r_n = P_n r_{n-1} + S_n r_{n-2})."""
import json, sys
import numpy as np
from scipy.optimize import least_squares

def load(tag):
    o = json.load(open(f'cauchy_{tag}.json'))
    return np.array(o['c_im']), o

def model(p, n, ncorr):
    R, th, g, Cr, Ci = p[:5]
    a = p[5:5 + 2 * ncorr].reshape(-1, 2)
    corr = np.ones_like(n, dtype=complex)
    for k in range(ncorr):
        corr += (a[k, 0] + 1j * a[k, 1]) / n ** (k + 1)
    # log-scaled: r_n * R^n n^g = 2 Re[C e^{-i n th} corr]
    return 2 * np.real((Cr + 1j * Ci) * np.exp(-1j * n * th) * corr)

def fit(r, n1, n2, ncorr, p0):
    n = np.arange(n1, n2 + 1).astype(float)
    def res(p):
        R, th, g = p[:3]
        scaled = r[n1:n2 + 1] * R ** n * n ** g
        return scaled - model(p, n, ncorr)
    # residual depends on R,g through scaling too; fine for least squares
    p0 = np.concatenate([p0[:5], np.zeros(2 * ncorr)]) if len(p0) == 5 else p0
    sol = least_squares(res, p0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=20000)
    return sol.x, np.sqrt(np.mean(sol.fun ** 2))

def recurrence_est(r, n):
    """Solve r_n = P r_{n-1} + S r_{n-2}, r_{n+1} = P r_n + S r_{n-1} for (P,S) (assumed locally constant)."""
    A = np.array([[r[n - 1], r[n - 2]], [r[n], r[n - 1]]])
    P, S = np.linalg.solve(A, [r[n], r[n + 1]])
    return P, S

def recurrence_table(r, ns):
    out = []
    for n in ns:
        P, S = recurrence_est(r, n)
        R2 = -1.0 / S if S < 0 else np.nan  # |x|^2 ~ -S  => R ~ 1/sqrt(-S)
        R = 1 / np.sqrt(-S) if S < 0 else np.nan
        costh = P * R / 2
        out.append((n, R, np.arccos(np.clip(costh, -1, 1)) if np.isfinite(R) else np.nan))
    return out

def p0_from_recurrence(r, n):
    _, R, th = recurrence_table(r, [n])[0]
    return np.array([R, th, 1.5, r[n] * R ** n * n ** 1.5, 0.0])

def vp_resid(p, r, n1, n2, ncorr, env):
    """Variable projection: for fixed (R, th, g) solve linear LSQ for complex B_k in
       r_n = Re[ n^-g x^n sum_{k=0..ncorr} B_k n^-k ],  residual weighted by fixed envelope env_n."""
    R, th, g = p
    n = np.arange(n1, n2 + 1).astype(float)
    base = n ** (-g) * np.exp(-n * np.log(R) - 1j * n * th)
    cols = []
    for k in range(ncorr + 1):
        b = base * n ** (-k)
        cols += [b.real, -b.imag]  # Re[(Br + i Bi) b] = Br Re b - Bi Im b
    A = np.array(cols).T / env[:, None]
    y = r[n1:n2 + 1] / env
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    return A @ coef - y, coef

def vp_fit(r, n1, n2, ncorr, p0):
    n = np.arange(n1, n2 + 1).astype(float)
    env = p0[0] ** (-n) * n ** (-p0[2])
    f = lambda p: vp_resid(p, r, n1, n2, ncorr, env)[0]
    sol = least_squares(f, p0, x_scale=[1e-3, 1e-3, 1e-2], xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=5000)
    return sol.x, np.sqrt(np.mean(sol.fun ** 2))
