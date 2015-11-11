import numpy as np
import sys as sys
import h5py
from scipy.io import netcdf
import matplotlib.pyplot as plt

def openncyear(nm,ny0,ny1):
  nh4a     = []
  ndmd     = []

  ny = ny1 -ny0

  for i in range(ny):
	fname = nm + '.h0.' + '%04d'%(ny0+i+1) + '-' + '01-01-00000.nc'
	f = netcdf.netcdf_file(fname, 'r')
        nh4a.append(f.variables['SMIN_NH4'][:, 0].copy())
	f.close()

  for i in range(ny):
	fname = nm + '.h1.' + '%04d'%(ny0+i+1) + '-' + '01-01-00000.nc'
	f = netcdf.netcdf_file(fname, 'r')
        ndmd.append(f.variables['PLANT_NDEMAND'][:, 0].copy())
	f.close()

  data = {}
  data['nh4a'] = np.asarray(nh4a).reshape(ny*365*48, 1)
  data['ndmd'] = np.asarray(ndmd).reshape(ny*365*48, 1)
  return data

def openh5data(nm):
  f0 = h5py.File(nm, 'r')

  tt       = []
  ngasmin  = []

  for i in f0.keys():
    title = i.split()
    if title[0] == u'Time:':
      tt.append(float(title[1]))	
      ngasmin.append( f0[i][u'NGASmin [mol_m^3]'][0,0,:])

  t  = sorted(tt)
  it = sorted(range(len(tt)), key=lambda k: tt[k])
  nt = len(tt)
  nx = 10

  sngasmin  = np.zeros((nt,nx))
 

  for i in range(len(tt)):
    if len(ngasmin) > 0:
      sngasmin[i,:] =ngasmin[it[i]]

  data = {}
  data['TIME']     = np.asarray(t) * 365.0
  data['NGASmin']  = sngasmin  

  f0.close()
  return data

ny0 = 0
ny1 = 1

nc1 = openncyear('run1y0a/BR-Cax_I1850CLM45CN_ad_spinup.clm2', ny0, ny1)
nc2 = openncyear('run1y0e/BR-Cax_I1850CLM45CN_ad_spinup.clm2', ny0, ny1)
nc3 = openncyear('run1y0d/BR-Cax_I1850CLM45CN_ad_spinup.clm2', ny0, ny1)

h51 = openh5data('run1y0a/BR-Cax_I1850CLM45CN_ad_spinup-000.h5')
h52 = openh5data('run1y0e/BR-Cax_I1850CLM45CN_ad_spinup-000.h5')
h53 = openh5data('run1y0d/BR-Cax_I1850CLM45CN_ad_spinup-000.h5')

t = ny0 + np.arange((ny1-ny0)*365*48)/48.0

lx = 0.02
ly = 0.88
xmin = 250.0 #0.6
xmax = 260.0 #0.8
plt.subplots_adjust(hspace=0.001)


ax1=plt.subplot(2, 1, 1)
plt.semilogy(t, nc1['nh4a'], 'b-', t, nc2['nh4a'], 'r-', t, nc3['nh4a'], 'g-')
plt.xlim([xmin, xmax])
plt.ylim([1e-7, 1e-3])
plt.yticks([1e-6, 1e-5, 1e-4])
plt.ylabel('NH${_4}^+$ (gN m$^{-2}$)')
plt.text(lx, ly, '(a)', transform=ax1.transAxes)
ax2 = ax1.twinx()
ax2.plot(t, nc1['ndmd']*1e8, 'c:')
plt.xlim([xmin, xmax])
plt.ylim([0, 10])
plt.yticks([0, 3, 6, 9])
plt.ylabel('Demand (10$^{-8}$ gN m$^{-2}$ s$^{-1}$)')
lgd = plt.legend(('Plant nitrogen demand', ),loc=3)
lgd.draw_frame(False)

ax2=plt.subplot(2, 1, 2)
plt.semilogy(h51['TIME'], h51['NGASmin'].min(1), 'b-', h52['TIME'], h52['NGASmin'].min(1), 'r-', h53['TIME'], h53['NGASmin'].min(1), 'g-')
plt.text(lx, ly, '(b)', transform=ax2.transAxes)
plt.xlim([xmin, xmax])
plt.ylim([1e-40, 1e-8])
plt.yticks([1e-40, 1e-30, 1e-20, 1e-10])
plt.ylabel('N$_\mathrm{2}$O-N (mol m$^{-3}$)')
lgd = plt.legend(('STOL = 10$^{-10}$', 'STOL = 10$^{-30}$', 'STOL = 10$^{-50}$'),loc=4)
lgd.draw_frame(False)
#txt = lgd.get_texts();
#plt.setp(txt, fontsize='small');
plt.xlabel('Day in the first year')

xticklabels = ax1.get_xticklabels()
plt.setp(xticklabels, visible=False)

fig = plt.gcf()
fig.set_size_inches(8, 6)
plt.savefig('cax1yn2ostol0.pdf')
plt.savefig('cax1yn2ostol0.png')
#plt.show()

