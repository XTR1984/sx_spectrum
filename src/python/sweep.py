import time
import math
import serial
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import animation  


class SXSpectrum(): #sx127x spectrum getter
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

    def getSpectrum(self, startf, step, size, showtime=True):
        st = time.time()
        startf = int (startf*1000000)
        step = int (step * 1000000)
        #spm = bytearray(size)
        req = "Sweep:"+str(startf)+":"+ str(step)+":" + str(size)+"\n"
        self.ser.write(req.encode("ASCII"))
        self.ser.flush()
        spm = self.ser.read(size)
        delta = time.time()-st
        if showtime:
            print("sweeptime=", delta)
        return spm

    def getSpectrumNumPy(self,startf,step,size):
        import numpy as np
        data = self.getSpectrum(startf, step, size)
        y = np.frombuffer(data,dtype=np.uint8)
        y = np.float32(y)
        y = - y/2
        return y



def drawSpectrum(sx,startf,step,sz):
    y = sx.getSpectrumNumPy(startf,step,sz)
    x = np.linspace(startf, startf+y.size*step, y.size)
    plt.plot(x, y)
    plt.show()

def animate_plt(sx, startf,step,sz,waterfall=True):
    fig, axes = plt.subplots(2,1)
    waterfall_data = np.zeros((100,sz))
    waterfall_data[:]=-100
    y = sx.getSpectrumNumPy(startf,step,sz)
    x = np.linspace(startf, startf+y.size*step, y.size)
    pic1, = axes[0].plot(x, y,"r-", animated=True)
    vmin,vmax = -120,-90
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    pic2 = axes[1].pcolormesh(waterfall_data,norm=norm)
    pics = [pic1,pic2]
    axes[0].set_xlabel('frequency, MHz')
    axes[0].set_ylabel('RSSI,dBm')
    axes[0].set_title("sx spectrum")
    axes[0].set_ylim([-130.0, -90.0])
    axes[0].margins(0)
    axes[1].set_xticks([])

    def subanimate(i):
        nonlocal waterfall_data
        y = sx.getSpectrumNumPy(startf,step,sz)
        pic1.set_data(x, y)
        waterfall_data = np.roll(waterfall_data,-1,axis=0)
        waterfall_data[99,:sz] = y
        pics[1]= axes[1].pcolormesh(waterfall_data,norm=norm)
        return pics

    anim = animation.FuncAnimation(fig, subanimate, 
                               frames=720, interval=0, blit=True
                               ) 
    fig.tight_layout()    
    plt.show()



def main():
   ser = serial.Serial("COM10", 115200,timeout=5)
   sx = SXSpectrum(ser)
   sx.init()
   startf = 750
   step = 0.5
   sz = 500
   animate_plt(sx,startf,step,sz)

if __name__ == '__main__':
    main()


