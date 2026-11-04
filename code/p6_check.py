"""BAR-DYN1b P6 (sealed rule in SEALS/DYN1b/AMENDMENT-DYN1b.md, item 2): at d = 32768 the blind value is closer to the
family-A prediction than to family B in BOTH q2 and w. Prints the same lines as SEALS/DYN1b/DYN1b_verdict-DYN1b.txt (last 3).
Run from the top folder of the deposit: python code/p6_check.py"""
import json

blind = json.load(open('data/DYN1b/RESULT.json'))['track']['32768']
A = json.load(open('data/DYN1b/PRED-DYN1b.json'))
B = json.load(open('data/DYN1b/PRED-DYN1b-rivalB.json'))
ok = True
for k in ('q2', 'w'):
    x = complex(float(blind[k][0]), float(blind[k][1]))
    a = complex(*A[k]['32768']['pred'])
    b = complex(*B[k]['32768'])
    print(k, '|x-A|', abs(x - a), '|x-B|', abs(x - b))
    ok = ok and abs(x - a) < abs(x - b)
print('P6', 'HOLDS' if ok else 'FAILED')
