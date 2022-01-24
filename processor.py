import numpy as np
from numpy import pi
# from scipy.fft import fft, rfftfreq
from scipy.fft import rfft
from scipy.signal import find_peaks
# from scipy.signal import freqz
from scipy.signal import butter, lfilter
# import matplotlib.pyplot as plt
import math

class Processor:

    def findCrossZero(self, measure):
        return np.where(np.diff(np.sign(measure)))[0][0]

    def butter_lowpass(self, cutoff, fs, order=5):
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return b, a

    def butter_lowpass_filter(self, data, cutoff, fs, order=5):
        b, a = self.butter_lowpass(cutoff, fs, order=order)
        y = lfilter(b, a, data)
        return y

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
        current_balanced = data['current'] - np.mean(data['current'])
        voltage_balanced = data['voltage'] - np.mean(data['voltage'])

        # abs_yf = np.abs(fft(current_balanced))

        SAMPLE_RATE = 2500  # Hertz
        DURATION = 1

        N = SAMPLE_RATE * DURATION

        f_signal = rfft(current_balanced)
        # xf = rfftfreq(N, 1 / SAMPLE_RATE)

        yf = f_signal.copy()
        xpeak,ypeak = find_peaks(abs(yf), distance=25)
        # yf[(np.abs(xf)>3)] = 0 # cut signal above 3Hz


        for x in range(5):
            yf[x] = 0


        order = 11
        fs = 2500      
        cutoff = 60
        fundamentalFrec = 50 
        current_fundamental = self.butter_lowpass_filter(current_balanced, cutoff, fs, order)
        voltage_fundamental = self.butter_lowpass_filter(voltage_balanced, cutoff, fs, order)

        t = np.linspace(0, 1, len(current_balanced), endpoint=False)

        zeroCurrent = self.findCrossZero(current_fundamental)
        zeroVoltage = self.findCrossZero(voltage_fundamental)

        print("zeroCurrent = ",zeroCurrent)
        print("zeroVoltage = ",zeroVoltage)
        diffPhase = abs(zeroVoltage - zeroCurrent)*(1/fs)*(2*pi*fundamentalFrec)
        print("diffPhase = ", diffPhase)
        cosphi = math.cos(diffPhase)

        # plt.subplot(2, 1, 2)
        # plt.plot(t, current_balanced, 'b-', label='data')
        # plt.plot(t, current_fundamental, 'g-', linewidth=2, label='filtered current')
        # plt.plot(t, voltage_fundamental, 'r-', linewidth=2, label='filtered voltage')
        # plt.xlabel('Time [sec]')
        # plt.grid()
        # plt.legend()

        # plt.subplots_adjust(hspace=0.35)
        # plt.show()

        irms = self.rmsValue(current_balanced, len(current_balanced))
        vrms = self.rmsValue(voltage_balanced, len(voltage_balanced))

        print ("RMS:")
        print ("\t{:.4f}".format(irms),"A")
        print ("\t{:.4f}".format(vrms),"V")

        thd_value = self.thd(abs(yf), xpeak)
        print ("Total Harmonic Distortion:")
        print ("\t{:.4f}".format(thd_value*100),"%")

        df_value = self.distortionFactor(thd_value)
        print ("Distorsion factor:")
        print ("\t{:.4f}".format(df_value))

        print ("Displacement factor 'cos(phi)':")
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