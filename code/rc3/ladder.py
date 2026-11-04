"""Ladder fit: r_n = sum_{k=1..K} Re[ zeta_k^{-n} (C_k s_n + D_k t_n) ],
s_n = [x^n](1-x)^{1/2}, t_n = [x^n](1-x)^{3/2}  (beta FIXED = 1/2, plus the analytic-times-sqrt correction).
Variable projection: amplitudes C_k, D_k (complex) by linear LSQ; (R_k, theta_k) by nonlinear LSQ, multistart."""
import numpy as np
from scipy.optimize import least_squares
from scipy.special import gammaln

def binom_coef(a, n):
    # [x^n](1-x)^a = Gamma(n-a)/(Gamma(-a) Gamma(n+1)), computed with signs via recurrence
    c = np.empty(len(n));
    out = np.ones(int(n.max()) + 1)
    for m in range(1, len(out)):
        out[m] = out[m - 1] * (m - 1 - a) / m
    return out[n.astype(int)]

def design(par, n, nord=2):
    K = len(par) // 2
    cols = []
    s = binom_coef(0.5, n); t = binom_coef(1.5, n); v = binom_coef(2.5, n)
    bases = [s, t, v][:nord]
    for k in range(K):
        R, th = par[2 * k], par[2 * k + 1]
        ph = np.exp(-n * np.log(R) - 1j * n * th)
        for b in bases:
            bb = ph * b
            cols += [bb.real, -bb.imag]
    return np.array(cols).T

def resid(par, r, n, env, nord):
    A = design(par, n, nord) / env[:, None]
    y = r / env
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    return A @ c - y

def fit_K(r_all, n1, n2, K, starts, nord=2, R_env=None):
    n = np.arange(n1, n2 + 1).astype(float)
    r = r_all[n1:n2 + 1]
    if R_env is None:
        R_env = starts[0][0]
    env = R_env ** (-n) * n ** (-1.5)
    best = None
    for p0 in starts:
        lb = []; ub = []
        for k in range(K):
            lb += [1.0, 0.0]; ub += [4.0, np.pi]
        p0 = np.clip(p0, np.array(lb) + 1e-6, np.array(ub) - 1e-6)
        try:
            sol = least_squares(resid, p0, args=(r, n, env, nord), bounds=(lb, ub),
                                xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=3000)
        except Exception:
            continue
        rms = np.sqrt(np.mean(sol.fun ** 2))
        if best is None or rms < best[1]:
            best = (sol.x, rms)
    par, rms = best
    pairs = sorted([(par[2 * k], par[2 * k + 1]) for k in range(K)])
    return pairs, rms

def make_starts(R0, th0, K, nstart, rng):
    starts = []
    for i in range(nstart):
        p = []
        for k in range(K):
            if k == 0:
                Rk = R0 * (1 + 0.01 * rng.standard_normal()); tk = th0 + 0.02 * rng.standard_normal()
            else:
                Rk = R0 * (1 + rng.uniform(0.005, 0.12)); tk = th0 + rng.uniform(-0.25, 0.25)
            p += [Rk, min(max(tk, 0.01), np.pi - 0.01)]
        starts.append(np.array(p))
    return starts

def ladder(r_all, n1, n2, R0, th0, Kmax=4, nstart=24, seed=1, nord=2, improve=3.0):
    rng = np.random.default_rng(seed)
    res = {}
    for K in range(1, Kmax + 1):
        pairs, rms = fit_K(r_all, n1, n2, K, make_starts(R0, th0, K, nstart, rng), nord=nord, R_env=R0)
        res[K] = (pairs, rms)
    # selection: accept K+1 only if rms improves by factor > improve
    Ksel = 1
    for K in range(2, Kmax + 1):
        if res[K][1] * improve < res[Ksel][1]:
            Ksel = K
    return Ksel, res

def contributions(r_all, n1, n2, pairs, R_env, nord=2):
    """relative contribution of each pair at n=n2 (|term_k(n2)| / max_k)."""
    n = np.arange(n1, n2 + 1).astype(float)
    par = np.array([v for p in pairs for v in p])
    env = R_env ** (-n) * n ** (-1.5)
    A = design(par, n, nord)
    c, *_ = np.linalg.lstsq(A / env[:, None], r_all[n1:n2 + 1] / env, rcond=None)
    ncol = 2 * nord
    contrib = []
    for k in range(len(pairs)):
        term = A[-1, k * ncol:(k + 1) * ncol] @ c[k * ncol:(k + 1) * ncol]
        # magnitude of complex term: rebuild complex amplitude
        cc = c[k * ncol:(k + 1) * ncol]
        R, th = pairs[k]
        mag = 0
        for j, a in enumerate([0.5, 1.5, 2.5][:nord]):
            amp = cc[2 * j] + 1j * cc[2 * j + 1]
            mag += abs(amp * binom_coef(a, np.array([n2]))[0]) * R ** (-n2)
        contrib.append(mag)
    contrib = np.array(contrib)
    return contrib / contrib.max()
