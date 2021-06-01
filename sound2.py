####CC Franziska Mohs####

import aupyom as ap
import numpy
import threading 
import tkinter as tk
import main as menü

lock = threading.Condition()
sampler = ap.Sampler()
freq = 440.0
sr = 22050
t = 50
s1 = ap.Sound(numpy.sin(2 * numpy.pi * freq * numpy.linspace(0, t, sr * t)), sr)

def center(win):
    
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

class Sound:

    def __init__(self, window, window_title, daten):
        self.window = window
        self.window.title(window_title)
        window.iconbitmap(r'C:\Users\Franziska\Desktop\Bachelorthesis\git\thrust-o-meter\assets\bone.ico')
        
        self.daten = daten
        self.rl_flag=tk.IntVar()
        self.var = 0


        sound_btn = tk.Button(window, text='SOUND!', bd=5, command=self.sound_an)
        sound_btn.grid(row=1, column=1, padx=20, pady=20)
        stop_btn = tk.Button(window, text='STOP!', bd=5, command=self.sound_stop)
        stop_btn.grid(row=1, column=2, padx=20, pady=20)
        rechts_rd= tk.Radiobutton(window, text='Rechts!', var=self.rl_flag, value=0, command=lambda: self.set_var(0))
        rechts_rd.grid(row=2, column=1, padx=20, pady=20)
        links_rd= tk.Radiobutton(window, text='Links!', var=self.rl_flag, value=1, command=lambda: self.set_var(1))
        links_rd.grid(row=2, column= 2, padx=20, pady=20)
        rechts_rd.select()
        center(self.window)
        self.window.mainloop() 

             
    def sound_an(self):
        sampler.play(s1)
        threading.Thread(target=self.update, daemon=True).start()

    def sound_stop(self):
        sampler.remove(s1)
    
    def update(self):
        self.daten.lock.acquire()
       
        while True:
           
            if self.var ==0:
                s1.pitch_shift = int(self.daten.r)
            else:
                s1.pitch_shift = int(self.daten.l)  
        
            self.daten.lock.wait()

    def set_var(self, val):
        self.var = val
        return self.var
        

def main(daten):
    Sound(tk.Tk(), "Sound", daten)
    
      