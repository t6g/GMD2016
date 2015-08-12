import numpy as np
import pylab as plt

# dc/dt = -(c-e)/(c-e+s)
# (ck+1 - ck)/dt = -(ck+1 - e)/(ck+1 - e + s)
# f = (ck+1 - ck)/dt + (ck+1 - e)/(ck+1 - e + s)
# d = df/dck+1 = 1/dt + s/(ck+1 - e + s)^2
# delta = f/d
# for the first iteration, ck+1 = ck
# delta = (ck+1 - e)/(ck+1 - e + s) / (1/dt + s/(ck+1 - e + s)^2)

c0 = 1e-6
s0 = 1e-6
dt = 1e-3
e0 = 1e-20

xi = np.arange(-9, -4, 0.01)
xx = np.zeros_like(xi)
ti = np.zeros_like(xi)
f1 = np.zeros_like(xi)
f2 = np.zeros_like(xi)
f3 = np.zeros_like(xi)
fb = np.ones_like(xi)
fb = fb * c0

for i in range(len(xi)):
  xx[i] = 10**xi[i]
  ti[i] = 10**(xi[i])
  f1[i] = (xx[i] - e0)/(xx[i] - e0 + s0   ) / (1.0/dt +    s0 / (xx[i] - e0 + s0) / (xx[i] - e0 + s0)) 
  f2[i] = (c0    - e0)/(c0    - e0 + xx[i]) / (1.0/dt + xx[i] / (c0 - e0 + xx[i]) / (c0 - e0 + xx[i])) 
  f3[i] = (c0    - e0)/(c0    - e0 + s0)    / (1.0/ti[i] + s0 / (c0 - e0 + s0) / (c0 - e0 + s0)) 
  f1[i] = f1[i]/xx[i]
  f2[i] = f2[i]/c0
  f3[i] = f3[i]/c0

"""
lx = 0.05
ly = 0.9

plt.subplots_adjust(left=0.2, hspace=0.25)
ax1 = plt.subplot(3, 1, 1)
plt.loglog(ti, f3, 'b-', ti, fb, 'r--')
plt.xlabel('$R_a\Delta$ t')
#plt.ylabel(r'$[\mathrm{NH_4^+}]^k$ or $\delta [\mathrm{NH_4^+}]^k$ [M]')
plt.ylabel('Concentration [M]')
lgd = plt.legend(('$\delta [\mathrm{NH_4^+}]^k$', '$[\mathrm{NH_4^+}]^k$'), loc=4)
lgd.draw_frame(False)
#txt = lgd.get_texts()
#plt.setp(txt, fontsize='small')
plt.text(lx, ly, '(a)', transform=ax1.transAxes)

ax2 = plt.subplot(3, 1, 2)
plt.loglog(xx, f1, 'b-', xx, xx, 'r--')
plt.xlabel('$[\mathrm{NH_4^+}]^k$ [M]')
plt.ylabel(r'$[\mathrm{NH_4^+}]^k$ or $\delta [\mathrm{NH_4^+}]^k$ [M]')
plt.ylabel('Concentration [M]')
plt.yticks([1e-9, 1e-6, 1e-3])
plt.text(lx, ly, '(b)', transform=ax2.transAxes)

ax3 = plt.subplot(3, 1, 3)
plt.loglog(xx, f2, 'b-', xx, fb, 'r--')
plt.xlabel('$k_m$ [M]')
plt.ylabel(r'$[\mathrm{NH_4^+}]^k$ or $\delta [\mathrm{NH_4^+}]^k$ [M]')
plt.ylabel('Concentration [M]')
plt.text(lx, ly, '(c)', transform=ax3.transAxes)
"""

plt.loglog(xx, f3, 'b-', xx, f1, 'r-', xx, f2, 'g-')
plt.grid()
lgd = plt.legend(('$R_a\Delta t$', '$[\mathrm{NH_4^+}]$', '$k_\mathrm{m}$'), loc=4)
lgd.draw_frame(False)
plt.xlabel('$R_a\Delta t$, $[\mathrm{NH_4^+}]$, or $k_m$')
plt.ylabel('$\delta[\mathrm{NH_4^+}]/[\mathrm{NH_4^+}]$')
plt.subplots_adjust(bottom=0.15)


fig = plt.gcf()
fig.set_size_inches(6, 4)
plt.savefig('fig07monodupdate1.pdf')
plt.show()
