import aupyom as ap
import time
import numpy
from threading import Thread
import serial
raw = serial.Serial('COM6', 115200)

sampler = ap.Sampler()
freq = 440.0
sr = 22050
t = 15
pitch = 0
def read_serial(raw):
    global pitch
    while True:
        try :
            line = raw.readline()
            nonl = line.strip()
            decoded = nonl.decode()
            t, val1, val2 = decoded.split()
            pitch = int(val1)/64 #1kg=64 g=9,81 Bodenhöhe=200
        except: 
            pass
Thread(target=read_serial, args=(raw,)).start()
s1 = ap.Sound(numpy.sin(2 * numpy.pi * freq * numpy.linspace(0, t, sr * t)), sr)
sampler.play(s1)
while s1.playing:
    
    s1.pitch_shift = pitch
    time.sleep(0.1)
   
    


    
