import aupyom as ap
import numpy
import threading 
# import serial
import tkinter as tk

sampler = ap.Sampler()
freq = 440.0
sr = 22050
t = 50
s1 = ap.Sound(numpy.sin(2 * numpy.pi * freq * numpy.linspace(0, t, sr * t)), sr)
def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
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

    def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("300x100")
            
            sound_btn = tk.Button(window, text='SOUND!', bd=5, command=self.sound_an)
            sound_btn.grid(row=1, column=1, sticky='w')
            stop_btn = tk.Button(window, text='STOP!', bd=5, command=self.sound_stop)
            stop_btn.grid(row=1, column=2, sticky='w')
            center(self.window)
            self.window.mainloop() 
             
    def sound_an(self):
        sampler.play(s1)

    def sound_stop(self):
        sampler.remove(s1)
        
        

def main(serial_list):
    
    lock = threading.Condition()
    def update(serial_list):
       
        lock.acquire()

        while True:
            lock.wait()
            z, val1, val2 = serial_list
            s1.pitch_shift = int(val1) 
    threading.Thread(target=update,args=(serial_list,), daemon=True).start()
    Sound(tk.Tk(), "Sound")

    

if __name__ == '__main__':
    main([10,10.0,10.0])



