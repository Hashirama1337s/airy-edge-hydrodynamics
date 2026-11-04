"""Airy constants of the large-d law for the shear critical point (paper Section 3.1) and the leading-law misses (Section 4.3).

W(U) = Ai'(U)^2 - U Ai(U)^2 (= integral of Ai^2 from U to infinity, so W' = -Ai^2).
U1, U2, U3 = its first three complex zeros with Im U > 0; T1 = Ai'(U1)/Ai(U1).
Law: qfr^2 + 2 = A d^(-1/3) + O(1/d), wfr - i = B d^(-1/3) + O(1/d), with A = -4 T1 2^(-1/3), B = 2i T1 2^(-1/3).
The leading-law miss |q2_blind + 2 - A d^(-1/3)| uses the blind tracked values in data/DYN1b/RESULT.json.
Usage (from the top folder of the deposit):  python code/airy_constants.py
"""
import json
import mpmath as mp

mp.mp.dps = 30


def W(U):
    return mp.airyai(U, 1) ** 2 - U * mp.airyai(U) ** 2


seeds = [mp.mpc(-2.79, 1.094), mp.mpc(-4.457, 1.027), mp.mpc(-5.846, 0.979)]
Us = [mp.findroot(W, s) for s in seeds]
for k, U in enumerate(Us, 1):
    dW = mp.diff(W, U)
    print("U%d = %s   |W(U)| = %s   |W'(U) + Ai(U)^2| = %s" % (k, mp.nstr(U, 12), mp.nstr(abs(W(U)), 2),
                                                          mp.nstr(abs(dW + mp.airyai(U) ** 2), 2)))
U1 = Us[0]
T1 = mp.airyai(U1, 1) / mp.airyai(U1)
c = mp.mpf(2) ** (-mp.mpf(1) / 3)
A = -4 * T1 * c
B = 2j * T1 * c
print("T1 = %s" % mp.nstr(T1, 12))
print("|U1 - T1^2| = %s   (U = T^2 at a zero: no d^(-2/3) term)" % mp.nstr(abs(U1 - T1 ** 2), 2))
print("A  = %s" % mp.nstr(A, 12))
print("B  = %s" % mp.nstr(B, 12))
print("|A - 2iB| = %s" % mp.nstr(abs(A - 2j * B), 2))
R = json.load(open("data/DYN1b/RESULT.json"))["track"]
for d in ("8192", "16384", "32768"):
    q2 = mp.mpc(*map(mp.mpf, R[d]["q2"]))
    miss = abs(q2 + 2 - A * mp.mpf(d) ** (-mp.mpf(1) / 3))
    print("d = %5s  leading-law miss |q2 + 2 - A d^(-1/3)| = %s" % (d, mp.nstr(miss, 5)))
