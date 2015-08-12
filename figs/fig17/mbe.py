import numpy as np
import pylab as plt
import matplotlib.ticker as mtick
import sys as sys
import re

def readnbe(infile):
  ibe  = []
  nbe  = []
  lines = file(infile).readlines()

  for line in lines:
    m = re.match(".*nbalance error =(.*) column = (.*) step = (.*)", line)
    if m:
      nbe.append(float(m.group(1)))
      ibe.append(int(m.group(3)))


  ttt = np.zeros(len(ibe))
  for i in range(len(ibe)):
    ttt[i] = float(ibe[i])* 0.5 / 24.0 # / 365.0

  res = {}
  res['nbe'] = nbe
  res['time'] = ttt
  return res

def readcbe(infile):
  ibe  = []
  cbe  = []
  lines = file(infile).readlines()

  for line in lines:
    m = re.match(".*cbalance error =(.*) column = (.*) step = (.*)", line)
    if m:
      cbe.append(float(m.group(1)))
      ibe.append(int(m.group(3)))


  ttt = np.zeros(len(ibe))
  for i in range(len(ibe)):
    ttt[i] = float(ibe[i])* 0.5 / 24.0 #/ 365.0

  res = {}
  res['cbe'] = cbe
  res['time'] = ttt
  return res

nbe1 = readnbe('run6_1y/nbe.log')
cbe1 = readcbe('run6_1y/cbe.log')

#nbej = readnbe('run6_1yj/nbe.log')
#cbej = readcbe('run6_1yj/cbe.log')

nbes = readnbe('run6_1ys/nbe.log')
cbes = readcbe('run6_1ys/cbe.log')

lx = 0.04
ly = 0.88
plt.subplots_adjust(left=0.18, hspace=0.08) #, right=0.9, top=0.9, bottom=0.1)

ax1 = plt.subplot(2, 1, 1)
plt.plot(cbe1['time'], cbe1['cbe'], 'b+', cbes['time'], cbes['cbe'], 'gx')
plt.xlim([220, 365])
plt.ylim([0, 4.0e-4])
plt.yticks([0, 1e-4, 2e-4, 3e-4, 4e-4])
ax1.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
plt.text(lx, ly, '(a) C', transform=ax1.transAxes)
plt.ylabel('Mass balance error (g m$^{-2}$)')
plt.setp(ax1.get_xticklabels(), visible=False)

ax2 = plt.subplot(2, 1, 2)
plt.plot(nbe1['time'], nbe1['nbe'], 'b+', nbes['time'], nbes['nbe'], 'gx')
plt.xlim([220, 365])
plt.xlabel('Time (day)')
plt.ylabel('Mass balance error (g m$^{-2}$)')
ax2.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1e'))
plt.ylim([0, 2.0e-5])
lgd = plt.legend(('scaling update (STOL=10$^{-8}$, $\lambda_{min}=10^{-10}$)', 'scaling update (STOL=10$^{-50}$, $\lambda_{min}=10^{-50}$)'),loc=1)
lgd.draw_frame(False)
txt = lgd.get_texts();
plt.setp(txt, fontsize='medium');
plt.text(lx, ly, '(b) N', transform=ax2.transAxes)

fig = plt.gcf()
fig.set_size_inches(7, 9)
plt.savefig('mbe.png')
plt.savefig('mbe.pdf')
plt.show()

