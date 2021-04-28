import tkinter
from Analyse import open_analyse_from_main
from reader import open_reader_from_main
from realtimeplot3 import open_realtimeplot3_from_main

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
        def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("700x350")
            
            analyse_btn = tkinter.Button(window, text="ANALYSE!", bd='5', command=open_analyse_from_main)
            analyse_btn.pack()
            reader_btn = tkinter.Button(window, text="READER!", bd='5', command=open_reader_from_main)
            reader_btn.pack()
            realtimeplot_btn = tkinter.Button(window, text="REALTIMEPLOT!", bd='5', command=open_realtimeplot3_from_main)
            realtimeplot_btn.pack()

            center(self.window)
            self.window.mainloop()           



ThrustOMeter(tkinter.Tk(), "Thrust-O-Meter 🦾")