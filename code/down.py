"""Track the shear critical point c0 down in d with fixed linear steps in d (double precision).
usage: down.py d_start d_end h out.jsonl [wfr0 q2_0]
Jump checks at every step:
  (1) predictor-corrector distance pred = max(|dw|,|dsig|) between the linear predictor and the converged point;
  (2) half-step check: from the same accepted point, two steps of h/2 (each with its own Newton solve) must land on the
      same root as the single step h; reported as 'half_diff' (max over w, sig in thermal units wfr, qfr^2).
A step is accepted only if Newton converged in <= 8 iterations, pred < 0.02 and half_diff < 1e-9; otherwise h is halved.
"""
import sys, json, math
from lib import *

d0 = float(sys.argv[1]); d1 = float(sys.argv[2]); H = float(sys.argv[3]); out = sys.argv[4]
wfr0 = complex(sys.argv[5]) if len(sys.argv) > 5 else complex(1.4436414, -1.0692250)
q20 = complex(sys.argv[6]) if len(sys.argv) > 6 else complex(1.8906469, 1.1711505)
sgn = 1.0 if d1 > d0 else -1.0


def solve(wp, sp, d):
    w, s, h = crit(CNP, wp, sp, d)
    return complex(w), complex(s), h


w, s, h = solve(wfr0 / 2, q20 / 4, d0)
f = open(out, 'w')
rec = dict(d=d0, q2=[(4 * s).real, (4 * s).imag], w=[(2 * w).real, (2 * w).imag], it=len(h), last=h[-1], pred=0.0, half_diff=0.0, h=0.0)
f.write(json.dumps(rec) + "\n"); f.flush(); print(rec, flush=True)
hist = [(d0, w, s)]
d = d0
while sgn * (d1 - d) > 1e-12:
    step = min(H, abs(d1 - d))
    while True:
        dn = d + sgn * step
        if abs(dn - d1) < 1e-12:
            dn = d1
        if len(hist) >= 2:
            (da, wa, sa), (db, wb, sb) = hist[-2], hist[-1]
            r = (dn - db) / (db - da)
            wp = wb + r * (wb - wa); sp = sb + r * (sb - sa)
        else:
            wp, sp = hist[-1][1], hist[-1][2]
        w2, s2, h2 = solve(wp, sp, dn)
        pred = max(abs(w2 - wp), abs(s2 - sp))
        # half-step check (constant predictor from the accepted point for the first half, linear for the second)
        dm = (d + dn) / 2
        wm, sm, hm = solve(hist[-1][1] + (wp - hist[-1][1]) / 2, hist[-1][2] + (sp - hist[-1][2]) / 2, dm)
        wh, sh, hh = solve(2 * wm - hist[-1][1], 2 * sm - hist[-1][2], dn)
        half = max(abs(2 * (wh - w2)), abs(4 * (sh - s2)))
        ok = len(h2) <= 8 and h2[-1] < 1e-6 and pred < 0.02 and half < 1e-9
        if ok:
            break
        step /= 2
        print("halve", dn, len(h2), h2[-1], pred, half, flush=True)
        if step < 1e-4:
            raise SystemExit("stuck")
    d = dn
    hist.append((d, w2, s2))
    rec = dict(d=d, q2=[(4 * s2).real, (4 * s2).imag], w=[(2 * w2).real, (2 * w2).imag], it=len(h2), last=h2[-1], pred=pred,
               half_diff=half, h=step, mid=dict(d=dm, q2=[(4 * sm).real, (4 * sm).imag], w=[(2 * wm).real, (2 * wm).imag]))
    f.write(json.dumps(rec) + "\n"); f.flush(); print(rec, flush=True)
