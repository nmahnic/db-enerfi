import numpy as np
from numpy import pi
# from scipy.fft import fft, rfftfreq
from scipy.fft import rfft
from scipy.signal import find_peaks
# from scipy.signal import freqz
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
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
        print("Mean Current: ",np.mean(data['current']))
        print("Mean Voltage: ",np.mean(data['voltage']))
        current_balanced = data['current'] - np.mean(data['current'])
        voltage_balanced = -(data['voltage'] - np.mean(data['voltage']))
    
        print("Points Voltage", len(voltage_balanced))
        print("Points Current", len(current_balanced))

        SAMPLE_RATE = 2500  # Hertz
        DURATION = 1

        N = SAMPLE_RATE * DURATION

        f_signal = rfft(current_balanced)

        yf = f_signal.copy()
        xpeak,ypeak = find_peaks(abs(yf), distance=25)

        for x in range(5):
            yf[x] = 0


        order = 11
        fs = 2500      
        cutoff = 60
        fundamentalFrec = 50 
        current_fundamental = self.butter_lowpass_filter(current_balanced, cutoff, fs, order)
        voltage_fundamental = self.butter_lowpass_filter(voltage_balanced, cutoff, fs, order)

        xVoltage,yVoltage = find_peaks(voltage_fundamental, distance=50)
        xCurrent,yCurrent = find_peaks(current_fundamental, distance=50)

        # print(voltage_fundamental[xVoltage])
        # print(current_fundamental[xCurrent])

        yVoltageMean = np.mean(voltage_fundamental[xVoltage][3:])
        yCurrentMean = np.mean(current_fundamental[xCurrent][3:])
        print("yVoltage:")
        print(yVoltageMean)
        print("yCurrent:")
        print(yCurrentMean)

        current_max = 1135.8131103378914
        voltage_max = 1147.038207104175

        voltage_fixed = (voltage_fundamental*(214.5*(2**0.5))/voltage_max)*1.0
        current_fixed = (current_fundamental*(7.1*(2**0.5))/current_max)*1.0

        zeroCurrent = self.findCrossZero(current_fixed[200:])
        zeroVoltage = self.findCrossZero(voltage_fixed[200:])

        print("zeroCurrent = ",zeroCurrent)
        print("zeroVoltage = ",zeroVoltage)
        diffPhase = abs(zeroVoltage - zeroCurrent)*(1/fs)*(2*pi*fundamentalFrec)
        print("diffPhase = ", diffPhase)
        cosphi = abs(math.cos(diffPhase))
        senphi = abs(math.sin(diffPhase))

        # t = np.linspace(0, 1, len(current_fixed), endpoint=False)
        # plt.subplot(1, 1, 1)
        # plt.plot(t, current_balanced, linewidth=2, label='current_balanced')
        # plt.plot(t, current_fixed, 'g-', linewidth=2, label='filtered current')
        # plt.plot(t, voltage_fixed, 'r-', linewidth=2, label='filtered voltage')
        # plt.plot(voltage_fundamental, 'g-', linewidth=2, label='voltage_fundamental')
        # plt.plot(current_fundamental, 'r-', linewidth=2, label='current_fundamental')
        # plt.plot(xVoltage, voltage_fundamental[xVoltage], 'o')
        # plt.plot(xCurrent, current_fundamental[xCurrent], 'g^')
        # plt.xlabel('Time [sec]')
        # plt.xlabel('samples')
        # plt.grid()
        # plt.legend()
        # plt.show()

        irms_fundamental = self.rmsValue(current_fixed[200:], len(current_fixed[200:]))
        vrms_fundamental = self.rmsValue(voltage_fixed[200:], len(voltage_fixed[200:]))
        irms = self.rmsValue(current_fixed[200:], len(current_fixed[200:]))
        vrms = self.rmsValue(voltage_fixed[200:], len(voltage_fixed[200:]))

        active_power = irms_fundamental*vrms_fundamental*cosphi
        reactive_power = irms_fundamental*vrms_fundamental*senphi
        apparent_power = irms * vrms
        distortion_power = ((apparent_power**2)-(active_power**2)+(reactive_power**2))**.5
        pf_1 = apparent_power/active_power

        thd_value = self.thd(abs(yf), xpeak)
        df_value = self.distortionFactor(thd_value)
        pf_2 = df_value*cosphi
        
        print ("RMS:")
        print ("\t{:.4f}".format(irms),"A")
        print ("fo:\t{:.4f}".format(irms_fundamental),"A")
        print ("\t{:.4f}".format(vrms),"V")
        print ("fo:\t{:.4f}".format(vrms_fundamental),"V")

        
        print ("Total Harmonic Distortion:")
        print ("\t{:.4f}".format(thd_value*100),"%")

        
        print ("Distorsion factor:")
        print ("\t{:.4f}".format(df_value))

        print ("Displacement factor 'cos(phi)':")
        print ('\t',cosphi)

        print("Power Factor = Displacement Factor x Distortion Factor:")
        print ("pf_1\t{:.4f}".format(pf_1))
        print ("pf_2\t{:.4f}".format(pf_2))

        print("Power Factor = Displacement Factor x Distortion Factor:")
        print ("active power\t{:.4f}".format(active_power))
        print ("reactive power\t{:.4f}".format(reactive_power))
        print ("apparent power\t{:.4f}".format(apparent_power))
        print ("distotion power\t{:.4f}".format(distortion_power))
        
        res = {
            "active_power" : float(active_power),
            "cos_phi" : float(cosphi),
            "irms" : float(irms),
            "pf" : float(pf_1),
            "thd" : float(thd_value),
            "vrms" : float(vrms),
        }

        return res