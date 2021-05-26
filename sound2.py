import aupyom as ap
import time
import numpy


sampler = ap.Sampler()
freq = 440.0
sr = 22050
t = 15

s1 = ap.Sound(numpy.sin(2 * numpy.pi * freq * numpy.linspace(0, t, sr * t)), sr)
sampler.play(s1)
while s1.playing:
    
    s1.pitch_shift = 1
    time.sleep(0.1)
    s1.pitch_shift = 2
    time.sleep(0.1)
    s1.pitch_shift = 4
    time.sleep(0.1)
    s1.pitch_shift =10
    time.sleep(0.1)
    s1.pitch_shift =20
    time.sleep(1)
    


    
