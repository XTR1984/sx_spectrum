import time
import math
import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation  


class SXScope(): #sx127x rssi getter
    def __init__(self, ser:serial.Serial):
        self.ser = ser
        pass
    def init(self):
        #init:gain:avgsamples:rxbxmant:rxbxexp:delay_us
        self.ser.write(b"Init:1:5:2:5:1000\n")
        self.ser.flush()
        l = self.ser.readline()
        if not l==b'Init ok\r\n':
          print("bad init")
        else:
          print("init ok")
        pass

    def setFreq(self, freq):
        req = "SetFreq:"+str(freq)+"\n"
        self.ser.write(req.encode("ASCII"))
        self.ser.flush()
        ok = self.ser.readline()
        if ok == b'OK':
           print("Set freq ok")
    
    def getRssi(self):
        req = "GetRSSI\n"
        self.ser.write(req.encode("ASCII"))
        self.ser.flush()
        rssi = self.ser.read()
        rssi = int(rssi[0])
        return -(int)(rssi)/2


    def animateRSSI(self, limits):
        y = -130* np.ones(200)
        fig, ax = plt.subplots()
        x = np.linspace(0, 200, 200)
        line, = ax.plot(x, y)
        ax.set_ylim(limits)
        ax.set_xlabel('time')
        ax.set_ylabel('RSSI,dBm')

        def update(frame):
            nonlocal y
            rssi = self.getRssi()
            y = np.roll(y,-1)
            y[199] = rssi
            line.set_ydata(y)  
            return line,

        ani = animation.FuncAnimation(fig, update, frames=1, interval=1)
        plt.show()


def main():
   ser = serial.Serial("COM10", 115200,timeout=1)
   sx = SXScope(ser)
   sx.init()
   freq  = 868200000
   sx.setFreq(freq)
   sx.animateRSSI( (-130,-70))



if __name__ == '__main__':
    main()


