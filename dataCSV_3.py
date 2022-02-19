import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks

import json

def thd(abs_data,xpeak):  
    sq_sum=0.0
    for r in range(len(abs_data)):
        if(r in xpeak):
            # print(abs_data[r],r)
            sq_sum = sq_sum + (abs_data[r])**2

    sq_harmonics = sq_sum -(max(abs_data))**2
    thd = sq_harmonics**0.5 / max(abs_data)

    return thd

def distortionFactor(thd):
    den = 1+(thd**2)
    return (1/den)**.5
 


t = []
tension = []
corriente = []


filename = "measuresByDate/sample2022_02_19-03_20_37_PM.json"
f = open(filename)
jsonData = json.load(f)
f.close()

tension = jsonData["voltage"]
corriente = jsonData["current"]


sample_balanced = corriente - np.mean(corriente)

fig, axs = plt.subplots(3)
axs[0].plot(sample_balanced)
axs[1].plot(sample_balanced)
axs[1].set_xlim([0,200])
abs_yf = np.abs(fft(sample_balanced))

SAMPLE_RATE = 2500  # Hertz
DURATION = 1

N = SAMPLE_RATE * DURATION

f_signal = rfft(sample_balanced)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

yf = f_signal.copy()
xpeak,ypeak = find_peaks(abs(yf), distance=40)
# yf[(np.abs(xf)>3)] = 0 # cut signal above 3Hz


for x in range(5):
    yf[x] = 0


axs[2].plot(xf, np.abs(yf))
axs[2].set_xlim([0,900])
axs[2].plot(xpeak,np.abs(yf[xpeak]),'o')


# axs[1].set_ylim([100, yf.max()])
plt.savefig('medicion.png')

thd_value = thd(abs(yf), xpeak)
print ("Total Harmonic Distortion:")
print ("\t{:.4f}".format(thd_value*100),"%")

df_value = distortionFactor(thd_value)
print ("Distorsion factor:")
print ("\t{:.4f}".format(df_value))

print ("Displacement factor 'cos(phi)':")
cosphi = 0
print ('\t',cosphi)

print("Power Factor = Displacement Factor x Distortion Factor:")
print ("\t{:.4f}".format(df_value+cosphi))


plt.show()