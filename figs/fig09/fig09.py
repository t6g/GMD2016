import numpy as np
import matplotlib.pyplot as plt

r0 = np.loadtxt('lit0-obs-0.tec',skiprows=1)
r1 = np.loadtxt('lit0a-obs-0.tec',skiprows=1)
r2 = np.loadtxt('lit0b-obs-0.tec',skiprows=1)

plt.subplots_adjust(wspace=0.3)
lx = 0.05
ly = 0.9

ax1=plt.subplot(2, 2, 1)
plt.plot(r0[:, 0], r0[:,5], 'b+-.', r1[:, 0], r1[:,5], 'rx:', r2[:, 0], r2[:, 5], 'g-*') 
plt.ylabel('Lit1 (mol m$^{-3}$)')
plt.ylim([0, 0.22])
a = plt.axes([.25, .70, .15, .12])
plt.plot(r0[:, 0], r0[:,5], 'b+-.', r1[:, 0], r1[:,5], 'rx:', r2[:, 0], r2[:, 5], 'g-*') 
plt.xlim([0, 2])
plt.xticks([0, 1, 2])
plt.ylim([0, 0.22])
plt.yticks([0, 0.1, 0.2])
#plt.setp(a, yticks=[])
#a.set_xlabel('c x 10$^{-8}$')
plt.text(lx, ly, '(a)', transform=ax1.transAxes)

ax2=plt.subplot(2, 2, 2)
plt.plot(r0[:, 0], r0[:,3], 'b+-.', r1[:, 0], r1[:,3], 'rx:', r2[:, 0], r2[:, 3], 'g-*') 
plt.ylabel('SOM1 (mol m$^{-3}$)')
plt.ylim([0.0, 0.052])
b = plt.axes([.72, .70, .15, .12])
plt.plot(r0[:, 0], r0[:,3], 'b+-.', r1[:, 0], r1[:,3], 'rx:', r2[:, 0], r2[:, 3], 'g-*') 
plt.xlim([0, 2])
plt.xticks([0, 1, 2])
plt.yticks([0, 0.02, 0.04])
plt.ylim([0.0, 0.052])
plt.text(lx, ly, '(b)', transform=ax2.transAxes)

ax3=plt.subplot(2, 2, 3)
plt.plot(r0[:, 0], r0[:,4], 'b+-', r1[:, 0], r1[:,4], 'rx:', r2[:, 0], r2[:, 4], 'g-*') 
lgd = plt.legend(('$k_m = 10^{-6}$', '$k_m = 10^{-9}$', '$k_m = 10^{-12}$'), numpoints=1, loc=4);
lgd.draw_frame(False);
plt.ylabel('SOM2 (mol m$^{-3}$)')
plt.xlabel('Time (d)')
plt.ylim([0,0.1])
#plt.yticks([1e-15, 1e-10, 1e-5])
plt.text(lx, ly, '(c)', transform=ax3.transAxes)

ax4=plt.subplot(2, 2, 4)
plt.semilogy(r0[:, 0], r0[:,2], 'b+-.', r1[:, 0], r1[:, 2], 'rx:', r2[:, 0], r2[:, 2], 'g-*')
plt.xlabel('Time (d)')
plt.ylabel('NH${_4}^+$ (M)')
plt.ylim([1e-15,1e-4])
plt.yticks([1e-15, 1e-10, 1e-5])
for tick in ax4.yaxis.get_major_ticks():
    tick.label.set_fontsize(10) 
#ax3.yaxis.label.set_size(10)
d = plt.axes([.72, .17, .15, .12])
plt.semilogy(r0[:, 0], r0[:,2], 'b+-.', r1[:, 0], r1[:, 2], 'rx:', r2[:, 0], r2[:, 2], 'g-*')
plt.xlim([0, 2])
plt.xticks([0, 1, 2])
plt.yticks([1e-15, 1e-10, 1e-5])
for tick in d.yaxis.get_major_ticks():
    tick.label.set_fontsize(10) 
plt.text(lx, ly, '(d)', transform=ax4.transAxes)

xticklabels = ax1.get_xticklabels() + ax2.get_xticklabels()
plt.setp(xticklabels, visible=False)

fig = plt.gcf()
fig.set_size_inches(8, 6)
ofname = 'figdecomp.pdf'
plt.savefig(ofname)
plt.show()
