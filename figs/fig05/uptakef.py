import math as math
import numpy as np
import matplotlib.pyplot as plt

# compare uptake scheme using CLM and PF
# given 
#   demand rate [mol/L s]
#   concentration NH4+ [M]
#   concentration NO3- [M] 
#   time step size s
# what is f = actual uptake/demand (e.g., fpg in CLM)?  
 
def clm(demand, nh4, no3, dt):
  # CLM N demand distribution between NH4+ and NO3-
  uptake = 0.0
  if demand < nh4 / dt:
    uptake = demand
  else:
    uptake = nh4/dt

  demand_remain = demand - uptake
  if demand_remain > 0.0:
    if demand_remain < no3/dt:
      uptake = demand
    else:
      uptake = uptake + no3/dt
  return (uptake/demand)

def pf(demand, nh4, no3, dt, km):
  # rate_nh4 = demand * nh4 / (nh4 + km)
  # rate_no3 = (demand - rate_nh4 )* no3 / (no3 + km)
  #          = demand * km / (nh4 + km) * no3 / (no3 + km)

  # dc/dt = R c/(c+k_m) = rate_nh4
  # (c_{k+1} - c_k)/dt = R c_{k+1} / (c_{k+1} + k_m)      backward difference
  # c_{k+1}^2 - (c_k - k_m - R dt) c_{k+1} - k_m c_k = 0  
  # b = c_k - k_m - R dt
  # c_{k+1} = (-b + \sqrt(b^2 + 4 k_m c_k))/2

  b_nh4 = nh4 - km - demand * dt
  nh4_1 = 0.5 * (b_nh4 + math.sqrt(b_nh4 * b_nh4 + 4.0 * km * nh4))

  demand_no3 = demand * km / (nh4_1 + km)

  b_no3 = no3 - km - demand * km / (nh4_1 + km) * dt
  no3_1 = 0.5 * (b_no3 + math.sqrt(b_no3 * b_no3 + 4.0 * km * no3))
  
  uptake = (nh4 + no3 - nh4_1 - no3_1)/dt
  return (uptake/demand)

dt  = 1800.0
km1 = 1.0e-6
km2 = 1.0e-7
km3 = 1.0e-8
demand = 1.0e-9
x = y = np.arange(-8.0, -4.0, 0.01)
xx, yy = np.meshgrid(x, y)
res_clm = np.zeros_like(xx)
res_pf1 = np.zeros_like(xx)
res_pf2 = np.zeros_like(xx)
res_pf3 = np.zeros_like(xx)

for i in range(len(x)):
  for j in range(len(y)):
    nh4 = 10**x[i]
    no3 = 10**y[j]  
    res_clm[i,j] = clm(demand, nh4, no3, dt)
    res_pf1[i,j] = pf(demand, nh4, no3, dt, km1)
    res_pf2[i,j] = pf(demand, nh4, no3, dt, km2)
    res_pf3[i,j] = pf(demand, nh4, no3, dt, km3)

lx = 0.05
ly = 0.90
ax1 = plt.subplot(2, 2, 1)
ct1 = plt.contourf(xx, yy, res_clm, 50)
plt.axis('equal')
plt.xlim([-8, -4])
plt.ylim([-8, -4])
plt.yticks([-8, -7, -6, -5, -4], ['$10^{-8}$', '$10^{-7}$', '$10^{-6}$', '$10^{-5}$', '$10^{-4}$'])
plt.ylabel('NO${_3}^-$ [M]')
#plt.text(lx, ly, '(a)', transform=ax1.transAxes)
plt.title('CLM')

ax2 = plt.subplot(2, 2, 2)
ct2 = plt.contourf(xx, yy, res_pf1, 50)
plt.axis('equal')
plt.xlim([-8, -4])
plt.ylim([-8, -4])
plt.title('$k_\mathrm{m}$ = 10$^{-6}$')
#plt.text(lx, ly, '(b)', transform=ax2.transAxes)

ax3 = plt.subplot(2, 2, 3)
ct3 = plt.contourf(xx, yy, res_pf3, 50)
plt.axis('equal')
plt.xlim([-8, -4])
plt.ylim([-8, -4])
plt.xticks([-8, -7, -6, -5, -4], ['$10^{-8}$', '$10^{-7}$', '$10^{-6}$', '$10^{-5}$', '$10^{-4}$'])
plt.yticks([-8, -7, -6, -5, -4], ['$10^{-8}$', '$10^{-7}$', '$10^{-6}$', '$10^{-5}$', '$10^{-4}$'])
plt.xlabel('NH${_4}^+$ [M]')
plt.ylabel('NO${_3}^-$ [M]')
plt.title('$k_\mathrm{m}$ = 10$^{-10}$')
#plt.text(lx, ly, '(d)', transform=ax3.transAxes)

ax4 = plt.subplot(2, 2, 4)
ct4 = plt.contourf(xx, yy, res_pf2, 50)
plt.axis('equal')
plt.xlim([-8, -4])
plt.ylim([-8, -4])
plt.xticks([-8, -7, -6, -5, -4], ['$10^{-8}$', '$10^{-7}$', '$10^{-6}$', '$10^{-5}$', '$10^{-4}$'])
plt.xlabel('NH${_4}^+$ [M]')
plt.title('$k_\mathrm{m}$ = 10$^{-8}$')
#plt.text(lx, ly, '(c)', transform=ax4.transAxes)

ticklabels = ax1.get_xticklabels() + ax2.get_xticklabels() + ax2.get_yticklabels() + ax4.get_yticklabels() 
plt.setp(ticklabels, visible=False)
fig = plt.gcf()

fig.subplots_adjust(right=0.8)
cbar_ax = fig.add_axes([0.85, 0.14, 0.05, 0.7])
fig.colorbar(ct3, cax=cbar_ax, ticks=[0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0])

fig.set_size_inches(8, 6.75)
plt.savefig('uptakef.pdf')
plt.show()
