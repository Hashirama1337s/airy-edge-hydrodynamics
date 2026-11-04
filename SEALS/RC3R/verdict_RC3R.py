import json
R = json.load(open("blind/RESULT-R.json")); f = lambda k: float(R[k]); b = lambda k: str(R[k]).lower() == "true"
cin = f("Cin_maxrel") < 1e-6
cout = f("Cout_maxrel") > 1e-3 or not b("Cout_closes")
print("C_in", "PASS" if cin else "FAIL", R["Cin_maxrel"]); print("C_out", "PASS" if cout else "FAIL", R["Cout_maxrel"], R["Cout_closes"])
p = f("P1_maxrel")
v = "VOID" if not (cin and cout) else ("HOLDS" if p < 1e-6 and b("P1_closes") else ("FAILED" if p > 1e-4 or not b("P1_closes") else "INCONCLUSIVE"))
print("P1", v, R["P1_maxrel"], R["P1_closes"])
