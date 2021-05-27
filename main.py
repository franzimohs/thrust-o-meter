import tkinter as tk
from tkinter import filedialog
from tkinter.constants import FLAT
# from Analyse import open_analyse_from_main
from reader import open_reader_from_main
from realtimeplot3 import open_realtimeplot3_from_main
import subprocess
from flappy import main as flappy
from threading import Thread, Condition
import serial
from FileComparison import main as filecomp
from sound2 import main as sound
eichwert_r = 0.00
eichwert_l = 0.00
nullwert_r = 0.00
nullwert_l = 0.00

class Daten():
        def __init__(self):
                self.lock = Condition()
                self.t = 10
                self.r = 10.0
                self.l = 10.0

daten = Daten()

def center(win):
    """
    centers atk window
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
    
# 

class ThrustOMeter():
        def browsefunc(self):
            self.filename = filedialog.askopenfilename()
            self.pathlabel.config(text=self.filename)
            self.analyse_btn.config(state='normal')

        def eichung(self, daten):
            global eichwert_r, eichwert_l
            if self.eichungwechsel:
                eichwert_r = daten.r
                self.eichungR_lable.config(text=f"Rechts: {str(eichwert_r)}")
                self.eichungwechsel = False
                self.eichung_btn.config(text='Eichung 1kg Links')
            else:
                eichwert_l = daten.l
                self.eichungL_lable.config()
                self.eichungL_lable.config(text=f"Links: {str(eichwert_l)}")
                self.eichungwechsel = True
                self.eichung_btn.config(text='Eichung 1kg Rechts')

        def nullung(self, daten):
            global nullwert_r, nullwert_l
            nullwert_r = daten.r
            nullwert_l = daten.l

        def speichern(self):
            with open('Eichwert', 'w') as speicher:
                speicher.write(f'{eichwert_r}\n{eichwert_l}\n')

        def entspeichern(self):
            global eichwert_r, eichwert_l
            with open('Eichwert', 'r') as speicher:
                eichwert_r = float(speicher.readline().strip())
                eichwert_l = float(speicher.readline().strip())

        def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("700x300")
            self.entspeichern()
        
            
            self.pathlabel = tk.Label(window)
            self.pathlabel.grid(row=0, column=0, sticky='e')
            self.flag_game = tk.BooleanVar()
            self.eichungwechsel = True
            browsebutton = tk.Button(window, text="Browse", command=self.browsefunc)
            browsebutton.grid(row=1, padx=121, column=0)
            tk.Label(window, text='Maximalkraft: ').grid(row=0, column=2, sticky='w')
            tk.Label(window, text='Vorspannungskraft: ').grid(row=1, column=2, sticky='w')
            tk.Label(window, text='Vorspannungslänge: ').grid(row=2, column=2, sticky='w')

            plateauH_entry =tk.Entry(window, width=6)
            plateauH_entry.grid(row=1, column=3, sticky='w')
            peak_entry =tk.Entry(window, width=6)
            peak_entry.grid(row=0, column= 3, sticky='w')
            plateauL_entry =tk.Entry(window, width=6)
            plateauL_entry.grid(row=2, column=3, sticky='w')
            self.analyse_btn =tk.Button(window, text="ANALYSE!", bd='5', command=lambda: filecomp(self.filename,float(peak_entry.get()), float(plateauH_entry.get()), float(plateauL_entry.get())), state='disabled')
            self.analyse_btn.grid(row=0, column=1, sticky='w' )
            reader_btn =tk.Button(window, text="READER!", bd='5', command=lambda: open_reader_from_main(daten))
            reader_btn.grid(row=3, column=1, sticky='w')
            realtimeplot_btn =tk.Button(window, text="REALTIMEPLOT!", bd='5', command=lambda: open_realtimeplot3_from_main(daten))
            realtimeplot_btn.grid(row=4, column=1, sticky='w')
            
            game_rdR =tk.Radiobutton(window, text= 'Rechts!', var = self.flag_game, value=False)
            game_rdR.grid(row=5, column =2, sticky='w')
            game_rdL =tk.Radiobutton(window, text = 'Links!', var = self.flag_game, value = True)
            game_rdL.grid(row=5, column=3, sticky='w')
            game_btn =tk.Button(window, text="SPIEL!", bd='5', command=lambda: flappy(self.flag_game.get(), daten))
            game_btn.grid(row=5, column=1, sticky='w')
            fortschritt_btn =tk.Button(window, text="FORTSCHRITT!", bd='5')
            fortschritt_btn.grid(row=6, column=1, sticky='w')
            
            self.eichungR_lable=tk.Label(window, text='Rechts')
            self.eichungR_lable.grid(row=7, column=0, sticky='w')
            self.eichungL_lable=tk.Label(window, text='Links')
            self.eichungL_lable.grid(row=8, column=0, sticky='w')
            
            self.eichung_btn=tk.Button(window, text='Eichung 1kg Rechts', bd='5', command=lambda: self.eichung(daten))
            self.eichung_btn.grid(row=7, column= 1, sticky='w')
            speichern_btn = tk.Button(window, text='speichern!',bd='5', command=self.speichern)
            speichern_btn.grid(row=7, column=2, sticky='w')
            sound_btn= tk.Button(window, text='SOUND!', bd='5', command=lambda: sound(daten) )
            sound_btn.grid(row=8, column=1, sticky='w')

            center(self.window)
            self.window.mainloop()    

def main(Port):
    
    raw = serial.Serial(Port, 115200)

    def read_serial(raw):
        global daten

        while True:
            try:
                line = raw.readline()
                nonl = line.strip()
                decoded = nonl.decode()

                parts = decoded.split()
                if (3 != len(parts)):
                        continue
                t, r, l = parts

                daten.t = int(t)
                daten.r = (float(r) - nullwert_r) / (eichwert_r - nullwert_r)
                daten.l = (float(l) - nullwert_l) / (eichwert_l - nullwert_l)
                with daten.lock:
                        daten.lock.notify_all()
            except Exception as e:
                print('reader failed:', e)
    Thread(target=read_serial, args=(raw,), daemon=True).start()
    ThrustOMeter(tk.Tk(), "Thrust-O-Meter")

if __name__ == '__main__':
    main('COM6')
