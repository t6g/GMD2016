import numpy as np
import sys as sys
from scipy.io import netcdf
import matplotlib.pyplot as plt

def openncyear(nm,ny0,ny1):
  tt       = []
  litc     = []
  somc     = []
  vegc     = []
  tlai     = []
  nh4a     = []
  no3a     = []

  ny = ny1 -ny0

  for i in range(ny):
	fname = nm + '%04d'%(ny0+i+1) + '-' + '01-01-00000.nc'
	f = netcdf.netcdf_file(fname, 'r')
	tt.append(f.variables['time'][0])
        litc.append(f.variables['TOTLITN'][:, 0].copy())
        somc.append(f.variables['TOTSOMN'][:, 0].copy())
        vegc.append(f.variables['TOTVEGN'][:, 0].copy())
        tlai.append(f.variables['TLAI'][:, 0].copy())
        nh4a.append(f.variables['SMIN_NH4'][:, 0].copy())
        no3a.append(f.variables['SMIN_NO3'][:, 0].copy())
	f.close()

  data = {}
  data['time'] = tt
  data['litc'] = np.asarray(litc).reshape(ny*365, 1)
  data['somc'] = np.asarray(somc).reshape(ny*365, 1)
  data['vegc'] = np.asarray(vegc).reshape(ny*365, 1)
  data['tlai'] = np.asarray(tlai).reshape(ny*365, 1)
  data['nh4a'] = np.asarray(nh4a).reshape(ny*365, 1)
  data['no3a'] = np.asarray(no3a).reshape(ny*365, 1)
  return data

ny0 = 0
ny1 = 500

#if(len(sys.argv) > 0):
#  ny1 = int(sys.argv[1])

data1 = openncyear('../run-clm/US-Brw_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data2 = openncyear('../run3l/US-Brw_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data3 = openncyear('../run6l/US-Brw_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data4 = openncyear('../run9l/US-Brw_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)

t = ny0 + np.arange((ny1-ny0)*365)/365.0

plt.subplots_adjust(hspace=0.001)
lx = 0.01
ly = 0.88

ax1=plt.subplot(6, 1, 1)
plt.plot(t, data1['tlai'], 'b-', t, data2['tlai'], 'r-', t, data3['tlai'], 'g-', t, data4['tlai'], 'm-')
plt.xlim([0, ny1])
plt.ylim([0, 3.5])
plt.yticks([0, 1, 2, 3])
plt.ylabel('LAI')
plt.text(lx, ly, '(a)', transform=ax1.transAxes)

ax2=plt.subplot(6, 1, 2)
plt.plot(t, data1['vegc'], 'b-', t, data2['vegc'], 'r-', t, data3['vegc'], 'g-', t, data4['vegc'], 'm-')
plt.xlim([0, ny1])
plt.ylim([0, 25])
plt.yticks([0, 10, 20])
plt.ylabel('VEGN (gN m$^{-2}$)')
plt.text(lx, ly, '(b)', transform=ax2.transAxes)

ax3=plt.subplot(6, 1, 3)
plt.plot(t, data1['litc'], 'b-', t, data2['litc'], 'r-', t, data3['litc'], 'g-', t, data4['litc'], 'm-')
plt.xlim([0, ny1])
plt.ylim([0, 8])
plt.yticks([0, 2, 4, 6])
plt.ylabel('LITN (gN m$^{-2}$)')
plt.text(lx, ly, '(c)', transform=ax3.transAxes)

ax4=plt.subplot(6, 1, 4)
plt.plot(t, data1['somc'], 'b-', t, data2['somc'], 'r-', t, data3['somc'], 'g-', t, data4['somc'], 'm-')
plt.xlim([0, ny1])
plt.ylim([0, 60])
plt.yticks([0, 20, 40])
plt.ylabel('SOMN (gN m$^{-2}$)')
plt.text(lx, ly, '(d)', transform=ax4.transAxes)
lgd = plt.legend(('CLM4.5', 'CLM-PF ($k_\mathrm{m} = 10^{-3}$)', 'CLM-PF ($k_\mathrm{m} = 10^{-6}$)', 'CLM-PF ($k_\mathrm{m} = 10^{-9}$)'),loc=4)
lgd.draw_frame(False)
txt = lgd.get_texts();
plt.setp(txt, fontsize='small');

ax5=plt.subplot(6, 1, 5)
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'g-', t, data4['nh4a'], 'm-')
plt.xlim([0, ny1])
plt.ylim([1e-6, 30])
plt.yticks([1e-6, 1e-3, 1])
plt.ylabel('NH${_4}^+$ (gN m$^{-2}$)')
plt.text(lx, ly, '(e)', transform=ax5.transAxes)

ax6=plt.subplot(6, 1, 6)
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'g-', t, data4['no3a'], 'm-')
plt.xlim([0, ny1])
plt.ylim([1e-6, 30])
plt.yticks([1e-6, 1e-3, 1])
plt.ylabel('NO${_3}^-$ (gN m$^{-2}$)')
plt.xlabel('Elapsed time (y)')
plt.text(lx, ly, '(f)', transform=ax6.transAxes)

xticklabels = ax1.get_xticklabels() + ax2.get_xticklabels() + ax3.get_xticklabels() + ax4.get_xticklabels() + ax5.get_xticklabels()
plt.setp(xticklabels, visible=False)

ax1a = plt.axes([0.18, 0.80, 0.20, 0.09]) 
plt.plot(t, data1['tlai'], 'b-', t, data2['tlai'], 'r-', t, data3['tlai'], 'g-', t, data4['tlai'], 'm-')
plt.xlim([0, 10])
plt.xticks([0, 2, 4, 6, 8])
plt.ylim([0, 0.04])
plt.yticks([0, .02])

ax2a = plt.axes([0.18, 0.67, 0.20, 0.09]) 
plt.plot(t, data1['vegc'], 'b-', t, data2['vegc'], 'r-', t, data3['vegc'], 'g-', t, data4['vegc'], 'm-')
plt.xlim([0, 10])
plt.xticks([0, 2, 4, 6, 8])
plt.ylim([0, 0.25])
plt.yticks([0, .1, .2])

ax3a = plt.axes([0.18, 0.53, 0.20, 0.09]) 
plt.plot(t, data1['litc'], 'b-', t, data2['litc'], 'r-', t, data3['litc'], 'g-', t, data4['litc'], 'm-')
plt.xlim([0, 10])
plt.xticks([0, 2, 4])
plt.ylim([0, 0.1])
plt.yticks([0, .05])
plt.setp(ax3a.get_xticklabels(), visible=False)

ax4a = plt.axes([0.18, 0.39, 0.20, 0.09]) 
plt.plot(t, data1['somc'], 'b-', t, data2['somc'], 'r-', t, data3['somc'], 'g-', t, data4['somc'], 'm-')
plt.xlim([0, 10])
plt.xticks([0, 2, 4])
plt.ylim([0, 0.5])
plt.yticks([0, .2, .4])
plt.setp(ax4a.get_xticklabels(), visible=False)

ax5a = plt.axes([0.18, 0.24, 0.20, 0.09]) 
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'g-', t, data4['nh4a'], 'm-')
plt.xlim([0, 10])
plt.ylim([1e-9, 10])
plt.yticks([1e-9, 1e-6, 1e-3, 1])
plt.setp(ax5a.get_xticklabels(), visible=False)

ax6a = plt.axes([0.18, 0.11, 0.20, 0.09]) 
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'g-', t, data4['no3a'], 'm-')
plt.xlim([0, 10])
plt.ylim([1e-10, 10])
plt.yticks([1e-9, 1e-6, 1e-3, 1])
plt.setp(ax6a.get_xticklabels(), visible=False)

xminb = ny1 - 10
xmaxb = ny1
ax1b = plt.axes([0.68, 0.78, 0.20, 0.09]) 
plt.plot(t, data1['tlai'], 'b-', t, data2['tlai'], 'r-', t, data3['tlai'], 'g-', t, data4['tlai'], 'm-')
plt.xlim([xminb, xmaxb])
plt.ylim([0, 3.5])
plt.yticks([0, 1, 2, 3])
plt.setp(ax1b.get_xticklabels(), visible=False)

ax2b = plt.axes([0.68, 0.65, 0.20, 0.09]) 
plt.plot(t, data1['vegc'], 'b-', t, data2['vegc'], 'r-', t, data3['vegc'], 'g-', t, data4['vegc'], 'm-')
plt.xlim([xminb, xmaxb])
plt.yticks([0, 10, 20])
plt.ylim([0, 25])

ax3b = plt.axes([0.68, 0.51, 0.20, 0.09]) 
plt.plot(t, data1['litc'], 'b-', t, data2['litc'], 'r-', t, data3['litc'], 'g-', t, data4['litc'], 'm-')
plt.xlim([xminb, xmaxb])
plt.yticks([0, 2, 4, 6])
plt.ylim([0, 8])
plt.setp(ax3b.get_xticklabels(), visible=False)

ax5b = plt.axes([0.68, 0.24, 0.20, 0.09]) 
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'g-', t, data4['nh4a'], 'm-')
plt.xlim([xminb, xmaxb])
plt.ylim([1e-6, 100])
plt.yticks([1e-6, 1e-3, 1])
plt.setp(ax5b.get_xticklabels(), visible=False)

ax6b = plt.axes([0.68, 0.11, 0.20, 0.09]) 
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'g-', t, data4['no3a'], 'm-')
plt.xlim([xminb, xmaxb])
plt.ylim([1e-6, 100])
plt.yticks([1e-6, 1e-3, 1])
plt.setp(ax6b.get_xticklabels(), visible=False)

fig = plt.gcf()
fig.set_size_inches(16, 12)
plt.savefig('brw500yl.pdf')
plt.savefig('brw500yl.png')
#plt.show()
