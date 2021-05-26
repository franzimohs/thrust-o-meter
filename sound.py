import pyaudio
import numpy as np
import serial
from threading import Thread
import time
 
p = pyaudio.PyAudio()
f = 300.0
volume = 0.5     # range [0.0, 1.0]
fs = 44100 #44100       # sampling rate, Hz, must be integer
duration = 0.01  # in seconds, may be float
recording = True #440.0        # sine frequency, Hz, may be float
raw = serial.Serial('COM6', 115200)


# generate samples, note conversion to float32 array



# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=fs,
                output=True)
def read_serial(raw):
    global f
    while True:
        try :
            line = raw.readline()
            nonl = line.strip()
            decoded = nonl.decode()
            t, val1, val2 = decoded.split()
            f = -(float(val1)/64*9.81)+200 #1kg=64 g=9,81 Bodenhöhe=200
        except: 
            pass
Thread(target=read_serial, args=(raw,)).start()

# play. May repeat with different volume values (if done interactively) 
while True:
    samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32).tobytes() #'letzter'
    stream.write(samples)
    time.sleep(0.1)
# stream.stop_stream()
# stream.close()

# p.terminate()