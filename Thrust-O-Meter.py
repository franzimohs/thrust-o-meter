####CC Franziska Mohs####



import tkinter as tk
from main import main as menü
from tkinter import filedialog




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

class portabfrage:

    def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("300x100")
            window.iconbitmap('assets/bone.ico')
            port_lable= tk.Label(window, text='Serieller Port: ')
            port_lable.grid(row=1, column= 0, sticky='w')
            erklärung_lable = tk.Label(window, text='Suche den COM-Port\nim Gerätemanager.')
            erklärung_lable.grid(row=2, column=1, sticky='s')
            self.port_entry = tk.Entry(window,width=10)
            
            self.port_entry.grid(row=1, column= 1, sticky='w')
            self.port_entry.insert(0,'COM6')
            port_btn = tk.Button(window, text='Port speichern', bd=5, command=self.PortButton)
            port_btn.grid(row=1, column=2, sticky='w')
            self.Port='COM6'
            center(self.window)
            self.window.mainloop() 
             
    def PortButton(self):
        self.Port= self.port_entry.get()
        self.window.destroy()
        
        menü(self.Port)

def main():
    portabfrage(tk.Tk(), "Portabfrage")

if __name__ == '__main__':
    main()

