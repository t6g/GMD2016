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
ny1 = 300

#if(len(sys.argv) > 0):
#  ny1 = int(sys.argv[1])

data1 = openncyear('../run-clm/US-Pit_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data2 = openncyear('../run3l/US-Pit_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data3 = openncyear('../run6l/US-Pit_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data4 = openncyear('../run9l/US-Pit_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)

t = ny0 + np.arange((ny1-ny0)*365)/365.0


plt.subplots_adjust(hspace=0.001)
lx = 0.01
ly = 0.88
xmax = 100

ax1=plt.subplot(6, 1, 1)
plt.plot(t, data1['tlai'], 'b-', t, data2['tlai'], 'r-', t, data3['tlai'], 'm-', t, data4['tlai'], 'g-')
plt.xlim([0, xmax])
plt.ylim([0, 12])
plt.yticks([0, 5, 10])
plt.ylabel('LAI')
plt.text(lx, ly, '(a)', transform=ax1.transAxes)
lgd = plt.legend(('CLM4.5', 'CLM-PF ($k_\mathrm{m} = 10^{-3}$)', 'CLM-PF ($k_\mathrm{m} = 10^{-6}$)', 'CLM-PF ($k_\mathrm{m} = 10^{-9}$)'),loc=2)
lgd.draw_frame(False)

ax2=plt.subplot(6, 1, 2)
plt.plot(t, data1['vegc'], 'b-', t, data2['vegc'], 'r-', t, data3['vegc'], 'm-', t, data4['vegc'], 'g-')
plt.xlim([0, xmax])
plt.yticks([0, 50, 100])
plt.ylim([0, 150])
txt = lgd.get_texts();
plt.setp(txt, fontsize='small');
plt.text(lx, ly, '(b)', transform=ax2.transAxes)
plt.ylabel('VEGN (gN m$^{-2}$)')

ax2a = plt.axes([0.15, 0.67, 0.27, 0.09]) 
plt.plot(t, data1['vegc'], 'b-', t, data2['vegc'], 'r-', t, data3['vegc'], 'm-', t, data4['vegc'], 'g-')
plt.yticks([0, 40, 80])
plt.xticks([0, 100, 200])
plt.ylim([0, 120])

ax3=plt.subplot(6, 1, 3)
plt.plot(t, data1['litc'], 'b-', t, data2['litc'], 'r-', t, data3['litc'], 'm-', t, data4['litc'], 'g-')
plt.xlim([0, xmax])
plt.ylim([0, 10])
plt.yticks([0, 4, 8])
plt.ylabel('LitN (gN m$^{-2}$)')
plt.text(lx, ly, '(c)', transform=ax3.transAxes)

ax4=plt.subplot(6, 1, 4)
plt.plot(t, data1['somc'], 'b-', t, data2['somc'], 'r-', t, data3['somc'], 'm-', t, data4['somc'], 'g-')
plt.xlim([0, xmax])
plt.ylim([0, 80])
plt.yticks([0, 25, 50])
plt.ylabel('SOMN (g m$^{-2}$)')
plt.text(lx, ly, '(d)', transform=ax4.transAxes)

ax5=plt.subplot(6, 1, 5)
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'm-', t, data4['nh4a'], 'g-')
plt.xlim([0, xmax])
plt.ylim([1e-6, 10])
plt.yticks([1e-6, 1e-3, 1e-0])
plt.ylabel('NH${_4}^+$ (gN m$^{-2}$)')
plt.text(lx, ly, '(e)', transform=ax5.transAxes)

ax6=plt.subplot(6, 1, 6)
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'm-', t, data4['no3a'], 'g-')
plt.xlim([0, xmax])
plt.ylim([1e-6, 100])
plt.yticks([1e-6, 1e-3, 1e-0])
plt.ylabel('NO${_3}^-$ (gN m$^{-2}$)')
plt.xlabel('Elapsed time (y)')
plt.text(lx, ly, '(f)', transform=ax6.transAxes)

ax4a = plt.axes([0.15, 0.40, 0.27, 0.09]) 
plt.plot(t, data1['somc'], 'b-', t, data2['somc'], 'r-', t, data3['somc'], 'm-', t, data4['somc'], 'g-')
plt.xlim([0, ny1])
plt.ylim([0, 80])
plt.yticks([0, 25, 50])
plt.xticks([0, 100, 200])

ax5a = plt.axes([0.68, 0.24, 0.20, 0.09]) 
plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'm-', t, data4['nh4a'], 'g-')
plt.xlim([5, 10])
plt.ylim([1e-9, 1])
plt.yticks([1e-8, 1e-5, 1e-2])

#ax6a = plt.axes([0.68, 0.11, 0.20, 0.09]) 
#plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'g-', t, data4['no3a'], 'm-')
#plt.xlim([0, 10])
#plt.ylim([1e-8, 10])
#plt.yticks([1e-8, 1e-5, 1e-2])
#plt.setp(ax6a.get_xticklabels(), visible=False)

#ax5b = plt.axes([0.68, 0.24, 0.20, 0.09]) 
#plt.semilogy(t, data1['nh4a'], 'b-', t, data2['nh4a'], 'r-', t, data3['nh4a'], 'g-', t, data4['nh4a'], 'm-')
#plt.xlim([70, 80])
#plt.ylim([1e-8, 10])
#plt.yticks([1e-8, 1e-5, 1e-2])

ax6b = plt.axes([0.68, 0.11, 0.20, 0.09]) 
#plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'g-', t, data4['no3a'], 'm-')
plt.semilogy(t, data1['no3a'], 'b-', t, data2['no3a'], 'r-', t, data3['no3a'], 'm-', t, data4['no3a'], 'g-')
plt.xlim([5, 10])
plt.ylim([1e-9, 1])
plt.yticks([1e-8, 1e-5, 1e-2])
#plt.xlim([295, 300])
#plt.ylim([20, 50])
#plt.yticks([30, 40])
#plt.setp(ax6b.get_xticklabels(), visible=False)

xticklabels = ax1.get_xticklabels() + ax2.get_xticklabels() + ax3.get_xticklabels() + ax4.get_xticklabels() + ax5.get_xticklabels()
plt.setp(xticklabels, visible=False)

fig = plt.gcf()
fig.set_size_inches(16, 12)
plt.savefig('pit300yl.pdf')
plt.savefig('pit300yl.png')
#plt.show()
