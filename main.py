####CC Franziska Mohs####

import tkinter as tk
from tkinter import filedialog
from tkinter.constants import FLAT
from reader import open_reader_from_main
from realtimeplot import open_realtimeplot3_from_main
from flappy import main as flappy
from threading import Thread, Condition
import serial
from FileComparison import main as filecomp
from sound import main as sound
from Lernfortschritt import main as fortschritt

eichwert_r = -62
eichwert_l = -62
eichwert_basis = 5
nullwert_r = 0.00
nullwert_l = 0.00
r = 0.00
l = 0.00

class Daten():
        def __init__(self):
                self.lock = Condition()
                self.t = 10
                self.r = 10.0
                self.l = 10.0

daten = Daten()

    


class ThrustOMeter():
        def browsefunc(self):
            self.filename = filedialog.askopenfilename(initialdir=self.pfad, title='Zu analysierende Datei wählen')
            pfad_ordner, pfad_datei =self.filename.split('ausgabe')
            datei, self.endung=pfad_datei.split('.')
            self.pathlabel.config(text=datei)
            self.analyse_btn.config(state='normal')
            self.ohne_ref_btn.config(state='normal')
            self.peak, self.vorspannung= self.welcher_peak()

        def eichung(self):
            if self.eichungwechsel:
                self.eichungR_entry.delete(0, 'end')
                self.eichungR_entry.insert(0,str(r))
                self.eichungwechsel = False
                self.eichung_btn.config(text='Eichung %skg links'%eichwert_basis)
            else:
                self.eichungL_entry.delete(0, 'end')
                self.eichungL_entry.insert(0,str(l))
                self.eichungwechsel = True
                self.eichung_btn.config(text='Eichung %skg links'%eichwert_basis)
            
        def disable_btn(self):
            self.game_btn.config(state='disabled')
            self.sound_btn.config(state='disabled')
            self.reader_btn.config(state='disabled')
            self.eichung_btn.config(state='disabled')
            self.realtimeplot_btn.config(state='disabled')
       
        def enable_btn(self):
            self.game_btn.config(state='normal')
            self.sound_btn.config(state='normal')
            self.reader_btn.config(state='normal')
            self.eichung_btn.config(state='normal')
            self.realtimeplot_btn.config(state='normal')

        def nullung(self, daten):
            global nullwert_r, nullwert_l
            nullwert_r = daten.r
            nullwert_l = daten.l

        def speichern(self):
            global eichwert_r, eichwert_l
            eichwert_l =float(self.eichungL_entry.get())
            eichwert_r =float(self.eichungR_entry.get())
            with open('Eichwert', 'w') as speicher:
                speicher.write(f'{eichwert_r}\n{eichwert_l}\n')
            self.eichungR_entry.delete(0,'end')
            self.eichungL_entry.delete(0,'end')
            self.eichungR_entry.insert(0, 'gespeichert!')
            self.eichungL_entry.insert(0,'gespeichert!')

        def entspeichern(self):
            global eichwert_r, eichwert_l
            with open('Eichwert', 'r') as speicher:
                eichwert_r = float(speicher.readline().strip())
                eichwert_l = float(speicher.readline().strip())
        
        def welcher_peak(self):
            if self.endung == 'tom00':
                peak =550
                vorspannung = 220
            if self.endung == 'tom10':
                peak=450
                vorspannung = 188
            if self.endung == 'tom20':
                peak=350
                vorspannung = 140
            if self.endung== 'tom30':
                peak=250
                vorspannung = 100
            if self.endung == 'tom01':
                peak = 550
                vorspannung = 138
            if self.endung == 'tom11':
                peak = 450
                vorspannung = 113
            if self.endung == 'tom21':
                peak = 350
                vorspannung = 88
            if self.endung == 'tom31':
                peak = 250
                vorspannung = 63
            return peak, vorspannung
        
        
        def Pfadspeichern(self):
            self.pfad = filedialog.askdirectory(title='Ausgabeordner wählen')
            with open('Ausgabepfad', 'w') as speicher:
                speicher.write(f'{self.pfad}')
                speicher.close()

        def Pfadentspeichern(self):
            with open('Ausgabepfad', 'r') as speicher:
                self.pfad = speicher.readline()
    
        def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("500x450")

            try:
                self.Pfadentspeichern()
            except Exception as e:
                print('Kann nicht Pfad entspeichern:'+ str(e))
                self.Pfadspeichern()

            
            try:
                self.entspeichern()
            except Exception as e:
                print('Kann nicht Eichwerte entspeichern:'+ str(e))

            self.callback = self.enable_btn
            window.iconbitmap('assets/bone.ico')
            self.pathlabel = tk.Label(window)
            self.pathlabel.grid(row=0, column=0)
            self.flag_game = tk.BooleanVar()
            self.eichungwechsel = True
            browsebutton = tk.Button(window, text="Browse",bd='5', command=self.browsefunc)
            browsebutton.grid(row=1, padx=40, column=0)
            
            tk.Label(window, text='Maximalkraft [N]:\n (nur FREIE ANALYSE)').grid(row=0, column=2, sticky='w')
            tk.Label(window, text='Vorspannungskraft [N]:\n (nur FREIE ANALYSE)').grid(row=1, column=2, sticky='w')
            tk.Label(window, text='Vorspannungslänge [ms]: ').grid(row=2, column=2, sticky='w')

            plateauH_entry =tk.Entry(window, width=6)
            plateauH_entry.grid(row=1, column=3, sticky='w')
            plateauH_entry.insert(0,'80')
            
            peak_entry =tk.Entry(window, width=6)
            peak_entry.grid(row=0, column= 3, sticky='w')
            peak_entry.insert(0,'360')

            plateauL_entry =tk.Entry(window, width=6)
            plateauL_entry.grid(row=2, column=3, sticky='w')
            plateauL_entry.insert(0,'4000')

            self.analyse_btn =tk.Button(window, text="ANALYSE!", bd='5', command=lambda: filecomp(self.filename,self.peak, self.vorspannung, float(plateauL_entry.get())), state='disabled')
            self.analyse_btn.grid(row=0, column=1, sticky='w' , pady=10)

            self.ohne_ref_btn = tk.Button(window, text='FREIE ANALYSE!', bd='5', command=lambda: filecomp(self.filename, float(peak_entry.get()), float(plateauH_entry.get()), float(plateauL_entry.get())), state='disabled')
            self.ohne_ref_btn.grid(row=1, column=1, sticky='w')

            self.reader_btn =tk.Button(window, text="AUFNAHME!", bd='5', command=lambda: (self.disable_btn(),self.nullung(daten),open_reader_from_main(daten, self.callback, self.pfad)))
            self.reader_btn.grid(row=3, column=1, sticky='w', pady= 5)

            self.realtimeplot_btn =tk.Button(window, text="REALTIMEPLOT!", bd='5', command=lambda:(self.disable_btn(), self.nullung(daten), open_realtimeplot3_from_main(daten, self.callback)))
            self.realtimeplot_btn.grid(row=4, column=1, sticky='w',pady=5)
            
            game_rdR =tk.Radiobutton(window, text= 'Rechts!', var = self.flag_game, value=False)
            game_rdR.grid(row=5, column =2, sticky='w')

            game_rdL =tk.Radiobutton(window, text = 'Links!', var = self.flag_game, value = True)
            game_rdL.grid(row=5, column=3, sticky='w')

            self.game_btn =tk.Button(window, text="SPIEL!", bd='5', command=lambda:(self.disable_btn(),self.nullung(daten), flappy(self.flag_game.get(), daten, self.callback)))
            self.game_btn.grid(row=5, column=1, sticky='w', pady=5)

            fortschritt_btn =tk.Button(window, text="FORTSCHRITT!", bd='5', command=fortschritt)
            fortschritt_btn.grid(row=6, column=1, sticky='w', pady=5)

            self.sound_btn= tk.Button(window, text='SOUND!', bd='5', command=lambda: (self.disable_btn(), self.nullung(daten),sound(daten, self.callback)))
            self.sound_btn.grid(row=7, column=1, sticky='w', pady=5)

            self.eichungR_lable=tk.Label(window, text='Rechts:')
            self.eichungR_lable.grid(row=8, column=0)
            self.eichungL_lable=tk.Label(window, text='Links:')
            self.eichungL_lable.grid(row=10, column=0)
            self.eichungR_entry= tk.Entry(window, width=15)
            self.eichungR_entry.grid(row=9, column=0)
            self.eichungL_entry=tk.Entry(window, width=15)
            self.eichungL_entry.grid(row=11, column=0)
            
            
            self.eichung_btn=tk.Button(window, text='Eichung %skg rechts'%eichwert_basis, bd='5', command=lambda: self.eichung())
            self.eichung_btn.grid(row=10, column= 1, sticky='w')

            self.speichern_btn = tk.Button(window, text='SAVE!',bd='5', command=self.speichern)
            self.speichern_btn.grid(row=10, column=2, sticky='w', padx=10)
            
            self.ordner_btn=tk.Button(window, text='Ordner wechseln', bd='5',command= self.Pfadspeichern)
            self.ordner_btn.grid(row=12, column=0)
            
            self.window.mainloop()    

def main(Port):
    
    raw = serial.Serial(Port, 115200)

    def read_serial(raw):
        global daten, r, l

        while True:
            try:
                line = raw.readline()
                nonl = line.strip()
                decoded = nonl.decode()

                parts = decoded.split()
                
                if (3 == len(parts)):
                    t, r, l = parts

                    daten.t = int(t)
                    daten.r = (float(r) - nullwert_r) / (eichwert_r/eichwert_basis - nullwert_r)
                    daten.l = (float(l) - nullwert_l) / (eichwert_l/eichwert_basis - nullwert_l)                
                elif (2 == len(parts)):
                    t, r = parts

                    daten.t = int(t)
                    daten.r = (float(r) - nullwert_r) / (eichwert_r/eichwert_basis - nullwert_r)
                    daten.l = 0
                   
                else:
                        continue
               
                with daten.lock:
                        daten.lock.notify_all()
            except Exception as e:
                print('reader failed:', e)
    Thread(target=read_serial, args=(raw,), daemon=True).start()
    ThrustOMeter(tk.Tk(), "Thrust-O-Meter")

if __name__ == '__main__':
    main('COM4')
