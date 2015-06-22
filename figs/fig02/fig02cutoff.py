import numpy as np
import matplotlib.pyplot as plt


x = np.arange(-11, -7.0, 0.001)
t = np.zeros_like(x)
f = np.zeros_like(x)
j = np.zeros_like(x)
l = 1e-10
u = 1e-8
d = u - l

for i in range(len(x)):
  t[i] = 10**x[i]
  if t[i] <= l:
    f[i] = 0.0
    j[i] = 0.0
  elif t[i] >= u:
    f[i] = 1.0
    j[i] = 0.0
  else:
    v = t[i] - l
    f[i] = 1.0 - (1.0 - v * v / d / d)**2
    j[i] = 4.0 * v / d / d * (1.0 - v * v / d / d)

lx = 0.05
ly = 0.9

plt.subplots_adjust( hspace=0.1, wspace = 0.1 )
     
ax1 = plt.subplot(2, 2, 1)
ax1.plot(t*1e8, f, 'b-')
plt.xlim([0, 2])
plt.ylim([0, 1.2])
ax1.set_ylabel('f(c)', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')
plt.text(lx, ly, '(a)', transform=ax1.transAxes)

ax1s = ax1.twinx()
ax1s.plot(t*1e8, j*1e-8, 'r')
plt.xlim([0, 2])
plt.ylim([0, 1.8])
plt.yticks([0, .3, .6, .9, 1.2, 1.5, 1.8])

ax2 = plt.subplot(2, 2, 2)
plt.semilogx(t, f, 'b-')
plt.xlim([1e-11, 1e-7])
plt.ylim([0, 1.2])
plt.text(lx, ly, '(b)', transform=ax2.transAxes)

ax2s = ax2.twinx()
ax2s.semilogx(t, j*1e-8, 'r')
plt.ylim([0, 1.8])
plt.yticks([0, .3, .6, .9, 1.2, 1.5, 1.8])
ax2s.set_ylabel('df(c)/dc x 10$^8$', color='r')
for tl in ax2s.get_yticklabels():
    tl.set_color('r')

x1  = t[1002:4000] 
y1  = f[1002:4000] 
x2  = t[1002:3001]
dy = j[1002:3001]

ax3 = plt.subplot(2, 2, 3)
plt.semilogy(x1*1e8, y1, 'b-')
plt.xlim([0, 2])
plt.ylim([1e-10, 1e2])
plt.yticks([1e-9, 1e-6, 1e-3, 1e0])
ax3.set_xlabel('c x 10$^{-8}$')
ax3.set_ylabel('f(c)', color='b')
for tl in ax3.get_yticklabels():
    tl.set_color('b')
plt.text(lx, ly, '(c)', transform=ax3.transAxes)

ax3s = ax3.twinx()
ax3s.semilogy(x2*1e8, dy, 'r')
plt.xlim([0, 2])
plt.ylim([1e-3, 1e10])
plt.yticks([ 1e-2, 1e1, 1e4, 1e7])

ax4 = plt.subplot(2, 2, 4)
plt.loglog(x1, y1, 'b-')
plt.xlim([1e-11, 1e-7])
plt.ylim([1e-10, 1e2])
plt.yticks([1e-9, 1e-6, 1e-3, 1e0])
ax4.set_xlabel('c')
plt.text(lx, ly, '(d)', transform=ax4.transAxes)

ax4s = ax4.twinx()
ax4s.loglog(x2, dy, 'r')
plt.xlim([1e-11, 1e-7])
plt.ylim([1e-3, 1e10])
plt.xticks([ 1e-10, 1e-9, 1e-8, 1e-7])
plt.yticks([ 1e-2, 1e1, 1e4, 1e7])
ax4s.set_ylabel('df(c)/dc', color='r')
for tl in ax4s.get_yticklabels():
    tl.set_color('r')

xticklabels = ax1.get_xticklabels() + ax1s.get_xticklabels() + ax2.get_xticklabels() + ax2s.get_xticklabels() 
plt.setp(xticklabels, visible=False)

yticklabels = ax1s.get_yticklabels() + ax2.get_yticklabels() + ax3s.get_yticklabels() + ax4.get_yticklabels() 
plt.setp(yticklabels, visible=False)

fig = plt.gcf()
fig.set_size_inches(8, 6)
plt.savefig('fig02cutoff.pdf')
plt.show()
