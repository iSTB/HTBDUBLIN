"""
                print(av)
Read from a single sensor socket and sends values out as OSC.

author: Frank Loesche <Frank.Loesche@Plymouth.ac.uk>
"""
from Sensor import Sensor
import sys
import matplotlib.pyplot as plt

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
        plt.ion()
        self.axes = plt.gca()

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


                self.globalc+=1
                yield av 

b  = Band("192.168.0.154", 301)
for d in b.averaged():
    print(d)
