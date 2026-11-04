"""Blind seat: shear-channel spectral function of the AdS_{d+1} Schwarzschild brane, x = r^d shooting.

Own derivation (see RESULT.md for the steps):
  KK reduction of h_{mu y} = r^2 A_mu gives Maxwell with coupling N = r^{d+1}; gauge-invariant E = q A_t + omega A_x (KS field).
      d/dr[ r^{d+1} f E' / (omega^2 - q^2 f) ] + r^{d-3} E / f = 0,   f = 1 - r^{-d},  r_h = 1, T = d/(4 pi)
  With x = r^d, w = omega/d, sig = q^2/d^2 (so wfr = 2w, qfr^2 = 4 sig) all explicit d cancel except x^{-2/d}:
      d/dx[ x(x-1) E_x / (w^2 - sig + sig/x) ] + x^{1-2/d} E/(x-1) = 0.
  In L = ln x, times (x-1) Dhat, Dhat = alpha x + sig, alpha = w^2 - sig:
      (x-1)^2 Dhat E'' + (x-1)(x Dhat + (x-1) sig) E' + Dhat^2 x^{1-2/d} E = 0      (scaled below by e^{-3L})
  Horizon L=0: exponents +-i w; ingoing = L^{-i w} (Frobenius, g0 = 1).
  Far zone (f -> 1, error e^{-L}):  E'' + E' + alpha e^{-2L/d} E = 0, exact solutions z^{d/2} J_{+-d/2}(k z),
      z = e^{-L/d}, k^2 = d^2 alpha.  Normalisable (Dirichlet) branch: E'/E = lambda = -1 + R/d,
      R = u J_{nu+1}(u)/J_nu(u), nu = d/2, U = u^2 = d^2 alpha e^{-2L/d}, backward recurrence R_{n-1} = U/(2n - R_n).
  Spectral function F(w, sig) = E'(L_m) - lambda E(L_m); QNM <=> F = 0.  Jets in delta = w - w0 give F, F_w, F_ww/2.
Arithmetic: numpy complex128 batches ('np') or numpy object arrays of gmpy2 mpc ('mp').
"""
import math, cmath
import numpy as np
import gmpy2
from gmpy2 import mpc, mpfr

K = 2  # jet order in delta w
GNORM = True
PHI = True


class Ctx:
    def __init__(self, mode='np', bits=53):
        self.mode = mode
        self.bits = bits
        if mode == 'np':
            self.digits = 15.5
            self.exp = np.exp
            self.log = np.log
            self.arr = lambda z: np.asarray(z, dtype=complex)
            self.c = lambda z: complex(z)
            self.pi = math.pi
        else:
            ctx = gmpy2.get_context()
            ctx.precision = bits
            ctx.real_prec = bits
            ctx.imag_prec = bits
            self.digits = bits * math.log10(2)
            ex = np.frompyfunc(gmpy2.exp, 1, 1)
            lg = np.frompyfunc(gmpy2.log, 1, 1)
            self.exp = lambda a: ex(a) if isinstance(a, np.ndarray) else gmpy2.exp(a)
            self.log = lambda a: lg(a) if isinstance(a, np.ndarray) else gmpy2.log(a)
            conv = np.frompyfunc(lambda v: mpc(v), 1, 1)
            self.arr = lambda z: conv(np.asarray(z, dtype=object)).astype(object)
            self.c = lambda z: mpc(z)
            self.pi = gmpy2.const_pi()

    def zeros(self, shape):
        if self.mode == 'np':
            return np.zeros(shape, dtype=complex)
        z = np.empty(shape, dtype=object)
        z.fill(mpc(0))
        return z


# ---------------- jets: list of K+1 arrays ----------------
def jmul(a, b):
    return [sum(a[i] * b[k - i] for i in range(k + 1)) for k in range(K + 1)]


def jinv(a):
    b0 = 1 / a[0]
    b = [b0]
    for k in range(1, K + 1):
        s = sum(a[i] * b[k - i] for i in range(1, k + 1))
        b.append(-s * b0)
    return b


def jadd(a, b):
    return [a[k] + b[k] for k in range(K + 1)]


def jsc(a, c):
    return [a[k] * c for k in range(K + 1)]


# ---------------- coefficient series ----------------
def amps(W, sig):
    """W jet, sig jet (arrays). Returns term lists [(amp_jet, exponent_index)] for c2, c1, c0."""
    al = jadd(jmul(W, W), jsc(sig, -1))
    s = sig
    c2 = [(al, 0), (jadd(s, jsc(al, -2)), -1), (jadd(al, jsc(s, -2)), -2), (s, -3)]
    c1 = [(al, 0), (jadd(jsc(s, 2), jsc(al, -1)), -1), (jsc(s, -3), -2), (s, -3)]
    a2 = jmul(al, al)
    c0 = [(a2, 'a'), (jsc(jmul(al, s), 2), 'b'), (jmul(s, s), 'c')]
    return al, c2, c1, c0


def series(C, terms, L0, N, t, fact):
    """Return array of shape (K+1, N, B): Taylor coeffs in h of sum amp * e^{a(L0+h)}."""
    B = L0.shape[0]
    out = C.zeros((K + 1, N, B))
    for amp, a in terms:
        if a == 'a':
            av = -2 * t
        elif a == 'b':
            av = -1 - 2 * t
        elif a == 'c':
            av = -2 - 2 * t
        else:
            av = a
        if C.mode == 'mp':
            av = mpfr(av) if not isinstance(av, (int,)) else av
        base = C.exp(av * L0)
        pw = [base]
        for n in range(1, N):
            pw.append(pw[-1] * av / n)
        P = np.stack(pw)  # (N, B)
        for k in range(K + 1):
            out[k] += P * amp[k][None, :]
    return out


def conv_at(Cs, Es, k, lo, hi):
    """sum_{j=lo}^{hi} Cs[:, k-j] (jet*) Es[:, j]  -> jet (list of arrays). Cs, Es shape (K+1, N, B)."""
    res = []
    cs = Cs[:, k - hi:k - lo + 1][:, ::-1]  # index j -> k-j
    es = Es[:, lo:hi + 1]
    for m in range(K + 1):
        acc = 0
        for i in range(m + 1):
            acc = acc + (cs[i] * es[m - i]).sum(axis=0)
        res.append(acc)
    return res


def taylor_step(C, L0, h, N, W, sig, t, E0, E1, fact=None):
    al, c2t, c1t, c0t = amps(W, sig)
    c2 = series(C, c2t, L0, N, t, fact)
    c1 = series(C, c1t, L0, N, t, fact)
    c0 = series(C, c0t, L0, N, t, fact)
    B = L0.shape[0]
    e = C.zeros((K + 1, N, B))
    d1 = C.zeros((K + 1, N, B))  # (j+1) e_{j+1}
    d2 = C.zeros((K + 1, N, B))  # (j+1)(j+2) e_{j+2}
    for m in range(K + 1):
        e[m, 0] = E0[m]
        e[m, 1] = E1[m]
        d1[m, 0] = E1[m]
    inv20 = jinv([c2[m, 0] for m in range(K + 1)])
    for k in range(N - 2):
        S = conv_at(c1, d1, k, 0, k)
        S = jadd(S, conv_at(c0, e, k, 0, k))
        if k > 0:
            S = jadd(S, conv_at(c2, d2, k, 0, k - 1))
        z = jmul(inv20, S)
        f = -1.0 / ((k + 1) * (k + 2)) if C.mode == 'np' else mpfr(-1) / ((k + 1) * (k + 2))
        for m in range(K + 1):
            zm = z[m] * f
            e[m, k + 2] = zm
            d1[m, k + 1] = (k + 2) * zm
            d2[m, k] = (k + 1) * (k + 2) * zm
    # evaluate
    Ev, Ed = [], []
    for m in range(K + 1):
        v = e[m, N - 1]
        for n in range(N - 2, -1, -1):
            v = v * h + e[m, n]
        dv = (N - 1) * e[m, N - 1]
        for n in range(N - 2, 0, -1):
            dv = dv * h + n * e[m, n]
        Ev.append(v)
        Ed.append(dv)
    return Ev, Ed


def frobenius(C, W, sig, t, h0, NF):
    """ingoing solution L^nu sum g_n L^n, nu = -i w, g0 = 1; value and derivative at h0 (array)."""
    B = h0.shape[0]
    al, c2t, c1t, c0t = amps(W, sig)
    zero = C.zeros(B)
    Lz = zero.copy()
    c2 = series(C, c2t, Lz, NF + 3, t, None)
    c1 = series(C, c1t, Lz, NF + 3, t, None)
    c0 = series(C, c0t, Lz, NF + 3, t, None)
    A = c2[:, 2:NF + 3]   # A_n = c2_{n+2}
    Bc = c1[:, 1:NF + 2]  # B_n = c1_{n+1}
    Cc = c0[:, 0:NF + 1]
    one = 1 if C.mode == 'np' else mpc(1)
    I = 1j if C.mode == 'np' else mpc(0, 1)
    nu = [-I * W[0], -I * W[1], -I * W[2]]  # W jet = [w0, 1, 0]
    g = C.zeros((K + 1, NF + 1, B))
    Q = C.zeros((K + 1, NF + 1, B))
    R = C.zeros((K + 1, NF + 1, B))
    if GNORM:
        # g0 = (1 - 2 i w): removes the k=1 resonance pole at w = -i/2 (wfr = -i); G = (1-2iw) F is analytic there
        g[0, 0] = one - 2 * I * W[0]
        g[1, 0] = -2 * I + 0 * W[0]
    else:
        g[0, 0] = one
    A0 = [A[m, 0] for m in range(K + 1)]
    B0 = [Bc[m, 0] for m in range(K + 1)]
    C0 = [Cc[m, 0] for m in range(K + 1)]

    def setQR(n):
        gn = [g[m, n] for m in range(K + 1)]
        nn = jadd(nu, [n * one + 0 * nu[0], 0 * nu[0], 0 * nu[0]])
        nm1 = jadd(nn, [-one + 0 * nu[0], 0 * nu[0], 0 * nu[0]])
        r = jmul(gn, nn)
        q = jmul(r, nm1)
        for m in range(K + 1):
            R[m, n] = r[m]
            Q[m, n] = q[m]
    setQR(0)
    for k in range(1, NF + 1):
        S = conv_at(A, Q, k, 0, k - 1)
        S = jadd(S, conv_at(Bc, R, k, 0, k - 1))
        S = jadd(S, conv_at(Cc, g, k, 0, k - 1))
        nn = jadd(nu, [k * one + 0 * nu[0], 0 * nu[0], 0 * nu[0]])
        nm1 = jadd(nn, [-one + 0 * nu[0], 0 * nu[0], 0 * nu[0]])
        den = jadd(jadd(jmul(A0, jmul(nn, nm1)), jmul(B0, nn)), C0)
        gk = jmul(jinv(den), S)
        for m in range(K + 1):
            g[m, k] = -gk[m]
        setQR(k)
    # sum at h0
    sv, sd = [], []
    for m in range(K + 1):
        v = g[m, NF]
        for n in range(NF - 1, -1, -1):
            v = v * h0 + g[m, n]
        sv.append(v)
        # R_n = g_n (n+nu): derivative sum R_n h0^{n-1}
        dv = R[m, NF]
        for n in range(NF - 1, -1, -1):
            dv = dv * h0 + R[m, n]
        sd.append(dv / h0)
    lh = C.log(h0)
    base = C.exp(nu[0] * lh)
    hj = [base, base * (-I * lh), base * (-I * lh) * (-I * lh) / 2]
    return jmul(hj, sv), jmul(hj, sd)


def bessel_lambda(C, al, Lend, d, M):
    """lambda jet = -1 + R_{d/2}/d, U = d^2 alpha e^{-2 Lend/d}."""
    fac = (d * d) * C.exp(-2 * Lend / d) if C.mode == 'np' else (mpfr(d) ** 2) * C.exp(-2 * Lend / mpfr(d))
    U = jsc(al, fac)
    nu = d / 2.0 if C.mode == 'np' else mpfr(d) / 2
    n = nu + M
    R = jsc(U, 1 / (2 * (n + 1)))
    for j in range(M):
        nn = nu + M - j
        den = [2 * nn - R[0], -R[1], -R[2]]
        R = jmul(U, jinv(den))
    return [R[0] / d - 1, R[1] / d, R[2] / d]


def jlog(a):
    """log of a jet (K=2)."""
    L0 = np.log(a[0]) if not isinstance(a[0], np.ndarray) or a[0].dtype != object else np.frompyfunc(gmpy2.log, 1, 1)(a[0])
    r1 = a[1] / a[0]
    r2 = a[2] / a[0]
    return [L0, r1, r2 - r1 * r1 / 2]


def jexp(a, C):
    e0 = C.exp(a[0])
    return [e0, e0 * a[1], e0 * (a[2] + a[1] * a[1] / 2)]


def bessel_phi(C, al, Lend, d, M, pair=None):
    """Pole-free matching pieces: Phi = prod_{n=nu+1}^{nu+M} (2n - R_n)/(2n)  (= J_nu(u)/leading-term x nonvanishing),
    returns (A, B) jets with Ftilde = A (E' + E) - B E, A = Phi, B = Phi R_nu / d.  np mode: overall real rescale
    exp(-s) with s = Re log P' (shared inside pairs k, k+pair so finite differences stay consistent)."""
    fac = (d * d) * C.exp(-2 * Lend / d) if C.mode == 'np' else (mpfr(d) ** 2) * C.exp(-2 * Lend / mpfr(d))
    U = jsc(al, fac)
    nu = d / 2.0 if C.mode == 'np' else mpfr(d) / 2
    n = nu + M
    R = jsc(U, 1 / (2 * (n + 1)))
    if C.mode == 'np':
        logP = [0 * U[0], 0 * U[0], 0 * U[0]]
    else:
        P = [U[0] * 0 + 1, U[0] * 0, U[0] * 0]
    last = None
    for j in range(M):
        nn = nu + M - j
        den = [2 * nn - R[0], -R[1], -R[2]]
        if j == M - 1:
            last = jsc(den, 1 / (2 * nn))
        else:
            dn = jsc(den, 1 / (2 * nn))
            if C.mode == 'np':
                logP = jadd(logP, jlog(dn))
            else:
                P = jmul(P, dn)
        R = jmul(U, jinv(den))
    if C.mode == 'np':
        sR = logP[0].real.copy()
        if pair is not None:
            sR[pair:] = sR[:len(sR) - pair]
        logP = [logP[0] - sR, logP[1], logP[2]]
        P = jexp(logP, C)
    A = jmul(P, last)
    B = jsc(jmul(P, U), 1 / (2 * (nu + 1) * d))
    return A, B


def sing_points(Ls):
    tp = 2j * math.pi
    return [0 * Ls, 0 * Ls + tp, 0 * Ls - tp, 0 * Ls + 2 * tp, 0 * Ls - 2 * tp, Ls, Ls + tp, Ls - tp]


def F_eval(C, w0, sig0, d, digits=None, kappa=0.25, hmax=1.0, Lm0=None, Mextra=None, ret_info=False, pair=None):
    """w0, sig0: arrays (complex128 values for geometry; converted to context). Returns jet [F, F_w, F_ww/2] (arrays)."""
    w0l = list(np.atleast_1d(np.asarray(w0, dtype=object)).ravel())
    s0l = list(np.atleast_1d(np.asarray(sig0, dtype=object)).ravel())
    w0c = np.array([complex(v) for v in w0l])
    s0c = np.array([complex(v) for v in s0l])
    B = w0c.shape[0]
    if digits is None:
        digits = C.digits
    t = 1.0 / d
    if C.mode == 'mp':
        t = mpfr(1) / mpfr(d)
    # geometry in complex128
    al0 = w0c ** 2 - s0c
    with np.errstate(divide='ignore', invalid='ignore'):
        xs = -s0c / al0
        Ls = np.log(xs)
    Ls = np.where(np.isfinite(Ls), Ls, 1e6 + 0j)
    s = np.where(Ls.imag > 0, -1.0, 1.0)
    RF = np.minimum.reduce([np.abs(Ls), np.abs(Ls - 2j * math.pi), np.abs(Ls + 2j * math.pi), np.full(B, 2 * math.pi)])
    r0 = np.minimum(0.4 * RF, 0.5)
    ph = np.exp(1j * s * math.pi / 4)
    h0 = r0 * ph
    A = 1.5 * math.sqrt(2) * ph
    if Lm0 is None:
        Lm0 = digits * math.log(10) + 8
    Lm = Lm0 + min(30.0, max(0.0, float(np.max(Ls.real[np.abs(Ls) < 1e5])) if np.any(np.abs(Ls) < 1e5) else 0.0))
    N = int(math.ceil(digits * math.log(10) / math.log(1 / kappa))) + 6
    NF = int(math.ceil(digits * math.log(10) / math.log(2.5))) + 10
    # segment 1: radial geometric
    qrat = 1 + kappa * 0.7
    n1 = int(math.ceil(np.max(np.log(np.abs(A) / r0)) / math.log(qrat)))
    n1 = max(n1, 1)
    ratio = (np.abs(A) / r0) ** (1.0 / n1)
    pts1 = [h0 * ratio ** j for j in range(n1 + 1)]
    # segment 2: horizontal common real parts
    sp = sing_points(Ls)
    xs2 = [1.5]
    while xs2[-1] < Lm - 1e-12:
        x = xs2[-1]
        P = x + 1.5j * s
        dist = np.min(np.abs(np.stack([P - q for q in sp])), axis=0)
        hh = min(float(np.min(kappa * dist)), hmax)
        xs2.append(min(x + hh, Lm))
    pts2 = [x + 1.5j * s for x in xs2]
    pts3 = [Lm + 1.5j * s * (1 - j / 3.0) for j in range(1, 4)]
    path = pts1 + pts2[1:] + pts3
    # context arrays
    if C.mode == 'np':
        W = [w0c.copy(), np.ones(B, dtype=complex), np.zeros(B, dtype=complex)]
        S = [s0c.copy(), np.zeros(B, dtype=complex), np.zeros(B, dtype=complex)]
    else:
        W = [C.arr(np.array(w0l, dtype=object)), C.arr(np.ones(B)), C.arr(np.zeros(B))]
        S = [C.arr(np.array(s0l, dtype=object)), C.arr(np.zeros(B)), C.arr(np.zeros(B))]
    tt = t
    Ev, Ed = frobenius(C, W, S, tt, C.arr(path[0]), NF)
    Lcur = C.arr(path[0])
    for P in path[1:]:
        Pn = C.arr(P)
        h = Pn - Lcur
        Ev, Ed = taylor_step(C, Lcur, h, N, W, S, tt, Ev, Ed)
        Lcur = Pn
    al = jadd(jmul(W, W), jsc(S, -1))
    u_abs = d * np.sqrt(np.abs(al0)) * math.exp(-Lm / d)
    if Mextra is None:
        Mextra = 0
    M = int(2 * np.max(u_abs) + 3 * digits + 60) + Mextra
    if PHI:
        Aj, Bj = bessel_phi(C, al, Lcur, d, M, pair=pair)
        Fj = jadd(jmul(Aj, jadd(Ed, Ev)), jsc(jmul(Bj, Ev), -1))
    else:
        lam = bessel_lambda(C, al, Lcur, d, M)
        Fj = jadd(Ed, jsc(jmul(lam, Ev), -1))
    if ret_info:
        return Fj, dict(N=N, NF=NF, steps=len(path) - 1, Lm=Lm, M=M)
    return Fj


def tocomplex(a):
    return np.array([complex(v) for v in np.asarray(a).ravel()])
