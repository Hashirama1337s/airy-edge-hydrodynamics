"""Readings of the BAR-RC3 ladder fits (paper Section 5.3): for each of the 10 fits at d = 2048 and 8192 (5 windows x 2
Cauchy circles), the pair reported by the seat (largest contribution at the window end), the nearest significant pair
(contribution > 1e-3, the fit driver's threshold), and any weaker pair inside |c0|.  Targets c0 as sealed in BAR-RC3.
Sealed lines: HOLDS if |R - |c0||/|c0| < 2e-3 and angle error < 5e-3; FAILED if the relative R error > 5e-3.
Usage (from the top folder of the deposit):  python code/rc3_pairs.py
"""
import cmath, json

C0 = {'2048': complex(-1.9154981851895594, 0.42924741091280705),
      '8192': complex(-1.94836923521368989578, 0.26885790575211286270)}
for d, c0 in C0.items():
    R0, th0 = abs(c0), cmath.phase(c0)
    fits = json.load(open("data/RC3/fits_%s.json" % d))
    n_weak, n_angle, weak_all = 0, 0, []
    print("d = %s, |c0| = %.10f, arg c0 = %.7f" % (d, R0, th0))
    for key, v in fits.items():
        sig = [(p, c) for p, c in zip(v['pairs'], v['contrib']) if c > 1e-3]
        rep = max(sig, key=lambda x: x[1])[0]
        near = min(sig, key=lambda x: x[0][0])[0]
        weak = [p[0] for p, c in sig if p is not rep and p[0] < R0]
        n_weak += bool(weak)
        weak_all += weak
        ang = abs(rep[1] - th0)
        n_angle += ang > 5e-3
        print("  %-18s K=%d reported R=%.7f rel %.2e angle %.2e | nearest R=%.5f rel %.2e | weaker pairs inside |c0|: %s"
              % (key, v['K'], rep[0], abs(rep[0] - R0) / R0, ang, near[0], abs(near[0] - R0) / R0,
                 ', '.join('%.5f' % r for r in weak) or '-'))
    print("  fits with a weaker pair inside |c0|: %d of %d%s" % (n_weak, len(fits),
          (' (R from %.3f to %.3f)' % (min(weak_all), max(weak_all))) if weak_all else ''))
    print("  fits whose reported pair breaks the 5e-3 angle line: %d of %d\n" % (n_angle, len(fits)))
