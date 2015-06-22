import numpy as np
import math as math
import matplotlib.pyplot as plt

def monod1step(ck, s, dt):
# dc/dt = -c/(c + s)
# ck+1^2 + (s + dt - ck) ck+1 - s ck = 0
# ck+1 = (ck - s - dt) + sqrti((ck - s - dt)^2 + 4 cks)
  tmp = ck - s - dt
  res = (tmp + math.sqrt(tmp * tmp + 4.0 * ck * s))/2.0
  return res

r0 = np.loadtxt('plantn0-obs-0.tec',skiprows=1)
r1 = np.loadtxt('plantn0a-obs-0.tec',skiprows=1)
r2 = np.loadtxt('plantn0b-obs-0.tec',skiprows=1)

n0 = np.zeros_like(r0[:, 0])
n1 = np.zeros_like(r1[:, 0])
n2 = np.zeros_like(r2[:, 0])

eps = 1e-20
k = 1e-7*3600.0/250.0

n0[0] = r0[0, 1]
n1[0] = r1[0, 1]
n2[0] = r2[0, 1]

for i in range(len(n0)-1):
    n0[i+1] = monod1step(r0[i, 1] - eps, 1e-6, k*(r0[i+1, 0] - r0[i, 0])) + eps   

for i in range(len(n1)-1):
    n1[i+1] = monod1step(r1[i, 1] - eps, 1e-9, k*(r1[i+1, 0] - r1[i, 0])) + eps   

for i in range(len(n2)-1):
    n2[i+1] = monod1step(r2[i, 1] - eps, 1e-9, k*(r2[i+1, 0] - r2[i, 0])) + eps   

plt.subplots_adjust(hspace=0.001)

"""
lx = 0.85
ly = 0.9
scale = 1e6
ax1=plt.subplot(2, 1, 1)
plt.plot(r1[:, 0], r1[:,1]*scale, 'r+', r2[:, 0], r2[:, 1]*scale, 'gx', r2[:, 0], n2*scale, 'c*')
plt.ylabel('Concentration ($\mathbf{\mu}$M)')
lgd = plt.legend(('$k_m = 10^{-9}$', '$k_m = 10^{-12}$', '$k_m = 10^{-12}$ (semi-analytical)'), numpoints=1, loc=1);
lgd.draw_frame(False);
#txt = lgd.get_texts();
#plt.setp(txt, fontsize='small');
plt.yticks([0, 1, 2, 3, 4])
plt.xlim([0,10])
plt.ylim([-0.2, 4.2])
plt.setp(ax1.get_xticklabels(), visible=False)
plt.text(lx, ly, '(a)', transform=ax1.transAxes)
"""
scale = 1.0
#ax3=plt.subplot(2, 1, 2)
plt.semilogy(r1[:, 0], r1[:,1]*scale, 'r+', r2[:, 0], r2[:, 1]*scale, 'gx', r2[:, 0], n2, 'c*')
plt.xlabel('Time (h)')
plt.ylabel('Concentration (M)')
plt.ylim([1e-21,1e-4])
plt.yticks([1e-20, 1e-15, 1e-10, 1e-5])
#for tick in ax3.yaxis.get_major_ticks():
#    tick.label.set_fontsize(10) 
#ax3.yaxis.label.set_size(10)
plt.xlim([0,10])
lgd = plt.legend(('$k_m = 10^{-9}$', '$k_m = 10^{-12}$', '$k_m = 10^{-12}$ (SA)'), numpoints=1, loc=1);
lgd.draw_frame(False);
#plt.text(lx, ly, '(b)', transform=ax3.transAxes)

fig = plt.gcf()
fig.set_size_inches(6, 4)
ofname = 'fig08plantntake1.pdf'
plt.savefig(ofname)
plt.show()
