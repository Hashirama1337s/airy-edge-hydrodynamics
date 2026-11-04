"""The d = 4 control and Table 4 of the paper: Newton refinement of the shear critical point c0 (double root of the
spectral function of code/qnmx.py, via code/lib.py) at 110 bits, the setting "A" of code/refine.py.

Seeds: at d = 4 the published 8-digit values of the d = 4 critical point (as in the blind seat's control); at the other d
the double-precision points of the deposited continuation tracks (data/c0down/down_h16.jsonl for d = 3, data/DYN1/track_c0.jsonl
for d = 512, 1024, 2048, data/DYN1b/track_c0b.jsonl for d >= 8192). Newton then converges to about 30 digits.
The result is compared with the deposited high-precision values (150 bits, setting "B"): data/c0down/refine_B.jsonl (d = 3),
data/DYN1/RESULT.json (d = 4 and 512-2048), data/DYN1b/RESULT.json (d >= 8192).
Usage (from the top folder of the deposit):  python code/table4.py      (about 1-2 minutes)
"""
import json, math, sys, time
sys.path.insert(0, "code")
import mpmath as mp
from lib import Ctx, crit
mp.mp.dps = 45

C = Ctx('mp', 110)
Lm0 = C.digits * math.log(10) + 8


def refine(wfr, q2, d):
    w, s, h = crit(C, wfr / 2, q2 / 4, d, kappa=0.25, hmax=1.0, Lm0=Lm0)
    return 4 * s, 2 * w, h


def track_point(fname, d, name=None):
    best = None
    for line in open(fname):
        r = json.loads(line)
        if abs(r['d'] - d) < 1e-9 and (name is None or r.get('name') == name):
            best = r
    return complex(*best['w']), complex(*best['q2'])


def cplx(p):
    return mp.mpc(p[0], p[1])


def tomp(z):
    return mp.mpc(str(z.real), str(z.imag))


R1 = json.load(open("data/DYN1/RESULT.json"))
R1b = json.load(open("data/DYN1b/RESULT.json"))["track"]
ref3 = [json.loads(l) for l in open("data/c0down/refine_B.jsonl")]
ref3 = [r for r in ref3 if abs(r['d'] - 3.0) < 1e-12][-1]

# d = 4 control
t0 = time.time()
q2, w, h = refine(complex(1.4436414, -1.0692250), complex(1.8906469, 1.1711505), 4)
pub_q2, pub_w = complex(1.8906469, 1.1711505), complex(1.4436414, -1.0692250)
print("d = 4 control: q2 = %s, wfr = %s" % (q2, w))
print("  published (8 digits): q2 = 1.8906469 + 1.1711505i, wfr = 1.4436414 - 1.0692250i; max |diff| = %.1e (rounding < 5e-8)"
      % max(abs(complex(q2) - pub_q2), abs(complex(w) - pub_w)))
print("  |q2| = %.6f   (%.0f s)" % (abs(complex(q2)), time.time() - t0))
q2_4 = q2

rows = [(3, "data/c0down/down_h16.jsonl", None, cplx(ref3['q2'])),
        (4, None, None, cplx(R1['d4']['q2'])),
        (512, "data/DYN1/track_c0.jsonl", "c0", cplx(R1['track']['512']['q2'])),
        (1024, "data/DYN1/track_c0.jsonl", "c0", cplx(R1['track']['1024']['q2'])),
        (2048, "data/DYN1/track_c0.jsonl", "c0", cplx(R1['track']['2048']['q2'])),
        (8192, "data/DYN1b/track_c0b.jsonl", "c0", cplx(R1b['8192']['q2'])),
        (16384, "data/DYN1b/track_c0b.jsonl", "c0", cplx(R1b['16384']['q2'])),
        (32768, "data/DYN1b/track_c0b.jsonl", "c0", cplx(R1b['32768']['q2']))]
print("\nTable 4 (q2 = qfr^2 of c0; diff = |110-bit value - deposited 150-bit value|):")
for d, f, name, ref in rows:
    t0 = time.time()
    if f is None:
        q2 = q2_4  # the d = 4 control above
    else:
        sw, sq = track_point(f, d, name)
        q2, w, h = refine(sw, sq, d)
    s = "%s %s %si" % (format(q2.real, '.21g'), '+' if q2.imag >= 0 else '-', format(abs(q2.imag), '.21g'))
    diff = mp.nstr(abs(tomp(q2) - ref), 2)
    print("d = %5d  c0 = %s   |c0| = %.5f   diff = %s   (%.0f s)" % (d, s, abs(complex(q2)), diff, time.time() - t0))
