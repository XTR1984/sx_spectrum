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

    def getSpectrumRaw(self, start_freq, step, size, showtime=True):
        st = time.time()
        start_freq = int (start_freq*1000000)
        step = int (step * 1000000)
        #spm = bytearray(size)
        req = "Sweep:"+str(start_freq)+":"+ str(step)+":" + str(size)+"\n"
        self.ser.write(req.encode("ASCII"))
        self.ser.flush()
        spm = self.ser.read(size)
        delta = time.time()-st
        if showtime:
            print("sweeptime=", delta)
        return spm
    
    def getSpectrum(self, start_freq, step, size, showtime=True):
        spm = self.getSpectrumRaw(self, start_freq, step, size, showtime)
        spm2 = [-x/2 for x in spm]
        return spm2

    def getSpectrumNumPy(self,start_freq,step,size):
        import numpy as np
        data = self.getSpectrumRaw(start_freq, step, size)
        y = np.frombuffer(data,dtype=np.uint8)
        y = np.float32(y)
        y = - y/2
        return y



def drawSpectrum(sx,start_freq,step,steps):
    y = sx.getSpectrumNumPy(start_freq,step,steps)
    x = np.linspace(start_freq, start_freq+y.size*step, y.size)
    plt.plot(x, y)
    plt.show()

def animate_plt(sx, start_freq,step,steps,ylim=(-130.0, -90.0),cmap="jet"):
    fig, axes = plt.subplots(2,1)
    waterfall_data = np.zeros((100,steps))
    waterfall_data[:]=-100
    y = sx.getSpectrumNumPy(start_freq,step,steps)
    x = np.linspace(start_freq, start_freq+y.size*step, y.size)
    pic1, = axes[0].plot(x, y,"r-", animated=True)
    vmin,vmax = ylim
    norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
    pic2 = axes[1].pcolormesh(waterfall_data,norm=norm,cmap=cmap)
    pics = [pic1,pic2]
    axes[0].set_xlabel('frequency, MHz')
    axes[0].set_ylabel('RSSI,dBm')
    axes[0].set_title("sx spectrum")
    axes[0].set_ylim(ylim)
    axes[0].margins(0)
    axes[1].set_xticks([])

    def subanimate(i):
        nonlocal waterfall_data
        y = sx.getSpectrumNumPy(start_freq,step,steps)
        pic1.set_data(x, y)
        waterfall_data = np.roll(waterfall_data,-1,axis=0)
        waterfall_data[99,:] = y
        pics[1]= axes[1].pcolormesh(waterfall_data,norm=norm,cmap=cmap)
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
   #start_freq, step, steps  = 432, 0.01, 500
   #start_freq, step, steps  = 300, 0.5, 300
   start_freq, step, steps  = 750, 0.5, 500
   animate_plt(sx,start_freq,step,steps,cmap="hot")
   #drawSpectrum(sx,start_freq,step,steps)

if __name__ == '__main__':
    main()


