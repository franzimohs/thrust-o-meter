import tkinter
from tkinter import filedialog
from tkinter.constants import FLAT
from Analyse import open_analyse_from_main
from reader import open_reader_from_main
from realtimeplot3 import open_realtimeplot3_from_main
import subprocess
# from flappy import main as flappy
from threading import Thread
import serial

raw = serial.Serial('COM6', 115200)
serial_list = [10, 10.0, 10.0]

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
    
def read_serial(raw):
    global serial_list
    while True:
        try :
            line = raw.readline()
            nonl = line.strip()
            decoded = nonl.decode()
            a, b, c = decoded.split()
            serial_list[0] = a
            serial_list[1] = b
            serial_list[2] = c
        except: 
            pass
Thread(target=read_serial, args=(raw,)).start()


class ThrustOMeter:
        
    
        def browsefunc(self):
            self.filename = filedialog.askopenfilename()
            self.pathlabel.config(text=self.filename)
            self.analyse_btn.config(state='normal')
        



        def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("700x200")

        
            
            self.pathlabel = tkinter.Label(window)
            self.pathlabel.grid(row=0, column=0, sticky='e')
            self.flag_game = tkinter.BooleanVar()

            browsebutton = tkinter.Button(window, text="Browse", command=self.browsefunc)
            browsebutton.grid(row=1, padx=121, column=0)
            
            self.analyse_btn = tkinter.Button(window, text="ANALYSE!", bd='5', command=lambda: open_analyse_from_main(self.filename), state='disabled')
            self.analyse_btn.grid(row=0, column=1, sticky='w' )
            reader_btn = tkinter.Button(window, text="READER!", bd='5', command=open_reader_from_main)
            reader_btn.grid(row=1, column=1, sticky='w')
            realtimeplot_btn = tkinter.Button(window, text="REALTIMEPLOT!", bd='5', command=lambda: open_realtimeplot3_from_main(serial_list))
            realtimeplot_btn.grid(row=2, column=1, sticky='w')
            
            game_rdR = tkinter.Radiobutton(window, text= 'Rechts!', var = self.flag_game, value=True)
            game_rdR.grid(row=3, column =2, sticky='w')
            game_rdL = tkinter.Radiobutton(window, text = 'Links!', var = self.flag_game, value = False)
            game_rdL.grid(row=3, column=3, sticky='w')
            # game_btn = tkinter.Button(window, text="SPIEL!", bd='5', command=lambda: flappy(self.flag_game.get()))
            # game_btn.grid(row=3, column=1, sticky='w')
            fortschritt_btn = tkinter.Button(window, text="FORTSCHRITT!", bd='5')
            fortschritt_btn.grid(row=4, column=1, sticky='w')
            center(self.window)
            self.window.mainloop()    
                 



ThrustOMeter(tkinter.Tk(), "Thrust-O-Meter 🦾")
