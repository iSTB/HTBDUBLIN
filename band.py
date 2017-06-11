"""
                print(av)
Read from a single sensor socket and sends values out as OSC.

author: Frank Loesche <Frank.Loesche@Plymouth.ac.uk>
"""
from Sensor import Sensor
import sys
import matplotlib.pyplot as plt
import time
import numpy as np
class Band(object):
    def __init__(self,ip="192.168.0.154",port= 301):
        self.ip = ip
        self.port = port
        try:
            self.s = Sensor(self.ip, self.port)
        except OSError:
            print("Could not connect to device with IP %s" % (arguments.sensorip))
            sys.exit(1)
        self.raw = self.read_raw()
        self.data = []
        self.globalc = 0
        #plt.ion()
        #self.axes = plt.gca()
    def read_raw(self):
        for line in self.s.get_measures(as_float=True):
            # This is where the mapping from measures (array of values) to Bundle is
            # happening.
            yield line[2]
    def averaged(self, window=10, plot=True):
        c = 0
        t= 0
        for d in self.raw:
            t += d
            c+=1
            if c == window:
                av = t/c
                c =0
                t =0
                if plot:
                    self.axes.set_xlim(self.globalc -50, self.globalc +50)
                    self.axes.set_ylim(0.9, 1.)
                    self.axes.relim()
                    self.axes.autoscale_view()
                    plt.scatter(self.globalc,av,color="black")
                    plt.pause(0.00000000000001)
                self.globalc+=1
                yield av 

    def get_freq(self,sample_time):
        """
        Gets the breathing frequecny over sample_time
        """
        data = []
        time1 = time.time() 
        for d in self.read_raw():
            data.append(d)
            time2 = time.time()
            print(time2-time1)
            if time2 - time1 >= sample_time:
                break           
        
        bigg = max(data)

        data = [d-bigg for d in data]
        data = [data[0]]*1000 + data + [data[-1]]*1000
        
        spectrum = np.fft.fft(data)
        spectrum = np.abs(spectrum)
        bigg = max([data])
        

        frq = np.fft.fftfreq(len(data))
        frq = frq[:15]
        spectrum= spectrum[:15]
        tot = 0
        for i in range(len(frq)):
            tot += frq[i] * spectrum[i]
        tot /= len(frq)
        
        
        print(tot)
        return tot 
         

        fig, ax = plt.subplots(2, 1)
        ax[0].plot(range(len(data)),data)
        ax[0].set_xlabel('Time')
        ax[0].set_ylabel('Amplitude')
        ax[1].plot(frq,spectrum,'r') # plotting the spectrum
        ax[1].set_xlabel('Freq (Hz)')
        ax[1].set_ylabel('|Y(freq)|')
        plt.show()
        #plot_url = plt.plot_mpl(fig, filename='mpl-basic-fft')



    #def get_freq

b  = Band("192.168.0.154", 301)
b.get_freq(30)
#for d in b.averaged():
#    print(d)
    

