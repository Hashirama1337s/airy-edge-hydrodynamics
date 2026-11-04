import sys, json, time, math, numpy as np
from lib import *
# refine.py trackfile name setting out  [ds...]
tf, name, setting, out = sys.argv[1:5]
ds=[int(x) for x in sys.argv[5:]] or [256,512,1024,2048,4096]
S={'A':dict(bits=110,kappa=0.25,hmax=1.0,dLm=0),'B':dict(bits=150,kappa=0.2,hmax=0.8,dLm=15),'C':dict(bits=128,kappa=0.25,hmax=1.0,dLm=0),'D':dict(bits=176,kappa=0.2,hmax=0.8,dLm=15)}[setting]
C=Ctx('mp',S['bits'])
L=[json.loads(l) for l in open(tf)]
for d in ds:
    r=[x for x in L if x['name']==name and abs(x['d']-d)<1e-9][-1]
    q2=complex(*r['q2']); wfr=complex(*r['w'])
    t0=time.time()
    Lm0=C.digits*math.log(10)+8+S['dLm']
    w,s,h=crit(C,wfr/2,q2/4,d,kappa=S['kappa'],hmax=S['hmax'],Lm0=Lm0)
    J,info=F_eval(C,np.array([w],dtype=object),np.array([s],dtype=object),d,kappa=S['kappa'],hmax=S['hmax'],Lm0=Lm0,ret_info=True)
    res=dict(name=name,d=d,setting=setting,bits=S['bits'],q2=[str((4*s).real),str((4*s).imag)],w=[str((2*w).real),str((2*w).imag)],
             hist=[float(x) for x in h],resF=float(abs(complex(J[0][0]))/abs(complex(J[1][0])+1e-300)),Fww=str(complex(2*J[2][0])),info=info,sec=time.time()-t0)
    open(out,'a').write(json.dumps(res)+"\n"); print(res,flush=True)
