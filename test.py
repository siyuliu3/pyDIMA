from pyDIMA import pyDIMA
from utils import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from sklearn.metrics import accuracy_score


"""Measurement Data
"""
raw_var = [[0.026996,0.068489,0.063984,0.060303,0.101124,0.071183,0.08174,0.064969,0.096239,0.086136,0.082412,0.072497,0.074126,0.066692,0.071178,0.069323],
[0.032395,0.117784,0.110352,0.132568,0.143023,0.055937,0.08653,0.114527,0.16135,0.111862,0.100805,0.106632,0.122906,0.101759,0.099857,0.095897]]

raw_del_vbl = [[0.014901,0.047735,0.065643,0.103899,0.122081,0.159625,0.172408,0.206304,0.235517,0.268179,0.284743,0.31687,0.343056,0.376996,0.39472,0.429525],
[0.014901,0.031402,0.047677,0.08292,0.107172,0.122541,0.12884,0.151114,0.184568,0.206578,0.216388,0.233944,0.257718,0.279392,0.292085,0.312799]]


#[2] is Vwl
raw_std_vs_vbl = [[80,160,240,320,400,480,560],
[0.6496,0.336,0.2128,0.168,0.14168,0.112,0.0784],[0.45,0.47,0.5,0.55,0.6,0.65,0.7]]

#pmisclassification rate
mis_rate = [28,15.5,8,7.5,6,5.5]




#####
Vwl_1 = 0.625
Vwl_2 = 0.55
maxVbl_0 = list()
std_0 = list()
myDIMA = pyDIMA(B, Vt,Vt_var,Nrow,Cblc,Ncol)
for i in range(0,2**(B)):
    W = np.zeros((int(Ncol/2)))
    W.fill(i)
    Vbl = myDIMA.FR(W,Vwl_1,model = "sqrt")
    std_0.append(np.std(Vbl)/np.mean(Vbl))
    maxVbl_0.append(np.mean(Vbl))


maxVbl_1 = list()
std_1 = list()
for i in range(0,2**(B)):
    W = np.zeros((int(Ncol/2)))
    W.fill(i)
    Vbl = myDIMA.FR(W,Vwl_2,model = "sqrt")
    std_1.append(np.std(Vbl)/np.mean(Vbl))
    maxVbl_1.append(np.mean(Vbl))




#plot

plt.figure(figsize=(20, 5))
plt.subplot(121)
plt.plot(std_0,'-or',label = r'$\Delta V_{BLmax}=$'+'{}mV'.format(np.asarray(maxVbl_0)[15]*1000))
plt.plot(std_1,'-ob',label = r'$\Delta V_{BLmax}=$'+'{}mV'.format(np.asarray(maxVbl_1)[15]*1000))
plt.plot(raw_var[0],'--r',label = 'Measured at Vwl='+'{}V'.format(Vwl_1))
plt.plot(raw_var[1],'--b',label = 'Measured at Vwl='+'{}V'.format(Vwl_2))
plt.xlabel("W",fontsize = 20)
plt.ylabel(r'$\frac{\sigma}{\mu}$',fontsize=20)
plt.legend(fontsize=10)


plt.subplot(122)
plt.plot(1000*np.asarray(maxVbl_0),'-or',label = r'$\Delta V_{BLmax}=$'+'{}mV'.format(np.asarray(maxVbl_0)[15]*1000))
plt.plot(1000*np.asarray(maxVbl_1),'-ob',label = r'$\Delta V_{BLmax}=$'+'{}mV'.format(np.asarray(maxVbl_1)[15]*1000))
plt.plot(1000*np.asarray(raw_del_vbl[0]),'--r',label = 'Measured at Vwl='+'{}V'.format(Vwl_1))
plt.plot(1000*np.asarray(raw_del_vbl[1]),'--b',label = 'Measured at Vwl='+'{}V'.format(Vwl_2))
plt.xlabel("W",fontsize = 20)
plt.ylabel(r'$\Delta V_{BL} \/\/(mV)$',fontsize=20)
plt.legend(fontsize = 10)

plt.tight_layout()

plt.savefig('Example.png',format = 'png')
plt.show()
