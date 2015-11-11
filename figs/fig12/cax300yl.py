import numpy as np
import sys as sys
from scipy.io import netcdf
import matplotlib.pyplot as plt

def openncyear(nm,ny0,ny1):
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
        litc.append(f.variables['TOTLITN'][:, 0].copy())
        somc.append(f.variables['TOTSOMN'][:, 0].copy())
        vegc.append(f.variables['TOTVEGN'][:, 0].copy())
        tlai.append(f.variables['TLAI'][:, 0].copy())
        nh4a.append(f.variables['SMIN_NH4'][:, 0].copy())
        no3a.append(f.variables['SMIN_NO3'][:, 0].copy())
	f.close()

  data = {}
  data['litc'] = np.asarray(litc).reshape(ny*365, 1)
  data['somc'] = np.asarray(somc).reshape(ny*365, 1)
  data['vegc'] = np.asarray(vegc).reshape(ny*365, 1)
  data['tlai'] = np.asarray(tlai).reshape(ny*365, 1)
  data['nh4a'] = np.asarray(nh4a).reshape(ny*365, 1)
  data['no3a'] = np.asarray(no3a).reshape(ny*365, 1)
  return data

ny0 = 0
ny1 = 300

data1 = openncyear('../run-clm/BR-Cax_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data2 = openncyear('../run3l/BR-Cax_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data3 = openncyear('../run6l/BR-Cax_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data4 = openncyear('../run9l/BR-Cax_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)

t = ny0 + np.arange((ny1-ny0)*365)/365.0

lx = 0.02
ly = 0.88
xmax = 100
plt.subplots_adjust(hspace=0.001)

ax1=plt.subplot(6, 1, 1)
plt.plot(t, data1['tlai'], 'b-', t, data2['tlai'], 'r-', t, data3['tlai'], 'm-', t, data4['tlai'], 'g-')
plt.xlim([0, xmax])
plt.ylim([0, 5])
plt.yticks([0, 2, 4])
plt.ylabel('LAI')
plt.text(lx, ly, '(a)', transform=ax1.transAxes)
lgd = plt.legend(('CLM4.5', 'CLM-PF ($k_\mathrm{m} = 10^{-3}$)', 'CLM-PF ($k_\mathrm{m} = 10^{-6}$)', 'CLM-PF ($k_\mathrm{m} = 10^{-9}$)'),loc=2)
lgd.draw_frame(False)
txt = lgd.get_texts();
plt.setp(txt, fontsize='small');

ax2=plt.subplot(6, 1, 2)
plt.plot(t, data1['vegc'], 'b-', t, data2['vegc'], 'r-', t, data3['vegc'], 'm-', t, data4['vegc'], 'g-')
plt.xlim([0, xmax])
plt.ylim([0, 100])
plt.yticks([0, 30, 60])
plt.ylabel('VEGN (gN m$^{-2}$)')
plt.text(lx, ly, '(b)', transform=ax2.transAxes)

ax2a = plt.axes([0.16, 0.67, 0.27, 0.09]) 
plt.plot(t, data1['vegc'], 'b-', t, data2['vegc'], 'r-', t, data3['vegc'], 'm-', t, data4['vegc'], 'g-')
plt.xlim([0, ny1])
plt.ylim([0, 90])
plt.yticks([0, 30, 60])
plt.xticks([0, 100, 200, 300])

ax3=plt.subplot(6, 1, 3)
plt.plot(t, data1['litc'], 'b-', t, data2['litc'], 'r-', t, data3['litc'], 'm-', t, data4['litc'], 'g-')
plt.xlim([0, xmax])
plt.ylim([0, 1.5])
plt.yticks([0, .5, 1])
plt.ylabel('LITN (gN m$^{-2}$)')
plt.text(lx, ly, '(c)', transform=ax3.transAxes)

ax4=plt.subplot(6, 1, 4)
plt.plot(t, data1['somc'], 'b-', t, data2['somc'], 'r-', t, data3['somc'], 'm-', t, data4['somc'], 'g-')
plt.xlim([0, xmax])
plt.ylim([0, 35])
plt.yticks([0, 10, 20 ,30])
plt.ylabel('SOMN (gN m$^{-2}$)')
plt.text(lx, ly, '(d)', transform=ax4.transAxes)

ax5=plt.subplot(6, 1, 5)
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'm-', t, data4['nh4a'], 'g-')
plt.xlim([0, xmax])
plt.ylim([1e-5, 10])
plt.yticks([1e-5, 1e-3, 1e-1])
plt.ylabel('NH${_4}^+$ (gN m$^{-2}$)')
plt.text(lx, ly, '(e)', transform=ax5.transAxes)

ax6=plt.subplot(6, 1, 6)
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'm-', t, data4['no3a'], 'g-')
plt.ylim([1e-5, 10])
plt.yticks([1e-5, 1e-3, 1e-1])
plt.xlim([0, xmax])
plt.ylabel('NO${_3}^-$ (gN m$^{-2}$)')
plt.xlabel('Elapsed time (y)')
plt.text(lx, ly, '(f)', transform=ax6.transAxes)

xticklabels = ax1.get_xticklabels() + ax2.get_xticklabels() + ax3.get_xticklabels() + ax4.get_xticklabels() + ax5.get_xticklabels()
plt.setp(xticklabels, visible=False)

ax4a = plt.axes([0.16, 0.40, 0.27, 0.09]) 
plt.plot(t, data1['somc'], 'b-', t, data2['somc'], 'r-', t, data3['somc'], 'm-', t, data4['somc'], 'g-')
plt.xlim([0, ny1])
plt.ylim([0, 35])
plt.yticks([0, 10, 20])
plt.xticks([0, 100, 200])

xmina = 0
xmaxa = 1

ax5a = plt.axes([0.71, 0.24, 0.18, 0.07]) 
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'm-', t, data4['nh4a'], 'g-')
plt.xlim([xmina, xmaxa])
plt.ylim([1e-6, 1])
plt.yticks([1e-6, 1e-3, 1])
#plt.setp(ax5a.get_xticklabels(), visible=False)

ax6a = plt.axes([0.71, 0.11, 0.18, 0.07]) 
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'm-', t, data4['no3a'], 'g-')
plt.xlim([xmina, xmaxa])
plt.ylim([1e-6, 1])
plt.yticks([1e-6, 1e-3, 1])
plt.setp(ax6a.get_xticklabels(), visible=False)

"""
xminb = 79
xmaxb = 80

ax5b = plt.axes([0.68, 0.24, 0.20, 0.09]) 
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'g-', t, data4['nh4a'], 'm-')
plt.xlim([xminb, xmaxb])
plt.ylim([1e-9, 10])
plt.yticks([1e-9, 1e-6, 1e-3, 1])
plt.setp(ax5b.get_xticklabels(), visible=False)

ax6b = plt.axes([0.68, 0.11, 0.20, 0.09]) 
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'g-', t, data4['no3a'], 'm-')
plt.xlim([xminb, xmaxb])
plt.ylim([1e-9, 10])
plt.yticks([1e-9, 1e-6, 1e-3, 1])
plt.setp(ax6b.get_xticklabels(), visible=False)
"""
fig = plt.gcf()
fig.set_size_inches(16, 12)
plt.savefig('cax300yl.pdf')
plt.savefig('cax300yl.png')
#plt.show()
