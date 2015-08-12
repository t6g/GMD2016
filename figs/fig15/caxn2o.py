import numpy as np
import h5py
import sys as sys
import matplotlib.pyplot as plt


def openh5data(nm):
  f0 = h5py.File(nm, 'r')

  tt       = []
  ngasmin  = []

  for i in f0.keys():
    title = i.split()
    if title[0] == u'Time:':
      if (float(title[1]) > 0.0):
        tt.append(float(title[1])*365.0)	
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
  data['TIME']     = t
  data['NGASmin']  = sngasmin  

  f0.close()
  return data
if (len(sys.argv) > 1):
  nm = sys.argv[1]

#ofname = nm + '-nl.pdf'
#nm = nm + '.h5'
res = openh5data('../run6_1y/BR-Cax_I1850CLM45CN_ad_spinup-000.h5')

t    = res['TIME']
ngasmin  = res['NGASmin']

lx = 0.05
ly = 0.9
xmin = 250
xmax = 256

plt.semilogy(t, ngasmin[:,9], 'b-', t, ngasmin[:,8], 'r-', t, ngasmin[:, 7], 'g-')
plt.xlim([xmin, xmax])
plt.ylim([1e-20, 1e-5])
plt.xlabel('Elapsed time (d)')
plt.ylabel('Concentration (mol m$^{-3}$)')
lgd = plt.legend(('Layer 1', 'Layer 2', 'Layer 3'),loc=3)
lgd.draw_frame(False)
plt.yticks([1e-20, 1e-15, 1e-10, 1e-5])

fig = plt.gcf()
fig.set_size_inches(6, 4.5)
plt.savefig('caxn2o.pdf')
#plt.show()
