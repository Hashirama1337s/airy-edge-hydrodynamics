"""Free conjugate-pair Darboux fits with optional second (real-axis) singularity."""
import numpy as np, sys, json
from scipy.optimize import least_squares
from darboux import load, recurrence_table

def design(p, n, nc, second, nc2):
    R, th, g = p[:3]
    base = n ** (-g) * np.exp(-n * np.log(R) - 1j * n * th)
    cols = []
    for k in range(nc + 1):
        b = base * n ** (-k); cols += [b.real, -b.imag]
    if second:
        R2, g2 = p[3:5]
        b2 = n ** (-g2) * np.exp(-n * np.log(R2)) * (-1.0) ** n
        for k in range(nc2 + 1):
            cols += [b2 * n ** (-k)]
    return np.array(cols).T

def fit(r, n1, n2, nc, p0, second=False, nc2=1, env=None):
    n = np.arange(n1, n2 + 1).astype(float)
    if env is None:
        env = p0[0] ** (-n) * n ** (-p0[2])
    y = r[n1:n2 + 1] / env
    def res(p):
        A = design(p, n, nc, second, nc2) / env[:, None]
        c, *_ = np.linalg.lstsq(A, y, rcond=None)
        return A @ c - y
    xs = [1e-3, 1e-3, 1e-2] + ([1e-3, 1e-2] if second else [])
    sol = least_squares(res, p0, x_scale=xs, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=5000)
    return sol.x, np.sqrt(np.mean(sol.fun ** 2))
