"""Sector-monodromy census of the hydro sheet inside a disk (DYN1b continuation seat).

Idea: the hydro sheet is the radial continuation of the hydro root from q2 ~ 0 (star domain).  If a hydro-involving
branch point b lies in the sector theta_k < arg q2 < theta_{k+1}, |q2| < R, then the closed loop
  ray theta_k (0 -> R)  +  arc |q2| = R (theta_k -> theta_{k+1})  +  ray theta_{k+1} (R -> 0)
has non-trivial monodromy: the arc-continued value at theta_{k+1} differs from the ray value there.
So: rays on angles theta_0..theta_K in [0, pi] (mirror symmetry q2 -> conj q2, w -> -conj w covers the lower half),
then K short arcs in parallel; mismatch_k = |arc end - ray value| (per sector).  No branch point in the disk
<=> all mismatches at noise level.  Done at two radii in one batch: R_in = |c0| - dr (test) and R_out = |c0| + dr
(positive control: exactly the sector containing arg c0 must light up).
usage: sector.py d absc0 argc0 dr K nstep out.json
"""
import sys, json, math, time
import numpy as np
from lib import *

C = CNP
DEAD = np.zeros(0, bool)


def Fb(w, s, d):
    J = F_eval(C, w, s, d)
    return [tocomplex(J[k]) for k in range(3)]


def newton(w, s, d, it=10, tol=1e-11):
    w = np.array(w, complex)
    for i in range(it):
        F, Fw, F2 = Fb(w, s, d)
        dw = -F / Fw
        w = w + dw
        bad = ~np.isfinite(w)
        if bad.any():
            DEAD[:] = DEAD | bad if DEAD.shape == bad.shape else DEAD
            w = np.where(bad, 0.05 + 0.05j, w); dw = np.where(bad, 0, dw)
        if np.max(np.abs(dw)) < tol:
            break
    F, Fw, F2 = Fb(w, s, d)
    return w, Fw, F2, np.abs(dw)


def follow(w0, qpath, d):
    W = [np.array(w0, complex)]
    w, Fw, F2, last = newton(W[0], qpath[0] / 4, d)
    W = [w]; mj = np.zeros(len(w)); ml = last
    for k in range(1, len(qpath)):
        wg = 3 * W[-1] - 3 * W[-2] + W[-3] if len(W) >= 3 else (2 * W[-1] - W[-2] if len(W) == 2 else W[-1])
        w, Fw, F2, last = newton(wg, qpath[k] / 4, d)
        mj = np.maximum(mj, np.abs(w - wg) / np.abs(Fw / F2)); ml = np.maximum(ml, last)
        W.append(w)
    return W, mj, ml


if __name__ == "__main__":
    d = float(sys.argv[1]); a0 = float(sys.argv[2]); th0 = float(sys.argv[3]); dr = float(sys.argv[4])
    K = int(sys.argv[5]); ns = int(sys.argv[6]); out = sys.argv[7]
    STEP = float(sys.argv[8]) if len(sys.argv) > 8 else 0.01
    T0 = time.time()
    Rin, Rout = a0 - dr, a0 + dr
    th = np.linspace(0.0, math.pi, K + 1)
    DEAD = np.zeros(K + 1, bool)
    # rays: uniform in rho from 0.05 to Rin (n1 steps) then to Rout (n2 steps); step ~0.02
    n1 = int(math.ceil((Rin - 0.05) / STEP)); n2 = max(6, int(math.ceil((Rout - Rin) / (STEP / 2))))
    rhos = list(0.05 + (Rin - 0.05) * np.arange(n1 + 1) / n1) + list(Rin + (Rout - Rin) * np.arange(1, n2 + 1) / n2)
    ph = np.exp(1j * th)
    qpath = [r * ph for r in rhos]
    W, mjr, mlr = follow(-1j * qpath[0] / 4, qpath, d)
    wRin = W[n1]; wRout = W[-1]
    print("rays", time.time() - T0, "dead rays", list(np.where(DEAD)[0]), "max ray jump", float(mjr.max()), "max last", float(mlr.max()), flush=True)
    for k in range(K + 1):
        print("  ray %2d th=%.4f jump=%.3f last=%.1e wRin=%s wRout=%s" % (k, th[k], mjr[k], mlr[k], wRin[k], wRout[k]), flush=True)
    np.savez(out.replace(".json", "_rays.npz"), th=th, rhos=np.array(rhos), W=np.array(W), mj=mjr, ml=mlr)
    res = dict(d=d, absc0=a0, argc0=th0, dr=dr, K=K, ns=ns, Rin=Rin, Rout=Rout, ray_maxjump=float(mjr.max()),
               ray_maxjump_per_angle=[float(x) for x in mjr])
    for R, wR, tag in ((Rin, wRin, 'in'), (Rout, wRout, 'out')):
        pass
    # arcs: both radii batched; sectors k = 0..K-1 ; two step counts for convergence
    Rb = np.concatenate([np.full(K, Rin), np.full(K, Rout)])
    tha = np.concatenate([th[:-1], th[:-1]]); thb = np.concatenate([th[1:], th[1:]])
    w0 = np.concatenate([wRin[:-1], wRout[:-1]]); wref = np.concatenate([wRin[1:], wRout[1:]])
    ends = {}
    for n in (ns, 2 * ns):
        qp = [Rb * np.exp(1j * (tha + (thb - tha) * j / n)) for j in range(n + 1)]
        Wa, mja, mla = follow(w0, qp, d)
        ends[n] = (Wa[-1], mja, mla)
        print("arcs n=%d" % n, time.time() - T0, flush=True)
    e1, mj1, ml1 = ends[ns]; e2, mj2, ml2 = ends[2 * ns]
    mism1 = np.abs(e1 - wref); mism2 = np.abs(e2 - wref); conv = np.abs(e1 - e2)
    for i, tag in ((0, 'in'), (1, 'out')):
        sl = slice(i * K, (i + 1) * K)
        res[tag] = dict(R=float(Rb[i * K]), mismatch_n=[float(x) for x in mism1[sl]], mismatch_2n=[float(x) for x in mism2[sl]],
                        arc_n_vs_2n=[float(x) for x in conv[sl]], arc_maxjump=float(max(mj1[sl].max(), mj2[sl].max())),
                        lit=[int(k) for k in range(K) if mism2[sl][k] > 1e-6],
                        sector_of_c0=int(np.searchsorted(th, th0) - 1), max_mismatch=float(mism2[sl].max()))
        print(tag, json.dumps({k: v for k, v in res[tag].items() if k not in ('mismatch_n', 'arc_n_vs_2n')}), flush=True)
    res['sec'] = time.time() - T0
    json.dump(res, open(out, 'w'), indent=1)
    print("done", res['sec'])
