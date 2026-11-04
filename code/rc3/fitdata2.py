import numpy as np, sys, json
from ladder import ladder, contributions
from spc import initial
from anfull import fit as freefit
from darboux import load
d=sys.argv[1]; tags=sys.argv[2].split(','); thr=1e-3
windows=[(30,200),(40,220),(30,180),(50,200),(30,240)]
out={}
for tag in tags:
    r,o=load(tag)
    for (n1,n2) in windows:
        R0,t0=initial(r,n2)
        Ksel,res=ladder(r,n1,n2,R0,t0)
        pairs=res[Ksel][0]
        cf=contributions(r,n1,n2,pairs,R0)
        sig=[p for p,c in zip(pairs,cf) if c>thr]
        dom=sig[0]
        print('%s %d-%d K=%d dominant R=%.10f theta=%.10f | pairs(contrib@n2): %s | rms %s'%(tag,n1,n2,Ksel,dom[0],dom[1],
              ' '.join('(%.5f,%.5f;%.1e)'%(p[0],p[1],c) for p,c in zip(pairs,cf)), ' '.join('%.1e'%res[K][1] for K in res)),flush=True)
        x,rms=freefit(r,n1,n2,2,np.array([dom[0],dom[1],1.5]))
        out[f'{tag}_{n1}_{n2}']=dict(K=Ksel,pairs=pairs,contrib=list(cf),dominant=dom,rms={K:res[K][1] for K in res},free=[x[0],x[1],x[2]-1,rms])
        print('    free single-pair: R=%.8f theta=%.8f beta=%.5f rms=%.1e'%(x[0],x[1],x[2]-1,rms),flush=True)
json.dump(out,open(f'fits_{d}.json','w'),indent=1,default=float)
