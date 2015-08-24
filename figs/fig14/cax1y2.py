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
  data['litc'] = np.asarray(litc).reshape(ny*17520, 1)
  data['somc'] = np.asarray(somc).reshape(ny*17520, 1)
  data['vegc'] = np.asarray(vegc).reshape(ny*17520, 1)
  data['tlai'] = np.asarray(tlai).reshape(ny*17520, 1)
  data['nh4a'] = np.asarray(nh4a).reshape(ny*17520, 1)
  data['no3a'] = np.asarray(no3a).reshape(ny*17520, 1)
  return data

ny0 = 0
ny1 = 1

data1 = openncyear('../run6_1y/BR-Cax_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data2 = openncyear('../run6_1ys/BR-Cax_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)
data3 = openncyear('../run6_1yl/BR-Cax_I1850CLM45CN_ad_spinup.clm2.h0.', ny0, ny1)

t = ny0 + np.arange((ny1-ny0)*17520)/17520.0*365.0
ny1 = ny1 * 365.0
lx = 0.02
ly = 0.85
plt.subplots_adjust(hspace=0.001)

ax5=plt.subplot(2, 1, 1)
plt.semilogy(t[::48], data1['nh4a'][::48], 'ro:', t[::48], data2['nh4a'][::48], 'g+:', t[::48], data3['nh4a'][::48], 'b-', markersize=3)
plt.xlim([0, ny1])
plt.ylim([1e-7, 1e-0])
plt.yticks([1e-7, 1e-5, 1e-3, 1e-1])
plt.ylabel('NH${_4}^+$ (gN m$^{-2}$)')
plt.text(lx, ly, '(a)', transform=ax5.transAxes)
plt.setp(ax5.get_xticklabels(), visible=False)

ax6=plt.subplot(2, 1, 2)
plt.semilogy(t[::48], data1['no3a'][::48], 'ro:', t[::48], data2['no3a'][::48], 'g+:',  t[::48], data3['no3a'][::48], 'b-', markersize=3)
plt.ylim([1e-7, 1e-1])
plt.yticks([1e-7, 1e-5, 1e-3])
plt.xlim([0, ny1])
plt.ylabel('NO${_3}^-$ (gN m$^{-2}$)')
plt.xlabel('Elapsed time (d)')
plt.text(lx, ly, '(b)', transform=ax6.transAxes)
lgd = plt.legend(('scaling update (STOL=10$^{-8}$, $\lambda_{min}=10^{-10}$)', 'scaling update (STOL=10$^{-50}$, $\lambda_{min}=10^{-50}$)', 'Log transformation'),loc=2)
lgd.draw_frame(False)
txt = lgd.get_texts();
plt.setp(txt, fontsize='small');

xmina = 226
xmaxa = 230

ax5a = plt.axes([0.18, 0.57, 0.18, 0.18]) 
plt.semilogy(t, data1['nh4a'], 'r-', t, data2['nh4a'], 'g-', t, data3['nh4a'], 'b-')
plt.semilogy(t[::48], data1['nh4a'][::48], 'rx', t[::48], data2['nh4a'][::48], 'g+')
plt.xlim([xmina, xmaxa])
plt.xticks([226, 227, 228, 229, 230])
plt.ylim([1e-7, 1e-3])
plt.yticks([1e-7, 1e-5, 1e-3])
#plt.setp(ax5a.get_xticklabels(), visible=False)

ax6a = plt.axes([0.18, 0.15, 0.18, 0.18]) 
plt.semilogy(t, data1['no3a'], 'r-', t, data2['no3a'], 'g-', t, data3['no3a'], 'b-')
plt.semilogy(t[::48], data1['no3a'][::48], 'rx', t[::48], data2['no3a'][::48], 'g+')
plt.xlim([xmina, xmaxa])
plt.xticks([226, 227, 228, 229, 230])
#plt.xticks([226, 228, 230])
plt.ylim([1e-7, 1e-2])
plt.yticks([1e-7, 1e-5, 1e-3])
#plt.setp(ax6a.get_xticklabels(), visible=False)

xminb = 250
xmaxb = 254

ax5b = plt.axes([0.40, 0.57, 0.18, 0.18]) 
plt.semilogy(t, data1['nh4a'], 'r-', t, data2['nh4a'], 'g-', t, data3['nh4a'], 'b-')
plt.semilogy(t[::48], data1['nh4a'][::48], 'rx', t[::48], data2['nh4a'][::48], 'g+')
plt.xlim([xminb, xmaxb])
plt.xticks([250, 251, 252, 253, 254])
plt.ylim([1e-7, 1e-3])
plt.yticks([1e-7, 1e-5, 1e-3])
plt.setp(ax5b.get_yticklabels(), visible=False)

ax6b = plt.axes([0.40, 0.15, 0.18, 0.18]) 
plt.semilogy(t, data1['no3a'], 'r-', t, data2['no3a'], 'g-', t, data3['no3a'], 'b-')
plt.semilogy(t[::48], data1['no3a'][::48], 'rx', t[::48], data2['no3a'][::48], 'g+')
plt.xlim([xminb, xmaxb])
#plt.xticks([250, 252, 254])
plt.xticks([250, 251, 252, 253, 254])
plt.ylim([1e-7, 1e-2])
plt.yticks([1e-7, 1e-5, 1e-3])
plt.setp(ax6b.get_yticklabels(), visible=False)

xminc = 295
xmaxc = 300

ax5c = plt.axes([0.65, 0.71, 0.20, 0.18]) 
plt.semilogy(t, data1['nh4a'], 'r-', t, data2['nh4a'], 'g-', t, data3['nh4a'], 'b-')
plt.semilogy(t[::48], data1['nh4a'][::48], 'rx', t[::48], data2['nh4a'][::48], 'g+')
plt.xlim([xminc, xmaxc])
plt.xticks([295,296, 297, 298, 299, 300])
plt.ylim([1e-7, 1e-3])
plt.yticks([1e-7, 1e-5, 1e-3])
plt.setp(ax5c.get_yticklabels(), visible=False)

ax6c = plt.axes([0.65, 0.31, 0.20, 0.18]) 
plt.semilogy(t, data1['no3a'], 'r-', t, data2['no3a'], 'g-', t, data3['no3a'], 'b-')
plt.semilogy(t[::48], data1['no3a'][::48], 'rx', t[::48], data2['no3a'][::48], 'g+')
plt.xlim([xminc, xmaxc])
#plt.xticks([295, 298, 300])
plt.xticks([295,296, 297, 298, 299, 300])
plt.ylim([1e-7, 1e-2])
plt.yticks([1e-7, 1e-5, 1e-3])
plt.setp(ax6c.get_yticklabels(), visible=False)

fig = plt.gcf()
fig.set_size_inches(12, 8)
plt.savefig('cax1y2.pdf')
#plt.show()
