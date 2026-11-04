import numpy as np, sys, json
from ladder import ladder, binom_coef
from darboux import recurrence_table
def initial(r, n2):
    t = recurrence_table(r, [n2 - 5])[0]
    return t[1] * (1 - 1.5 / (n2 - 5)), t[2]   # crude 1/n bias removal (g=1.5)
def synth(case, N=520, rng=None):
    n = np.arange(N + 1).astype(float); n[0] = 1e-9
    s = binom_coef(0.5, np.arange(N + 1)); t = binom_coef(1.5, np.arange(N + 1))
    r = np.zeros(N + 1)
    for (R, th, amp) in case:
        C = amp * np.exp(1j * rng.uniform(0, 2 * np.pi)); D = 0.5 * amp * np.exp(1j * rng.uniform(0, 2 * np.pi))
        ph = np.exp(-np.arange(N + 1) * np.log(R) - 1j * np.arange(N + 1) * th)
        r += np.real(ph * (C * s + D * t))
    r += 1e-14 * 1.92 ** (-np.arange(N + 1)) * rng.standard_normal(N + 1)
    return r
if __name__ == '__main__':
    n1, n2 = int(sys.argv[1]), int(sys.argv[2]); R1 = float(sys.argv[3]); th1 = float(sys.argv[4])
    rng = np.random.default_rng(7)
    cases = [
      [(R1, th1, 2e-4), (R1*1.02, th1+0.08, 3e-4)],
      [(R1, th1, 2e-4), (R1*1.05, th1-0.10, 5e-4)],
      [(R1, th1, 2e-4), (R1*1.03, th1+0.12, 2e-4), (R1*1.07, th1-0.06, 6e-4)],
      [(R1, th1, 2e-4), (R1*1.02, th1-0.15, 1e-4), (R1*1.10, th1+0.10, 8e-4)],
      [(R1, th1, 2e-4), (R1*1.025, th1+0.05, 3e-4), (R1*1.05, th1-0.12, 3e-4), (R1*1.09, th1+0.15, 6e-4)],
      [(R1, th1, 1e-4), (R1*1.04, th1-0.05, 4e-4), (R1*1.06, th1+0.18, 4e-4), (R1*1.10, th1-0.2, 1e-3)],
    ]
    errs = []
    for i, case in enumerate(cases):
        r = synth(case, rng=rng)
        R0, t0 = initial(r, n2)
        Ksel, res = ladder(r, n1, n2, R0, t0)
        Rf, tf = res[Ksel][0][0]
        eR = abs(Rf / R1 - 1); et = abs(tf - th1); errs.append((eR, et))
        print('case %d Ktrue=%d Ksel=%d  R=%.9f (rel err %.2e) theta=%.9f (err %.2e)  rms by K: %s' % (
            i, len(case), Ksel, Rf, eR, tf, et, ' '.join('%.1e' % res[K][1] for K in res)), flush=True)
    e = np.array(errs); print('MAX rel R err %.3e  MAX theta err %.3e' % (e[:, 0].max(), e[:, 1].max()))
    json.dump(dict(window=[n1, n2], max_rel_R_err=float(e[:, 0].max()), max_theta_err=float(e[:, 1].max()), errs=errs),
              open(f'spc_{n1}_{n2}.json', 'w'))
