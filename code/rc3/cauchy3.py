import sys, json, time, numpy as np
import qnm; qnm.wronskian = qnm.wronskian_b
from qnm import find_mode
d=int(sys.argv[1]); rho=float(sys.argv[2]); M=int(sys.argv[3]); tag=sys.argv[4]
kw={}
if len(sys.argv)>5: kw['rtol']=float(sys.argv[5])
if len(sys.argv)>6: kw['ym']=float(sys.argv[6])
t0=time.time()
hist=[]
def pred(hist):
    if len(hist)>=3:
        (a,fa),(b,fb),(c,fc)=hist[-3:]
        # quadratic Lagrange in q2
        return lambda x: fa*(x-b)*(x-c)/((a-b)*(a-c))+fb*(x-a)*(x-c)/((b-a)*(b-c))+fc*(x-a)*(x-b)/((c-a)*(c-b))
    return lambda x: -0.5j*x
# ramp along the real axis
for r in np.linspace(0.02, rho, max(6,int(rho/0.05)), endpoint=False):
    q=complex(r); w,it=find_mode(d,q,pred(hist)(q),**kw); hist.append((q,w))
ph=np.pi*2*np.arange(M//2+1)/M
ws=[]
for k,p in enumerate(ph):
    q=rho*np.exp(1j*p); w,it=find_mode(d,q,pred(hist)(q),**kw)
    if it<0: print('nonconv',k,flush=True)
    hist.append((q,w)); ws.append(w)
ws=np.array(ws)
full=np.concatenate([ws, -np.conj(ws[1:-1][::-1])])
n=np.arange(M)
c=np.fft.fft(full)/M/rho**n
out=dict(d=d,rho=rho,M=M,kw=kw,time=time.time()-t0,
         reW_at_minus_rho=float(ws[-1].real), imW_at_rho=float(ws[0].real),
         w_re=[float(x.real) for x in ws], w_im=[float(x.imag) for x in ws],
         c_re=[float(x.real) for x in c], c_im=[float(x.imag) for x in c])
json.dump(out,open(f'cauchy_{tag}.json','w'))
print('done',d,rho,M,'time',round(time.time()-t0,1),'Re w(-rho)=',ws[-1].real,'Re w(rho)=',ws[0].real)
print('c1..c6', c[1:7])
print('max|Re c_n| n<40', np.max(np.abs(c[1:40].real)))
