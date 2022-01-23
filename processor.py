import json
import numpy as np
from numpy import pi
from scipy.fft import fft
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks


class Processor:

    def rmsValue(self, arr, n):
        square = 0
        mean = 0.0
        root = 0.0
        
        #Calculate square
        for i in range(0,n):
            square += (arr[i]**2)
        
        #Calculate Mean
        mean = (square / (float)(n)) 

        #Calculate Root
        root = mean**.5
        
        return root

    def thd(self, abs_data,xpeak):  
        sq_sum=0.0
        for r in range(len(abs_data)):
            if(r in xpeak):
                sq_sum = sq_sum + (abs_data[r])**2

        sq_harmonics = sq_sum -(max(abs_data))**2
        thd = sq_harmonics**0.5 / max(abs_data)

        return thd

    def distortionFactor(self, thd):
        den = 1+(thd**2)
        return (1/den)**.5
    

    def task(self,data):
        sample_balanced = data['current'] - np.mean(data['current'])


        abs_yf = np.abs(fft(sample_balanced))

        SAMPLE_RATE = 2500  # Hertz
        DURATION = 1

        N = SAMPLE_RATE * DURATION

        f_signal = rfft(sample_balanced)
        xf = rfftfreq(N, 1 / SAMPLE_RATE)

        yf = f_signal.copy()
        xpeak,ypeak = find_peaks(abs(yf), distance=25)
        # yf[(np.abs(xf)>3)] = 0 # cut signal above 3Hz


        for x in range(5):
            yf[x] = 0


        # time = np.linspace(0.0, 0.4, int(0.4)/1e-4)
        # waveofSin = (2**.5)*np.cos(2.0*pi*50*time)    
        # n = len(waveofSin)
        irms = self.rmsValue(sample_balanced, len(sample_balanced))
        vrms = irms
        print ("RMS:")
        print ("\t{:.4f}".format(irms),"A")

        thd_value = self.thd(abs(yf), xpeak)
        print ("Total Harmonic Distortion:")
        print ("\t{:.4f}".format(thd_value*100),"%")

        df_value = self.distortionFactor(thd_value)
        print ("Distorsion factor:")
        print ("\t{:.4f}".format(df_value))

        print ("Displacement factor 'cos(phi)':")
        cosphi = 0
        print ('\t',cosphi)

        print("Power Factor = Displacement Factor x Distortion Factor:")
        pf = df_value+cosphi
        print ("\t{:.4f}".format(pf))


        res = {
            "active_power" : float(vrms*irms),
            "cos_phi" : float(cosphi),
            "irms" : float(irms),
            "pf" : float(pf),
            "thd" : float(thd_value),
            "vrms" : float(vrms),
        }

        return res