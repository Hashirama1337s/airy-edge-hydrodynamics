import json, numpy as np, sys
def ld(f):
    o=json.load(open(f)); return o, np.array(o['c_re'])+1j*np.array(o['c_im'])
res={}
for key,new,ref in [('P1','cauchyfull_d8192_r196.json','cauchy_d8192_r192.json'),
                    ('Cin','cauchyfull_d2048_r195.json','cauchy_d2048_r192.json'),
                    ('Cout','cauchyfull_d2048_r198.json','cauchy_d2048_r192.json')]:
    try: on,cn=ld(new)
    except FileNotFoundError: print(key,'missing'); continue
    _,cr=ld(ref)
    n=np.arange(1,151)
    rel=np.abs(cn[n]-cr[n])/np.abs(cr[n])
    closes = on['closure_abs']<1e-8 and abs(on['w_minus_rho'][0])<1e-8 and on['nonconv']==0
    i=np.argmax(rel)
    print('%s: maxrel(n=1..150)=%.3e at n=%d | rel at n=10,50,100,150: %s | |c0 new|=%.1e | closure %.2e Re w(-rho) %.2e sym %.2e nonconv %d -> closes=%s'%(
        key,rel.max(),n[i],' '.join('%.1e'%rel[k-1] for k in [10,50,100,150]),abs(cn[0]),on['closure_abs'],on['w_minus_rho'][0],on['sym_violation'],on['nonconv'],closes))
    res[key]=dict(maxrel=float(rel.max()),argmax=int(n[i]),closes=bool(closes),closure=on['closure_abs'],re_wm=on['w_minus_rho'][0],sym=on['sym_violation'],
                  rel_samples={int(k):float(rel[k-1]) for k in [10,50,100,150]})
json.dump(res,open('compareR.json','w'),indent=1)
