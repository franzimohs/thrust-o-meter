import tkinter
from tkinter import filedialog
from tkinter.constants import FLAT
from Analyse import open_analyse_from_main
from reader import open_reader_from_main
from realtimeplot3 import open_realtimeplot3_from_main
import subprocess
from flappy import main as flappy

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




class ThrustOMeter:
        def browsefunc(self):
            self.filename = filedialog.askopenfilename()
            self.pathlabel.config(text=self.filename)

        def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("700x200")

            
            
            self.pathlabel = tkinter.Label(window)
            self.pathlabel.grid(row=0, column=0, sticky='e')

            browsebutton = tkinter.Button(window, text="Browse", command=self.browsefunc)
            browsebutton.grid(row=1, padx=121, column=0)

            analyse_btn = tkinter.Button(window, text="ANALYSE!", bd='5', command=lambda: open_analyse_from_main(self.filename))
            analyse_btn.grid(row=0, column=1, sticky='w' )
            reader_btn = tkinter.Button(window, text="READER!", bd='5', command=open_reader_from_main)
            reader_btn.grid(row=1, column=1, sticky='w')
            realtimeplot_btn = tkinter.Button(window, text="REALTIMEPLOT!", bd='5', command=open_realtimeplot3_from_main)
            realtimeplot_btn.grid(row=2, column=1, sticky='w')
            game_btn = tkinter.Button(window, text="SPIEL!", bd='5', command=flappy)
            game_btn.grid(row=3, column=1, sticky='w')
            fortschritt_btn = tkinter.Button(window, text="FORTSCHRITT!", bd='5')
            fortschritt_btn.grid(row=4, column=1, sticky='w')
            center(self.window)
            self.window.mainloop()           



ThrustOMeter(tkinter.Tk(), "Thrust-O-Meter 🦾")