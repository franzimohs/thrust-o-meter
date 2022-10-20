####CC Franziska Mohs####



import tkinter as tk
from main import main as menü




def center(win):
    """
    centers a tkinter self.master
    :param win: the main self.master or Toplevel self.master to center
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

    def __init__(self, master, window_title):
            self.master = tk.Tk() if master is None else master
            self.master.title(window_title)
            self.master.geometry("300x100")
            self.master.iconbitmap('assets/bone.ico')
            port_lable= tk.Label(self.master, text='Serieller Port: ')
            port_lable.grid(row=1, column= 0, sticky='w')
            erklärung_lable = tk.Label(self.master, text='Suche den COM-Port\nim Gerätemanager.')
            erklärung_lable.grid(row=2, column=1, sticky='s')
            self.port_entry = tk.Entry(self.master,width=10)
            
            self.port_entry.grid(row=1, column= 1, sticky='w')
            self.port_entry.insert(0,'COM6')
            port_btn = tk.Button(self.master, text='Port speichern', bd=5, command=self.PortButton)
            port_btn.grid(row=1, column=2, sticky='w')
            self.Port='COM6'
            center(self.master)
            self.master.mainloop() 


    def PortButton(self):
        self.Port= self.port_entry.get()
        self.master.destroy()
        
        menü(self.Port)

class portwissenschaft():
    def __init__(self, master, Überschrift):
        import sys, serial

        success = False
        
        if sys.platform.startswith("win"):
            for i in range(1, 10):
                port = f"COM{i}"
                try:
                    serial.Serial(port)
                    success = True
                    break
                except:
                    pass
        elif sys.platform.startswith("linux"):
            import glob
            for port in glob.glob("/dev/ttyUSB*") + glob.glob("/dev/ttyACM*"):
                try:
                    serial.Serial(port)
                    success = True
                    break
                except:
                    pass

        if not success:
            portabfrage(master, Überschrift)

        menü(port)

def main():
    portwissenschaft(master=None, Überschrift="Portabfrage")

if __name__ == '__main__':
    main()

