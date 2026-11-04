"""RC seat: adaptive sector-monodromy census of the shear hydro sheet (fix of DYN1b/blind/sector.py root jumps).

Same idea as sector.py (copied solver qnmx.py/lib.py, unchanged): hydro-root rays at K+1 angles in [0, pi], then the
K short arcs at radius R between neighbouring rays; mismatch_k = |arc end - ray value at theta_{k+1}| (qnmx w units,
wfr = 2 w).  Radii R_in = |c0| - dr (test) and R_out = |c0| + dr (positive control).

Changes vs sector.py (all paths batched in ONE F_eval call per Newton iteration, each path with its own step):
  * adaptive steps: predictor = Lagrange extrapolation through the last <= 4 accepted points (non-uniform t);
    accept a step only if Newton converged (|dw| < NTOL in <= NIT its) AND the predictor error err = |w - w_pred|
    satisfies err <= min(tol, FRAC * sp), sp = |F_w / (F_ww/2)| = local distance to the nearest other root
    (quadratic model), AND sp did not drop by more than 3x over the step while sp < 0.02 (v1: any 3x change; v2: drop).  Else: halve h and redo (jump detector).
    h grows/shrinks with (target/err)^(1/(order+1)), capped by hmax.
  * two fully independent runs: run A (tol, hmax) and run B (tol/16, hmax/2) - rays AND arcs.  Arcs of run A use
    hmax = dtheta/n, arcs of run B dtheta/(2n): these are the BAR's "n" and "2n" arc runs.  Ray A vs ray B values at
    R_in/R_out are compared (independent root-jump check).
usage: rc.py d absc0 argc0 dr K n tolA out.json      |  rc.py probe d theta rho_max seconds tol
"""
import sys, json, math, time
import numpy as np
from lib import CNP, F_eval, tocomplex

NTOL = 1e-10
NIT = 8
FRAC = 0.05
HMIN = 1e-9
RHO0 = 0.02


def jet(w, s, d):
    J = F_eval(CNP, w, s, d)
    return [tocomplex(J[k]) for k in range(3)]


def qof(kind, par, t):
    """kind 0 = ray (t = rho, par = theta); kind 1 = arc (t = theta, par = R)."""
    return np.where(kind == 0, t * np.exp(1j * par), par * np.exp(1j * t))


def extrap(T, W, tn):
    """Lagrange extrapolation through points (T[j], W[j]) evaluated at tn. T, W lists of scalars."""
    m = len(T)
    out = 0
    for j in range(m):
        L = 1.0
        for k in range(m):
            if k != j:
                L *= (tn - T[k]) / (T[j] - T[k])
        out += L * W[j]
    return out


def run(kind, par, t0, stops, w0, d, tol, hmax, h0, label="", tlimit=None, verbose=True):
    """Continue P paths. stops[i] = increasing list of t values (last = end). Returns dict with values at stops + diag."""
    P = len(kind)
    kind = np.asarray(kind); par = np.asarray(par, float)
    t = np.array(t0, float); h = np.array(h0, float); hm = np.array(hmax, float)
    tol = np.broadcast_to(np.asarray(tol, float), (P,)).copy()
    hist = [[] for _ in range(P)]  # list of (t, w)
    vals = [[] for _ in range(P)]
    si = np.zeros(P, int)
    active = np.ones(P, bool)
    stuck = np.zeros(P, bool)
    # diagnostics
    maxjump = np.zeros(P); minsp = np.full(P, np.inf); nstep = np.zeros(P, int); nrej = np.zeros(P, int)
    maxres = np.zeros(P); maxerr = np.zeros(P)
    lastsp = np.full(P, np.nan)
    # initial Newton at t0
    w = np.array(w0, complex)
    q = qof(kind, par, t)
    ok, w, sp, res = newton(w, q / 4, d)
    for i in range(P):
        hist[i].append((t[i], w[i]))
        lastsp[i] = min(sp[i], 1.0) if not np.isnan(sp[i]) else 1.0
        minsp[i] = lastsp[i]
        if not ok[i]:
            stuck[i] = True; active[i] = False
    T0 = time.time(); it = 0; ncall = 0
    while active.any():
        it += 1
        idx = np.where(active)[0]
        tn = np.empty(len(idx)); wp = np.empty(len(idx), complex); order = np.empty(len(idx), int)
        for a, i in enumerate(idx):
            tgt = stops[i][si[i]]
            tn[a] = min(t[i] + h[i], tgt)
            Hs = hist[i][-4:]
            order[a] = len(Hs) - 1
            wp[a] = extrap([x[0] for x in Hs], [x[1] for x in Hs], tn[a])
        qn = qof(kind[idx], par[idx], tn)
        okn, wn, spn, resn = newton(wp.copy(), qn / 4, d)
        ncall += 1
        for a, i in enumerate(idx):
            err = abs(wn[a] - wp[a])
            spa = min(spn[a], 1.0) if not np.isnan(spn[a]) else 1.0  # F2 ~ 0 => no nearby root in the quadratic model
            target = FRAC * spa if order[a] == 0 else min(tol[i], FRAC * spa)
            # jump detector: a sudden DROP of the local root spacing (>3x) over one step => redo with h/2
            # (only in the crowded regime spa < 0.02: at small q2, F_ww crosses zero and |Fw/F2| is noise-dominated)
            good = okn[a] and np.isfinite(err) and err <= target and (spa > lastsp[i] / 3 or spa > 0.02)
            if not good:
                nrej[i] += 1
                h[i] *= 0.5
                if h[i] < HMIN:
                    stuck[i] = True; active[i] = False
                continue
            # accept
            t[i] = tn[a]
            hist[i].append((tn[a], wn[a]))
            if len(hist[i]) > 6:
                hist[i] = hist[i][-6:]
            nstep[i] += 1
            jr = err / spa
            if order[a] >= 1:
                maxjump[i] = max(maxjump[i], jr)
                maxerr[i] = max(maxerr[i], err)
            minsp[i] = min(minsp[i], spa); lastsp[i] = spa; maxres[i] = max(maxres[i], resn[a])
            fac = 2.0 if err == 0 else min(2.0, max(0.3, 0.8 * (target / err) ** (1.0 / (order[a] + 1))))
            if order[a] == 0:
                fac = min(fac, 1.5)
            h[i] = min(h[i] * fac, hm[i])
            if abs(t[i] - stops[i][si[i]]) < 1e-15:
                vals[i].append(wn[a])
                si[i] += 1
                if si[i] >= len(stops[i]):
                    active[i] = False
        if verbose and (it % 25 == 0):
            prog = np.array([(t[i] - t0[i]) / (stops[i][-1] - t0[i]) for i in range(P)])
            print("  [%s] it %d calls %d %.0fs active %d minprog %.4f rej %d" % (label, it, ncall, time.time() - T0,
                  active.sum(), prog.min(), nrej.sum()), flush=True)
        if tlimit is not None and time.time() - T0 > tlimit:
            break
    return dict(vals=vals, maxjump=maxjump, minsp=minsp, nstep=nstep, nrej=nrej, maxres=maxres, maxerr=maxerr,
                stuck=stuck, t=t, sec=time.time() - T0, calls=ncall)


def newton(w, s, d):
    """Batched Newton in w at fixed s. Returns ok, w, sp=|Fw/F2| (at last iterate), last |dw|."""
    w = np.array(w, complex); s = np.asarray(s, complex)
    P = len(w)
    ok = np.zeros(P, bool); sp = np.full(P, np.nan); res = np.full(P, np.inf)
    todo = np.arange(P)
    for k in range(NIT):
        if len(todo) == 0:
            break
        with np.errstate(all='ignore'):
            F, Fw, F2 = jet(w[todo], s[todo], d)
            dw = -F / Fw
        fin = np.isfinite(dw) & np.isfinite(w[todo])
        dw = np.where(fin, dw, 0)
        w[todo] = w[todo] + dw
        with np.errstate(all='ignore'):
            sp[todo] = np.abs(Fw / F2)
        res[todo] = np.where(fin, np.abs(dw), np.inf)
        conv = fin & (np.abs(dw) < NTOL)
        ok[todo[conv]] = True
        todo = todo[~conv & fin]
    return ok, w, sp, res


def census(d, a0, th0, dr, K, n, tolA):
    T0 = time.time()
    Rin, Rout = a0 - dr, a0 + dr
    th = np.linspace(0.0, math.pi, K + 1)
    kc = int(np.searchsorted(th, th0) - 1)
    # ---- rays: run A and run B batched
    nr = K + 1
    kind = np.zeros(2 * nr, int); par = np.concatenate([th, th])
    tolv = np.concatenate([np.full(nr, tolA), np.full(nr, tolA / 16)])
    hmax = np.concatenate([np.full(nr, 0.05), np.full(nr, 0.025)])
    q0 = RHO0 * np.exp(1j * par)
    w0 = -1j * q0 / 4
    stops = [[Rin, Rout]] * (2 * nr)
    R = run(kind, par, np.full(2 * nr, RHO0), stops, w0, d, tolv, hmax, np.full(2 * nr, 0.005), label="rays d=%g" % d)
    print("rays done %.0fs calls %d stuck %s" % (R['sec'], R['calls'], list(np.where(R['stuck'])[0])), flush=True)
    if R['stuck'].any():
        raise SystemExit("STUCK rays: %s" % list(np.where(R['stuck'])[0]))
    VA = np.array(R['vals'][:nr]); VB = np.array(R['vals'][nr:])  # (nr, 2) at Rin, Rout
    rayAB = np.abs(VA - VB)
    rays = dict(theta=th.tolist(), maxjump_A=R['maxjump'][:nr].tolist(), maxjump_B=R['maxjump'][nr:].tolist(),
                minsp_A=R['minsp'][:nr].tolist(), nstep_A=R['nstep'][:nr].tolist(), nstep_B=R['nstep'][nr:].tolist(),
                nrej_A=R['nrej'][:nr].tolist(), nrej_B=R['nrej'][nr:].tolist(), maxerr_A=R['maxerr'][:nr].tolist(),
                maxres=R['maxres'].max(), AB_diff_Rin=rayAB[:, 0].tolist(), AB_diff_Rout=rayAB[:, 1].tolist(),
                wA_Rin=[[v.real, v.imag] for v in VA[:, 0]], wA_Rout=[[v.real, v.imag] for v in VA[:, 1]],
                sec=R['sec'], calls=R['calls'])
    for k in range(nr):
        print("  ray %2d th=%.4f jumpA=%.2e jumpB=%.2e minsp=%.2e stepsA=%d rejA=%d rejB=%d |A-B| Rin=%.1e Rout=%.1e" % (
            k, th[k], R['maxjump'][k], R['maxjump'][nr + k], R['minsp'][k], R['nstep'][k], R['nrej'][k], R['nrej'][nr + k],
            rayAB[k, 0], rayAB[k, 1]), flush=True)
    # ---- arcs: (in, out) x (n from ray A, 2n from ray B), all batched
    dth = th[1] - th[0]
    kinds, pars, t0s, stopsA, w0s, tols, hms, tags = [], [], [], [], [], [], [], []
    for run_i, (V, nn, tl) in enumerate(((VA, n, tolA), (VB, 2 * n, tolA / 16))):
        for ri, Rr in enumerate((Rin, Rout)):
            for k in range(K):
                kinds.append(1); pars.append(Rr); t0s.append(th[k]); stopsA.append([th[k + 1]]); w0s.append(V[k, ri])
                tols.append(tl); hms.append(dth / nn); tags.append((run_i, ri, k))
    P = len(kinds)
    A = run(np.array(kinds), np.array(pars), np.array(t0s), stopsA, np.array(w0s), d, np.array(tols), np.array(hms),
            np.array(hms) / 8, label="arcs d=%g" % d)
    print("arcs done %.0fs calls %d stuck %s" % (A['sec'], A['calls'], list(np.where(A['stuck'])[0])), flush=True)
    mism = np.full((2, 2, K), np.nan); arcjump = np.zeros((2, 2, K)); arcsteps = np.zeros((2, 2, K), int)
    arcrej = np.zeros((2, 2, K), int); arcstuck = np.zeros((2, 2, K), bool); ends = np.full((2, 2, K), np.nan + 0j)
    for p, (run_i, ri, k) in enumerate(tags):
        V = VA if run_i == 0 else VB
        arcjump[run_i, ri, k] = A['maxjump'][p]; arcsteps[run_i, ri, k] = A['nstep'][p]; arcrej[run_i, ri, k] = A['nrej'][p]
        arcstuck[run_i, ri, k] = A['stuck'][p]
        if not A['stuck'][p]:
            ends[run_i, ri, k] = A['vals'][p][0]
            mism[run_i, ri, k] = abs(A['vals'][p][0] - V[k + 1, ri])
    out = dict(d=d, absc0=a0, argc0=th0, dr=dr, K=K, n=n, tolA=tolA, Rin=Rin, Rout=Rout, sector_of_c0=kc, rays=rays)
    for ri, tag in ((0, 'in'), (1, 'out')):
        out[tag] = dict(R=[Rin, Rout][ri], mismatch_n=mism[0, ri].tolist(), mismatch_2n=mism[1, ri].tolist(),
                        arc_end_n_vs_2n=np.abs(ends[0, ri] - ends[1, ri]).tolist(),
                        arc_maxjump_n=arcjump[0, ri].tolist(), arc_maxjump_2n=arcjump[1, ri].tolist(),
                        arc_steps_n=arcsteps[0, ri].tolist(), arc_steps_2n=arcsteps[1, ri].tolist(),
                        arc_rej_n=arcrej[0, ri].tolist(), arc_rej_2n=arcrej[1, ri].tolist(),
                        arc_stuck=np.where(arcstuck[:, ri].any(0))[0].tolist(),
                        lit_1e6_n=[k for k in range(K) if not mism[0, ri, k] <= 1e-6],
                        lit_1e6_2n=[k for k in range(K) if not mism[1, ri, k] <= 1e-6],
                        above_1e9_n=[k for k in range(K) if not mism[0, ri, k] <= 1e-9],
                        above_1e9_2n=[k for k in range(K) if not mism[1, ri, k] <= 1e-9],
                        max_mismatch_n=float(np.nanmax(mism[0, ri])), max_mismatch_2n=float(np.nanmax(mism[1, ri])),
                        max_mismatch_other_n=float(np.nanmax(np.delete(mism[0, ri], kc))),
                        max_mismatch_other_2n=float(np.nanmax(np.delete(mism[1, ri], kc))),
                        mismatch_c0_n=float(mism[0, ri, kc]), mismatch_c0_2n=float(mism[1, ri, kc]))
        o = out[tag]
        print(tag, "R=%.10f max_n=%.2e max_2n=%.2e lit_n=%s lit_2n=%s >1e-9 n=%s 2n=%s c0sec=%d m_c0 n=%.6e 2n=%.6e other max n=%.2e 2n=%.2e" % (
            o['R'], o['max_mismatch_n'], o['max_mismatch_2n'], o['lit_1e6_n'], o['lit_1e6_2n'], o['above_1e9_n'],
            o['above_1e9_2n'], kc, o['mismatch_c0_n'], o['mismatch_c0_2n'], o['max_mismatch_other_n'],
            o['max_mismatch_other_2n']), flush=True)
    out['arcs_sec'] = A['sec']; out['arcs_calls'] = A['calls']
    out['sec'] = time.time() - T0
    return out


if __name__ == "__main__":
    if sys.argv[1] == "probe":
        d = float(sys.argv[2]); th = float(sys.argv[3]); rmax = float(sys.argv[4]); tl = float(sys.argv[5])
        tol = float(sys.argv[6])
        kind = np.array([0]); par = np.array([th])
        R = run(kind, par, np.array([RHO0]), [[rmax]], -1j * RHO0 * np.exp(1j * par) / 4, d, tol, np.array([0.05]),
                np.array([0.005]), label="probe", tlimit=tl)
        print("probe: reached rho=%.5f of %.5f in %.1fs, calls %d, steps %d, rej %d, maxjump %.2e, minsp %.2e, stuck %s" % (
            R['t'][0], rmax, R['sec'], R['calls'], R['nstep'][0], R['nrej'][0], R['maxjump'][0], R['minsp'][0], R['stuck'][0]))
        if R['vals'][0]:
            print("w_end", R['vals'][0][0])
        sys.exit()
    d = float(sys.argv[1]); a0 = float(sys.argv[2]); th0 = float(sys.argv[3]); dr = float(sys.argv[4])
    K = int(sys.argv[5]); n = int(sys.argv[6]); tolA = float(sys.argv[7]); outf = sys.argv[8]
    res = census(d, a0, th0, dr, K, n, tolA)
    json.dump(res, open(outf, 'w'), indent=1)
    print("done %.0fs" % res['sec'])
