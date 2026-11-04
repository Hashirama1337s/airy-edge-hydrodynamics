import sys, json, time, math, numpy as np
from lib import *
# usage: track.py name w0fr q2_0 dstart dend steps_per_octave out
name=sys.argv[1]; wfr=complex(sys.argv[2]); q2=complex(sys.argv[3])
d0=float(sys.argv[4]); d1=float(sys.argv[5]); spo=int(sys.argv[6]); out=sys.argv[7]
bits=int(sys.argv[8]) if len(sys.argv)>8 else 0
C=Ctx('mp',bits) if bits else CNP
w,s=wfr/2,q2/4
w,s,h=crit(C,w,s,d0); w=complex(w); s=complex(s)
f=open(out,'a')
rec=dict(name=name,d=d0,q2=[(4*s).real,(4*s).imag],w=[(2*w).real,(2*w).imag],it=len(h),pred=0.0)
f.write(json.dumps(rec)+"\n"); f.flush(); print(rec,flush=True)
hist=[(math.log(d0),w,s)]
ld=math.log(d0); ld1=math.log(d1); dl=math.log(2)/spo
targets=[]
while ld < ld1-1e-12:
    nxt=min([math.log(2.0**k) for k in range(1,14) if math.log(2.0**k)>ld+1e-9]+[ld1])
    step=min(dl, nxt-ld)
    # snap to powers of 2
    ok=False
    while not ok:
        ln=ld+step
        if abs(ln-nxt)<1e-9: ln=nxt
        if len(hist)>=2:
            (la,wa,sa),(lb,wb,sb)=hist[-2],hist[-1]
            r=(ln-lb)/(lb-la)
            wp=wb+r*(wb-wa); sp=sb+r*(sb-sa)
        else:
            wp,sp=hist[-1][1],hist[-1][2]
        dn=math.exp(ln)
        w2,s2,h=crit(C,wp,sp,dn,tol=(1e-9 if bits else None)); w2=complex(w2); s2=complex(s2)
        pred=float(max(abs(w2-wp),abs(s2-sp)))
        if len(h)<=8 and h[-1]<1e-6 and pred<0.02:
            ok=True
        else:
            step/=2
            print("halve",dn,len(h),h[-1],pred,flush=True)
            if step<1e-4: raise SystemExit("stuck")
    ld=ln; hist.append((ld,w2,s2))
    dd=round(dn) if abs(dn-round(dn))<1e-6 else dn
    rec=dict(name=name,d=dd,q2=[(4*s2).real,(4*s2).imag],w=[(2*w2).real,(2*w2).imag],it=len(h),pred=pred)
    f.write(json.dumps(rec)+"\n"); f.flush(); print(rec,flush=True)
