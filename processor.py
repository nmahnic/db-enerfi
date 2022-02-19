from fileinput import filename
import numpy as np
from numpy import pi
# from scipy.fft import fft, rfftfreq
from scipy.fft import rfft
from scipy.signal import find_peaks
# from scipy.signal import freqz
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
import math
from datetime import datetime
import json

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

        # Serializing json
        json_object = json.dumps(data, indent = 4)
        timestr = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        filename = "measuresByDate/sample" + timestr + ".json"
        # Writing to sample.json
        with open(filename, "w") as outfile:
            outfile.write(json_object)

        print("Mean Current: ",np.mean(data['current']))
        print("Mean Voltage: ",np.mean(data['voltage']))
        current_balanced = data['current'] - np.mean(data['current'])
        voltage_balanced = -(data['voltage'] - np.mean(data['voltage']))

        print("Points Voltage", len(voltage_balanced))
        print("Points Current", len(current_balanced))

        SAMPLE_RATE = 2500  # Hertz
        DURATION = 1

        N = SAMPLE_RATE * DURATION

        f_signal_i = rfft(current_balanced)
        f_signal_v = rfft(voltage_balanced)

        yf_i = f_signal_i.copy()
        yf_v = f_signal_v.copy()
        xpeak_i,ypeak_i = find_peaks(abs(yf_i), distance=40)
        xpeak_v,ypeak_v = find_peaks(abs(yf_v), distance=40)

        for x in range(5):
            yf_i[x] = 0
            yf_v[x] = 0


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
        print("yVoltage:",yVoltageMean)
        print("yCurrent:",yCurrentMean)

        voltage_max = 1139.488075375003
        current_max = 1113.97432640357
        
        voltage_fixed = (voltage_fundamental*(216.2*(2**0.5))/voltage_max)*1.0
        current_fixed = (current_fundamental*(7.66*(2**0.5))/current_max)*1.0

        zeroCurrent = self.findCrossZero(current_fixed[200:])
        zeroVoltage = self.findCrossZero(voltage_fixed[200:])

        print("zeroCurrent = ",zeroCurrent)
        print("zeroVoltage = ",zeroVoltage)
        diffPhase = abs(zeroVoltage - zeroCurrent)*(1/fs)*(2*pi*fundamentalFrec)
        print("diffPhase = ", diffPhase)

        # t = np.linspace(0, 1, len(current_fixed), endpoint=False)
        # plt.subplot(1, 1, 1)
        # # plt.plot(t, current_balanced, linewidth=2, label='current_balanced')
        # # plt.plot(t, current_fixed, 'g-', linewidth=2, label='filtered current')
        # # plt.plot(t, voltage_fixed, 'r-', linewidth=2, label='filtered voltage')
        # # plt.plot(voltage_fundamental, 'g-', linewidth=2, label='voltage_fundamental')
        # # plt.plot(current_fundamental, 'r-', linewidth=2, label='current_fundamental')
        # plt.plot(voltage_fixed, 'g-', linewidth=2, label='voltage_fixed')
        # plt.plot(current_fixed, 'r-', linewidth=2, label='current_fixed')
        # plt.plot(xVoltage, voltage_fundamental[xVoltage], 'o')
        # plt.plot(xCurrent, current_fundamental[xCurrent], 'g^')
        # # plt.xlabel('Time [sec]')
        # plt.xlabel('samples')
        # plt.grid()
        # plt.legend()
        # plt.show()

        irms_fundamental = self.rmsValue(current_fixed[200:], len(current_fixed[200:]))
        vrms_fundamental = self.rmsValue(voltage_fixed[200:], len(voltage_fixed[200:]))
        irms = self.rmsValue(current_fixed[200:], len(current_fixed[200:]))
        vrms = self.rmsValue(voltage_fixed[200:], len(voltage_fixed[200:]))

        # irms_fundamental = irms_fundamental + 0.1
        # vrms_fundamental = vrms_fundamental + 1.0
        # irms = irms + 0.1
        # vrms = vrms + 1.0

        print ("RMS:")
        print ("\t{:.4f}".format(irms),"A")
        # print ("fo:\t{:.4f}".format(irms_fundamental),"A")
        print ("\t{:.4f}".format(vrms),"V")
        # print ("fo:\t{:.4f}".format(vrms_fundamental),"V")

        if (irms > 0.8):
            cosphi = abs(math.cos(diffPhase))
            senphi = abs(math.sin(diffPhase))

            active_power = irms_fundamental*vrms_fundamental*cosphi
            reactive_power = irms_fundamental*vrms_fundamental*senphi
            apparent_power = irms * vrms
            distortion_power = ((apparent_power**2)-(active_power**2)+(reactive_power**2))**.5
            pf_1 = apparent_power/active_power

            v_harmonics=[]
            i_harmonics=[]

            harmonic1_v = abs(yf_v[xpeak_v[0]])
            harmonic1_i = abs(yf_i[xpeak_i[0]])
            for i in range(len(xpeak_v)):
                v_harmonics.append(abs(yf_v[xpeak_v[i]])/harmonic1_v)

            for i in range(len(xpeak_i)):
                i_harmonics.append(abs(yf_i[xpeak_i[i]])/harmonic1_i)

            # print ("V Harmonics':")
            # print (v_harmonics)

            # print ("I Harmonics':")
            # print (i_harmonics)

            thd_i = self.thd(abs(yf_i), xpeak_i)
            thd_v = self.thd(abs(yf_v), xpeak_v)


            df_value = self.distortionFactor(thd_i)
            pf_2 = df_value*cosphi

        else:
            irms = 0
            irms_fundamental = 0
            cosphi = 1
            senphi = 1

            active_power = 0
            reactive_power = 0
            apparent_power = 0
            distortion_power = ((apparent_power**2)-(active_power**2)+(reactive_power**2))**.5
            pf_1 = 1

            thd_i = 0
            thd_v = self.thd(abs(yf_v), xpeak_v)
            df_value = 1
            pf_2 = df_value*cosphi




        print ("Total Harmonic Distorsion 'THD I':")
        print ("\t{:.4f}".format(thd_i*100),"%")
        print ("Total Harmonic Distorsion 'THD V':")
        print ("\t{:.4f}".format(thd_v*100),"%")


        print ("Distorsion factor:")
        print ("\t{:.4f}".format(df_value))

        print ("Displacement factor 'cos(phi)':")
        print ('\t',cosphi)

        print("Power Factor = Displacement Factor x Distortion Factor:")
        # print ("pf_1\t{:.4f}".format(pf_1))
        # print ("pf_2\t{:.4f}".format(pf_2))
        print ("\t{:.4f}".format(pf_2))

        print("Power Factor = Displacement Factor x Distortion Factor:")
        print ("active power\t{:.4f}".format(active_power))
        print ("reactive power\t{:.4f}".format(reactive_power))
        print ("apparent power\t{:.4f}".format(apparent_power))
        print ("distotion power\t{:.4f}\n".format(distortion_power))

        res = {
            "active_power" : float(active_power),
            "cos_phi" : float(cosphi),
            "irms" : float(irms),
            "pf" : float(pf_2),
            "thd_i" : float(thd_i),
            "thd_v" : float(thd_v),
            "vrms" : float(vrms),
        }

        return res
