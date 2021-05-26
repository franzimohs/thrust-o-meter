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
s1 = ap.Sound(numpy.sin(2 * numpy.pi * freq * numpy.linspace(0, t, sr * t)), sr)

def read_serial(raw):
    while True:
        try :
            line = raw.readline()
            nonl = line.strip()
            decoded = nonl.decode()
            t, val1, val2 = decoded.split()
            s1.pitch_shift = int(val1)/64 #1kg=64 g=9,81 Bodenhöhe=200
        except: 
            pass

sampler.play(s1)
Thread(target=read_serial, args=(raw,)).start()

while s1.playing:
    time.sleep(0.1)
