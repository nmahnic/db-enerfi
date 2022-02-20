import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks

import json

def thd(abs_data,xpeak):  
    sq_sum=0.0
    print("largo de xpeak ",len(xpeak))
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


filename = 'rectifcadorDiodo/sample2022_02_19-03_40_35_PM.json'
# filename = "sinRectificar/sample2022_02_19-03_57_56_PM.json"
f = open(filename)
jsonData = json.load(f)
f.close()

tension = jsonData["voltage"]
corriente = jsonData["current"]


sample_balanced = corriente - np.mean(corriente)

abs_yf = np.abs(fft(sample_balanced))

SAMPLE_RATE = 2500  # Hertz
DURATION = 1

N = SAMPLE_RATE * DURATION

f_signal = rfft(sample_balanced)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

yf = f_signal.copy()
xpeak,ypeak = find_peaks(abs(yf), distance=40)

for x in range(5):
    yf[x] = 0


maxYf = np.amax(np.abs(yf))
print("MAX -> ",maxYf)
# X = xpeak
# Y = np.abs(yf[xpeak])/maxYf

valores = []
xpeak = np.delete(xpeak,0)

for i in range(11):
    xpeak = np.delete(xpeak,len(xpeak)-1)

for i in xpeak:
    valores.append(np.abs(yf[i])/maxYf)

fig, ax = plt.subplots()

# Save the chart so we can loop through the bars below.
bars = ax.bar(
    x=np.arange(xpeak.size),
    height=valores,
    # tick_label=xpeak
    # tick_label=[50,100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000,1050,1100,1150,1200]
    tick_label=range(1,xpeak.size+1)
)

# Axis formatting.
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.set_axisbelow(True)
ax.yaxis.grid(True, color='#EEEEEE')
ax.xaxis.grid(False)

# Grab the color of the bars so we can make the
# text the same color.
bar_color = bars[0].get_facecolor()

# Add text annotations to the top of the bars.
# Note, you'll have to adjust this slightly (the 0.3)
# with different data.
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.01,
        round(round(bar.get_height(), 3)*100,1),
        horizontalalignment='center',
        color=bar_color,
        weight='bold'
    )

# Add labels and a title.
ax.set_xlabel('Number of harmonic, fo=50Hz', labelpad=15, color='#333333')
ax.set_ylabel('Percentage', labelpad=15, color='#333333')
ax.set_title('Harmoics of Measure 19/02/2022 03:40:35 PM', pad=15, color='#333333', weight='bold')

fig.tight_layout()



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