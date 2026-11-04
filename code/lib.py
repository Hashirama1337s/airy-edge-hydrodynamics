"""Newton drivers on the spectral function F(w, sig; d) of qnmx.py.  Thermal units: wfr = 2 w, qfr^2 = 4 sig."""
import numpy as np, math
import qnmx
from qnmx import Ctx, F_eval, tocomplex

CNP = Ctx('np')


def root_w(C, w, sig, d, tol=1e-13, it=30, **kw):
    """Newton in w at fixed sig (batched, complex128). returns w, jet."""
    w = np.asarray(w, dtype=complex).copy()
    sig = np.asarray(sig, dtype=complex)
    for i in range(it):
        J = F_eval(C, w, sig, d, **kw)
        F = tocomplex(J[0]); Fw = tocomplex(J[1])
        dw = -F / Fw
        w = w + dw
        if np.max(np.abs(dw)) < tol:
            break
    J = F_eval(C, w, sig, d, **kw)
    return w, J


def crit(C, w, sig, d, tol=None, it=30, hs=None, verbose=False, **kw):
    """Newton on (F, F_w) = 0 in (w, sig).  Jacobian sig-column by forward difference (only affects rate)."""
    if C.mode == 'np':
        w = complex(w); sig = complex(sig)
        if tol is None:
            tol = 1e-12
        if hs is None:
            hs = 1e-7
    else:
        from gmpy2 import mpc, mpfr
        w = mpc(w); sig = mpc(sig)
        if tol is None:
            tol = 10 ** (-(C.digits - 4))
        if hs is None:
            hs = mpfr(10) ** (-int(C.digits / 2))
    hist = []
    for i in range(it):
        J = F_eval(C, np.array([w, w], dtype=object), np.array([sig, sig + hs], dtype=object), d, pair=1, **kw)
        F0, F1 = J[0][0], J[0][1]
        Fw0, Fw1 = J[1][0], J[1][1]
        Fww0 = 2 * J[2][0]
        a11 = Fw0; a12 = (F1 - F0) / hs; a21 = Fww0; a22 = (Fw1 - Fw0) / hs
        det = a11 * a22 - a12 * a21
        dxw = -(a22 * F0 - a12 * Fw0) / det
        dxs = -(-a21 * F0 + a11 * Fw0) / det
        w = w + dxw; sig = sig + dxs
        step = max(abs(complex(dxw)), abs(complex(dxs)))
        hist.append(step)
        if verbose:
            print(i, complex(w), complex(sig), step, flush=True)
        if step < tol:
            break
        if len(hist) >= 3 and step < (1e-9 if C.mode == 'np' else 1e-8) and step > 0.3 * hist[-2]:
            break  # double-precision noise floor reached
    return w, sig, hist
