import numpy as np
from scipy.optimize import minimize_scalar as mini
from scipy.interpolate import interp1d as interp
from scipy.optimize import root_scalar as root

import matplotlib.pyplot as plt




class Solow_simple:

    def __init__(self,

                  n=int(1e2),
                 freq=1,
                 δ=1e-1,
                 A=2,
                 mps=.5, alpha=.3,ϕ=.1, s_min=0, s_max = 9):
        self.A=A
        self.mps=mps
        self.alpha=alpha
        self.ϕ=ϕ

        self.δ=δ
        self.β=np.exp(-δ/freq)
        self.freq=freq

        
        self.s_min=s_min
        self.s_max=s_max
        self.n=n
        self.s_grid=np.linspace(s_min,s_max,n)
        self.ds=(self.s_max-self.s_min)/(self.n-1)
        self.eq=root(lambda s: self.sdot(s,self.x(s)),bracket=[self.s_min,self.s_max],method='brentq').root
        self.s_grid=np.append(np.append(np.arange(self.s_min, self.eq(), self.ds),np.arange(self.eq(),self.s_max,self.ds)),self.s_max)

        self.veq=self.W(self.h(self.eq(),self.x(self.eq())),self.x(self.eq()))/(1-self.β)



    def x(self,s):
        return (1-self.mps)*s
    def sdot(self, s,x):
        return self.A *(s-x)**self.alpha-self.ϕ*s

    def W(self,s,x):
        return x**.5/self.freq

so_low=Solow_simple()

def vf(cl,s):
      if abs(s-cl.eq)<cl.ds:
        return cl.veq
      else:
        return  cl.W(s,cl.x(s))+cl.β*vf(cl,s+cl.sdot(s,cl.x(s)))

def state_action_value(cl,s_grid,s, v_array,policy):

    v = interp(s_grid, v_array)
    sav=lambda x: cl.W(s,x)+ cl.β * v(max(cl.s_min,s+cl.sdot(s,x)))

    if callable(policy):
      return sav(policy(s))
    else:
      return sav(policy)

def T(v,cl=None,s_grid=[],policy=None):
  if not list(s_grid):
    s_grid=cl.s_grid
  if policy==None:
    v_new = np.empty_like(v)
    x_new = np.empty_like(v)

    for i, s in enumerate(s_grid):
        # Maximize RHS of Bellman equation at state x
        foo=mini((lambda x: -state_action_value(cl,s_grid,s=s,v_array=v,policy=x/cl.freq)), bounds=(0, min(s,cl.policy_bound)),method='bounded')
        v_new[i]=-foo.fun
        x_new[i]=foo.x
    return v_new,x_new
  else:
    v_new = np.empty_like(v)

    for i, s in enumerate(s_grid):
      v_new[i] = state_action_value(cl,s_grid,s,v,policy)

    return v_new

def vfi_plot(cl=so_low,max_iter=1e2,s_grid=[],initial_guess=[],optimal=0,tol=0,policy=None,policy_iterations=0,ax_pol=1,plot=1):
  if not list(s_grid):
      s_grid=cl.s_grid
  if not list(initial_guess):
      initial_guess=0*s_grid
  if optimal==0 and policy==None:
      policy=cl.x

  fig, (ax1,ax2) = plt.subplots(2,1,sharex=True)

  v=initial_guess
  ax1.plot(s_grid, v, color=plt.cm.jet(0),
          lw=2, alpha=0.6, label='Initial guess')
  if ax_pol!=0:
    ax2.plot(s_grid,[cl.x(s) for s in s_grid], color=plt.cm.jet(0),
          lw=2, alpha=0.6, label='status quo policy')

  i = 0


  while i < max_iter and 1>tol:
      if optimal==0:

        v= T(v,cl,s_grid,policy)
      else:
        tmp=T(v,cl,s_grid)
        v_new = tmp[0]
        j=0
        xinterp=interp(s_grid,tmp[1])
        while j<=policy_iterations:
          v= T(v,cl,s_grid,policy=xinterp)
          ax1.plot(s_grid, v, color=plt.cm.jet(i /  max_iter), lw=2, alpha=0.6)
          j+=1
          if ax_pol!=0:
            ax2.plot(s_grid, tmp[1], color=plt.cm.jet(i /  max_iter), lw=2, alpha=0.6)

      ax1.plot(s_grid, v, color=plt.cm.jet(i /  max_iter), lw=2, alpha=0.6)

      i += 1


  ax1.plot(s_grid, v, color=plt.cm.jet(i / max_iter), lw=2, alpha=0.6,label='VFI approximation')
  if ax_pol!=0:
    if optimal!=0:
      ax2.plot(s_grid, tmp[1], color=plt.cm.jet(i /  max_iter), lw=2, alpha=0.6,label='improved policy')
    ax2.legend()
    ax2.set_ylabel('policy', fontsize=12)

  else:
    ax2.axis('off')
    fig.set_size_inches(9, 9)

  ax1.legend()


  ax1.set_ylabel('value', fontsize=12)
  ax1.set_xlabel('initial capital stock $s_0$', fontsize=12)
  ax1.set_title('Value function iterations')

  if optimal==0:
    cl.vn=v
  else:
    cl.v=v
  if plot==0:
     plt.close()


def plot_price(cl,max_iter=1e2,s_grid=[],initial_guess=[],optimal=0,tol=0,policy=None,policy_iterations=0,ax_pol=0,plot=1):
  vfi_plot(cl,max_iter,s_grid,initial_guess,optimal,tol,plot=0)
  if optimal==0:
    cl.pn=np.diff(cl.vn)/np.diff(s_grid)
    cl.pn=np.append(cl.pn,cl.pn[-1])
    fig, ax = plt.subplots()

    ax.plot(cl.s_grid,cl.pn)
    ax.set


def plot_fishery(cl):

  fig, ax = plt.subplots()

  ax.plot(cl.s_grid,[cl.f(s) for s in cl.s_grid],label='Natural Growth')
  ax.plot(cl.s_grid,[cl.h(s,cl.x(s)) for s in cl.s_grid],label='Harvest');
  ax.plot(cl.eq, cl.f(cl.eq), '-ro',label="equilibrium");
  ax.legend();

