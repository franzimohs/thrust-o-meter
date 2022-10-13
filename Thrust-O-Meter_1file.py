
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import FLAT
import numpy as np
from matplotlib import pyplot as plt
from threading import Thread, Condition
import serial
import math
from scipy import interpolate
from scipy.interpolate import UnivariateSpline
import threading
from tkinter.font import Font
import datetime
import os
import sys
import time
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *
import aupyom as ap
import threading 



eichwert_r = -62
eichwert_l = -62
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
    


class ThrustOMeter():
        def browsefunc(self):
            self.filename = filedialog.askopenfilename()
            pfad_ordner, pfad_datei =self.filename.split('ausgabe/')
            datei, self.endung=pfad_datei.split('.')
            self.pathlabel.config(text=datei)
            self.analyse_btn.config(state='normal')
            self.ohne_ref_btn.config(state='normal')
            self.peak= self.welcher_peak()
            

        def eichung(self):
           
            
            if self.eichungwechsel:
                self.eichungR_entry.delete(0, 'end')
                self.eichungR_entry.insert(0,str(r))
                self.eichungwechsel = False
                self.eichung_btn.config(text='Eichung 1kg links')
            else:
                self.eichungL_entry.delete(0, 'end')
                self.eichungL_entry.insert(0,str(l))
                self.eichungwechsel = True
                self.eichung_btn.config(text='Eichung 1kg rechts')
            
        
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
            if self.endung == 'tom0':
                peak =360
            if self.endung == 'tom1':
                peak=330
            if self.endung == 'tom2':
                peak=300
            if self.endung== 'tom3':
                peak=270
            return peak


        def __init__(self, window, window_title):
            self.window = window
            self.window.title(window_title)
            self.window.geometry("500x450")
        
            try:
                self.entspeichern()
            except Exception as e:
                print('Kann nicht entspeichern:'+ str(e))
                pass
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
            plateauL_entry.insert(0,'1000')

            self.analyse_btn =tk.Button(window, text="ANALYSE!", bd='5', command=lambda: filecomp(self.filename,self.peak, (self.peak/4), float(plateauL_entry.get())), state='disabled')
            self.analyse_btn.grid(row=0, column=1, sticky='w' , pady=10)
            self.ohne_ref_btn = tk.Button(window, text='FREIE ANALYSE!', bd='5', command=lambda: filecomp(self.filename, peak_entry.get(), plateauH_entry.get()), state='disabled')
            self.ohne_ref_btn.grid(row=1, column=1, sticky='w')
            self.reader_btn =tk.Button(window, text="AUFNAHME!", bd='5', command=lambda: (self.disable_btn(),self.nullung(daten),open_reader_from_main(daten, self.callback)))
            self.reader_btn.grid(row=3, column=1, sticky='w', pady= 5)

            self.realtimeplot_btn =tk.Button(window, text="REALTIMEPLOT!", bd='5', command=lambda:(self.disable_btn(), self.nullung(daten), realtime(daten, self.callback)))
            self.realtimeplot_btn.grid(row=4, column=1, sticky='w',pady=5)
            
            game_rdR =tk.Radiobutton(window, text= 'Rechts!', var = self.flag_game, value=True)
            game_rdR.grid(row=5, column =2, sticky='w')

            game_rdL =tk.Radiobutton(window, text = 'Links!', var = self.flag_game, value = False)
            game_rdL.grid(row=5, column=3, sticky='w')

            self.game_btn =tk.Button(window, text="SPIEL!", bd='5', command=lambda:(self.disable_btn(),self.nullung(daten), flappy(self.flag_game.get(), daten, self.callback)))
            self.game_btn.grid(row=5, column=1, sticky='w', pady=5)

            fortschritt_btn =tk.Button(window, text="FORTSCHRITT!", bd='5', command= Lernfortschritt)
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
            
            self.eichung_btn=tk.Button(window, text='Eichung 1kg rechts', bd='5', command=lambda: self.eichung())
            self.eichung_btn.grid(row=10, column= 1, sticky='w')

            self.speichern_btn = tk.Button(window, text='SAVE!',bd='5', command=self.speichern)
            self.speichern_btn.grid(row=10, column=2, sticky='w', padx=10)
            

            center(self.window)
            self.window.mainloop()    

def menü(Port):
    
    raw = serial.Serial(Port, 115200)

    def main_serial_read(raw):
        global daten, r, l

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
    Thread(target=main_serial_read, args=(raw,), daemon=True).start()
    ThrustOMeter(tk.Tk(), "Thrust-O-Meter")



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

class App(QtGui.QMainWindow):
    def __init__(self, daten, callback, parent=None):
        super(App, self).__init__(parent)
        self.setWindowIcon(QtGui.QIcon('assets/bone.ico'))
        self.daten = daten
        self.callback = callback 

        self.mainbox = QtGui.QWidget()
        self.setWindowTitle('Real-Time-Plot')
       
        self.setCentralWidget(self.mainbox)
        self.mainbox.setLayout(QtGui.QVBoxLayout())
        
        self.canvas = pg.GraphicsLayoutWidget()
        self.mainbox.layout().addWidget(self.canvas)
        
       
        self.target = pg.InfiniteLine(angle = 0, pos = 300, movable = True, bounds=[100,400])
       
        self.zielhöhe = QtGui.QLabel()
        self.label = QtGui.QLabel()
        self.mainbox.layout().addWidget(self.label)
        self.mainbox.layout().addWidget(self.zielhöhe)
        self.radioL = QtGui.QRadioButton()
        self.radioR = QtGui.QRadioButton()
        self.mainbox.layout().addWidget(self.radioL)
        self.mainbox.layout().addWidget(self.radioR)
        self.radioL.setText('Links!')
        self.radioR.setText('Rechts!')
        self.radioR.setChecked(True)
        
        self.otherplot = self.canvas.addPlot()
      
        self.otherplot.setYRange(0,400)
        self.otherplot.addItem(self.target)
        self.otherplot.hideButtons()
        self.otherplot.setLabel('left', text='Kraft', units='N')
        self.otherplot.setLabel('bottom', text='Zeit')
        self.h2 = self.otherplot.plot(pen='y')
        
        self.ydata = np.zeros(100)
       
        self.counter = 0
        self.fps = 0.
        self.lastupdate = time.time()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._update)
        self.timer.start(1000/30)  
    
    def closeEvent(self, event):
        self.callback()
        event.accept()


    def _update(self):
        if self.radioL.isChecked():
            val = self.daten.l
        if self.radioR.isChecked():
            val = self.daten.r
        
        
        self.ydata[:-1] = self.ydata[1:]
        self.ydata[-1] = val*9.81
        
        self.h2.setData(self.ydata)
        self.zielhöhe.setText('Zielwert: '+str(int(self.target.value()))+' N')
        
    
        now = time.time()
        dt = (now-self.lastupdate)
        if dt <= 0:
            dt = 0.000000000001
        fps2 = 1.0 / dt
        self.lastupdate = now
        self.fps = self.fps * 0.9 + fps2 * 0.1
        
        self.counter += 1
        
def realtime(daten, callback):
    app = QtGui.QApplication(sys.argv)
    thisapp = App(daten, callback)
    thisapp.show()
    app.exec_()   
FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 70 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}
flag =True

callback = 0

PLAYERS_LIST = ('assets/sprites/bone_upflap.png','assets/sprites/bone_midflap.png','assets/sprites/bone_downflap.png') 
 

# list of backgrounds
BACKGROUNDS_LIST = (
    'assets/sprites/background-day.png',
    'assets/sprites/background-night.png',
)

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-greenlong.png',
    'assets/sprites/pipe-redlong.png',
)
PIPES_DOWN_LIST = (
    'assets/sprites/pipe-greenlong.png',
    'assets/sprites/pipe-redlong.png',
)

BONE = 'assets/sprites/bone.png'
try:
    xrange
except NameError:
    xrange = range

ICON = pygame.image.load('assets/bone.ico')

def flappy(Flag, Daten, Callback):
    global SCREEN, FPSCLOCK, flag, daten, callback
    daten = Daten
    flag = Flag
    callback = Callback
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Flappy Bone')
    
    pygame.display.set_icon(ICON)
    # numbers sprites for score display
    IMAGES['numbers'] = (
        pygame.image.load('assets/sprites/0.png').convert_alpha(),
        pygame.image.load('assets/sprites/1.png').convert_alpha(),
        pygame.image.load('assets/sprites/2.png').convert_alpha(),
        pygame.image.load('assets/sprites/3.png').convert_alpha(),
        pygame.image.load('assets/sprites/4.png').convert_alpha(),
        pygame.image.load('assets/sprites/5.png').convert_alpha(),
        pygame.image.load('assets/sprites/6.png').convert_alpha(),
        pygame.image.load('assets/sprites/7.png').convert_alpha(),
        pygame.image.load('assets/sprites/8.png').convert_alpha(),
        pygame.image.load('assets/sprites/9.png').convert_alpha()
    )
    
    # game over sprite
    IMAGES['gameover'] = pygame.image.load('assets/sprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    IMAGES['message'] = pygame.image.load('assets/sprites/startbildschirm.png').convert_alpha()
    # base (ground) sprite
    IMAGES['base'] = pygame.image.load('assets/sprites/base.png').convert_alpha()
    
    # sounds
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    SOUNDS['die']    = pygame.mixer.Sound('assets/audio/die' + soundExt)
    SOUNDS['hit']    = pygame.mixer.Sound('assets/audio/hit' + soundExt)
    SOUNDS['point']  = pygame.mixer.Sound('assets/audio/point' + soundExt)
    SOUNDS['swoosh'] = pygame.mixer.Sound('assets/audio/swoosh' + soundExt)
    SOUNDS['wing']   = pygame.mixer.Sound('assets/audio/wing' + soundExt)

    while True:
        # select random background sprites
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

       
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[0]).convert_alpha(), 
            pygame.image.load(PLAYERS_LIST[1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[2]).convert_alpha(),
       )

        # select random pipe sprites
        pipeindex = random.randint(0, len(PIPES_LIST) - 1)
        IMAGES['pipe'] = (
            pygame.transform.flip(
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(PIPES_LIST[pipeindex]).convert_alpha(),
        )
        IMAGES['bone'] = pygame.transform.flip(pygame.image.load(BONE).convert_alpha(), False, True)
        # hismask for pipes
        HITMASKS['pipe'] = (
            getHitmask(IMAGES['pipe'][0]),
            getHitmask(IMAGES['pipe'][1]),
        )
        
        # hitmask for player
        HITMASKS['player'] = (
            getHitmask(IMAGES['player'][0]),
            getHitmask(IMAGES['player'][1]),
            getHitmask(IMAGES['player'][2]),
        )

        
        movementInfo = showWelcomeAnimation()
        crashInfo = mainGame(movementInfo)
        showGameOverScreen(crashInfo)

 

def read_serial(flag, daten, val=-150):


    faktor_maximalkraft = (SCREENHEIGHT-140)/200
    if flag:
        valy = daten.r*9.81
    else:
        valy = daten.l*9.81

    val =-(valy *faktor_maximalkraft)
    
    return val



def showWelcomeAnimation():
    """Shows welcome screen animation of flappy bird"""
    # index of player to blit on screen
    val =-150  
    playerIndex = 0
    playerIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerIndex after every 5th iteration
    loopIter = 0

    playerx = int(SCREENWIDTH * 0.2)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.12)

    basex = 0
    # amount by which base can maximum shift to left
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # player shm for up-down motion on welcome screen
    playerShmVals = {'val': 0, 'dir': 1}

    while True:
        val = read_serial(flag, daten, val)
        if val < -50:
            SOUNDS['wing'].play()
            return {
                'playery': playery + playerShmVals['val'],
                'basex': basex,
                'playerIndexGen': playerIndexGen,
            }

            
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                callback()
                pygame.quit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for mainGame
                SOUNDS['wing'].play()
                return {
                    'playery': playery + playerShmVals['val'],
                    'basex': basex,
                    'playerIndexGen': playerIndexGen,
                }

        # adjust playery, playerIndex, basex
        if (loopIter + 1) % 5 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 4) % baseShift)
        playerShm(playerShmVals)

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['player'][playerIndex],
                    (playerx, playery + playerShmVals['val']))
        SCREEN.blit(IMAGES['message'], (messagex, messagey))
        SCREEN.blit(IMAGES['base'], (basex, BASEY))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def mainGame(movementInfo):
    score = playerIndex = loopIter = 0
    playerIndexGen = movementInfo['playerIndexGen']
    playerx, playery = int(SCREENWIDTH * 0.2), movementInfo['playery']

    basex = movementInfo['basex']
    baseShift = IMAGES['base'].get_width() - IMAGES['background'].get_width()

    # get 2 new pipes to add to upperPipes lowerPipes list
    newPipe1 = getDownPipe()
    newPipe2 = getRandomPipe()
    random_bone = get_random_bone()

    # list of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]
    # list of bones 
    bones = [
        {'x': SCREENWIDTH +200+(SCREENWIDTH*0.75), 'y': random_bone[0]['y']},
        {'x': 2*SCREENWIDTH +200 +(SCREENWIDTH*0.75)+10, 'y': random_bone[0]['y'] }
    ]
    pipeVelX = -4

    
    playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    playerMaxVelY =  10   # max vel along Y, max descend speed
    
    playerAccY    =   1   # players downward accleration
    playerRot     =  0   # player's rotation
   
    playerRotThr  =  20   # rotation threshold
    playerFlapAcc =  -9   # players speed on flapping
    playerFlapped = False # True when player flaps
    
    val = -150
    
    hit_cd = 25
    hit_cd_counter=0
    wechsel_pipe = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                callback()
                pygame.quit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerFlapAcc
                    playerFlapped = True
                    SOUNDS['wing'].play()

        

        # check for crash here
        crashTest = checkCrash({'x': playerx, 'y': playery, 'index': playerIndex},
                               upperPipes, lowerPipes)
        hit=check_hit({'x': playerx, 'y': playery, 'index': playerIndex},
                               bones)
        hit_cd_counter-=1
        if hit and (hit_cd_counter<=0):
            score += 1
            SOUNDS['point'].play()
            hit_cd_counter=hit_cd      
            if score % 10 ==0:
                pipeVelX -=1
        
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperPipes': upperPipes,
                'lowerPipes': lowerPipes,
                'score': score,
                'playerVelY': playerVelY,
                'playerRot': playerRot
            }

        
        # playerIndex basex change
        if (loopIter + 1) % 3 == 0:
            playerIndex = next(playerIndexGen)
        loopIter = (loopIter + 1) % 30
        basex = -((-basex + 100) % baseShift)

        

        # player's movement
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

            # no rotation needed
            playerRot = 0

        # playerHeight = IMAGES['player'][playerIndex].get_height()
        val = read_serial(flag, daten, val)

            # playery 
        playery = SCREENHEIGHT -140 + val
            
        # move pipes to left
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            uPipe['x'] += pipeVelX
            lPipe['x'] += pipeVelX

        for bone in bones:
            bone['x'] +=pipeVelX

        
       

        # add new pipe when first pipe is about to touch left of screen
        if (len(upperPipes) > 0) and (0 < upperPipes[0]['x'] < 5):
            
            if wechsel_pipe:
                newPipe = getRandomPipe()
                
            else:
                newPipe = getDownPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])
            
        if (len(bones)==1) and (0< bones[0]['x']<5):
            newBone = get_random_bone()   
            bones.extend(newBone)
    

            
        
            


        # remove first pipe if its out of the screen
        if len(upperPipes) > 0 and upperPipes[0]['x'] < -IMAGES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
            wechsel_pipe= not wechsel_pipe
        if len(bones) > 0 and bones[0]['x'] < -IMAGES['bone'].get_width():
            bones.pop(0)
        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        
        
        
        for hit_pipe in bones:
            SCREEN.blit(IMAGES['bone'], (hit_pipe['x'], hit_pipe['y']))
        
 
        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
   
        

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        # print score so player overlaps the score
        showScore(score)

        # Player rotation has a threshold
        visibleRot = playerRotThr
        if playerRot <= playerRotThr:
            visibleRot = playerRot
        
        playerSurface = pygame.transform.rotate(IMAGES['player'][playerIndex], visibleRot)
        SCREEN.blit(playerSurface, (playerx, playery))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def showGameOverScreen(crashInfo):
    """crashes the player down ans shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.2
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerAccY = 2
    playerRot = crashInfo['playerRot']
    playerVelRot = 7
    val = -200
    basex = crashInfo['basex']

    upperPipes, lowerPipes = crashInfo['upperPipes'], crashInfo['lowerPipes']

    # play hit and die sounds
    SOUNDS['hit'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['die'].play()
    cd_gameover = 30

    while True:
        val = read_serial(flag, daten, val)
        cd_gameover -= 1
        if (val < -50) and (cd_gameover <= 0):
            return

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                callback()
                pygame.quit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEY - 1:
                    return

        # player y shift
        if playery + playerHeight < BASEY - 1:
            playery += min(playerVelY, BASEY - playery - playerHeight)

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerRot > -90:
                playerRot -= playerVelRot

        # draw sprites
        SCREEN.blit(IMAGES['background'], (0,0))

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))
        
        

        SCREEN.blit(IMAGES['base'], (basex, BASEY))
        showScore(score)

        


        playerSurface = pygame.transform.rotate(IMAGES['player'][1], playerRot)
        SCREEN.blit(playerSurface, (playerx,playery))
        SCREEN.blit(IMAGES['gameover'], (50, 180))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1

def get_random_bone():
    random_bone= -random.randrange(200,280)
    return [
        {'x': SCREENWIDTH +10, 'y': random_bone},
        
    ]


def getRandomPipe():
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapY = random.randrange(100, 280) 
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]

def getDownPipe():
    gapY = random.randrange(279, 280)
    gapY += int(BASEY * 0.2)
    pipeHeight = IMAGES['pipe'][0].get_height()
    pipeX = SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapY + PIPEGAPSIZE}, # lower pipe
    ]


def showScore(score):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0 # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = (SCREENWIDTH - totalWidth) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset, SCREENHEIGHT * 0.1))
        Xoffset += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        pipeW = IMAGES['pipe'][0].get_width()
        pipeH = IMAGES['pipe'][0].get_height()

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(uPipe['x'], uPipe['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(lPipe['x'], lPipe['y'], pipeW, pipeH)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return [True, False]

    return [False, False]

def check_hit(player, bones):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground

    playerRect = pygame.Rect(player['x'], player['y'],
                    player['w'], player['h'])
    pipeW = IMAGES['pipe'][0].get_width()
    pipeH = IMAGES['pipe'][0].get_height()

    
    for hit_pipe in bones:
        uPipeRect = pygame.Rect(hit_pipe['x'], hit_pipe['y'] -80, pipeW, pipeH)

        # player and upper/lower pipe hitmasks
        pHitMask = HITMASKS['player'][pi]
        uHitmask = HITMASKS['pipe'][0]

        # if bird collided with upipe or lpipe
        uCollide = pixelCollision(playerRect, uPipeRect, pHitMask, uHitmask)


        if uCollide:
            return True

    return False
    

def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False

def getHitmask(image):
    """returns a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

lock = threading.Condition()
sampler = ap.Sampler()
freq = 440.0
sr = 22050
t = 50
s1 = ap.Sound(np.sin(2 * np.pi * freq * np.linspace(0, t, sr * t)), sr)

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

    def __init__(self, window, window_title, daten, callback):
        self.window = window
        self.window.title(window_title)
        window.iconbitmap('assets/bone.ico')
        self.callback = callback
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
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
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
    def on_closing(self):
        self.callback()
        self.window.destroy()
              

def sound(daten, callback):
    Sound(tk.Tk(), "Sound", daten, callback)
class Analyse:
	"""
	Contains all methods needed to analyse a given array containing timestamps and values.
	Needs to be initialized new for _every_ array.
	Tip: Don't use the methods from outside. All relevant points are calculated in __init__
	Only ask for already calculated results (ie analyse.peak, analyse.dent etc.)
	"""

	def __init__(self, rawData):

		self.peakIsNegativ = False                         #Falls ihr die Daten irgendwann umdreht, sodass der Peak nicht nach unten ausschlägt: Setzt das hier auf False
		self.sliceCount = 0                               #Hier wird mitgezählt wie oft ich den Datensatz zugeschnitten habe, damit ich in keiner Reckrsivendlosschleife ende
		self.threshold = 10                             #So hoch müssen die Werte mindestsns sein, damit sie relevant sind (kann natürlich bei Bedarf angepasst werden)
		self.varLenght = 20                               #Auf diese Länge wird jeweils die Varianz berechnet. Mein Tipp: Falls das Plateau für eine Mindestdauer gehalten werden muss, würde ich hier ca die Hälfte dieser Zeit eintragen.
		#self.varThresh = 0.3                             #Die tolerierte Varianz berechne ich inzwischen relativ zum Datensatz, aber hier könnte man einen festen Wert einsetzen, wenn man will.
		self.rawData = rawData                            #Das ist das Array, das in den Konstruktor übergeben werden muss. Ich hab das an den bestehenden Datensätzen orientiert.
		self.rawDataBackUp = rawData.copy()               #Das brauche ich für den fall, dass ich die rawData zuschneiden muss, aber danach den orginalIndex wiederfinden will.
		self.cleanData = self.cleanUp()                   #Die Daten werden validiert, gespiegelt, nach oben geschoben und getrimmt.
		self.peak = self.findPeak(self.cleanData)         #Der Peak wird berechnet und als Tupel von Index, Timestamp und Wert angegeben. Der Kraftwert wird allerdings als meine geeichte Version zurückgegeben. Paar Zeilen weiter unten sind die Werte korrigiert.
		self.plateau = self.findPlateau(self.cleanData)   #Der Anfangspunkt des Plateaus wird ebenfalls als Tupel angegeben (index, timestamp, force). Für den Kraftwert gilt das gleich wie für den Peak.
		self.dent = self.findDent(self.cleanData)         #Das hier ist die Delle zwischen Plateau und Peak
		self.slope = self.calculateSlope()                #Das hier ist die Steigung zwischen Delle und Peak
		self.dentDepth = self.calculateDentDepth()        #Differenz zwischen Plateau und Delle
		self.time = self.calculateTimeToPeak()            #Zeit vom tiefsten Punkt der Delle zum Peak
		#Hier nochmal die Koordinaten von Peaks, Plateaus und Dent mit ihren orginal Index- und Forcewerten:
		#Zurückgegebn werden Tripel jeweils mit dem folgenden Aufbau: (Index, Timestamp, Force)
		oldIndexPeak = self.findOldIndex(self.peak[1])
		self.peakCorrect = (oldIndexPeak, self.rawDataBackUp[oldIndexPeak, 0], self.rawDataBackUp[oldIndexPeak, 1])

		oldIndexPlateau = self.findOldIndex(self.plateau[1])
		self.plateauCorrect = (oldIndexPlateau, self.rawDataBackUp[oldIndexPlateau, 0], self.rawDataBackUp[oldIndexPlateau, 1])

		oldIndexDent = self.findOldIndex(self.dent[1])
		self.dentCorrect = (oldIndexDent, self.rawDataBackUp[oldIndexDent, 0], self.rawDataBackUp[oldIndexDent, 1])

		"""
		print(f"Arbeits-Plateau: {self.plateau}")
		print(f"Arbeits-Dent: {self.dent}")
		print(f"Arbeits-Peak: {self.peak}")

		print(f"Orginal-Plateau: {self.plateauCorrect}")
		print(f"Orginal-Peak: {self.peakCorrect}")
		"""


	def calculateDentDepth(self):
		"""
		return: Difference between plateau hight and dent hight.
		"""
		return self.plateau[2] - self.dent[2]

	def calculateSlope(self):
		"""
		Calculates Slope between dent and Peak
		return: slope
		"""

		deltaX = self.peak[1] - self.dent[1]
		deltaY = self.peak[2] - self.dent[2]
		slope = deltaY / deltaX

		return slope
	
	def calculateTimeToPeak(self):
		"""
		Calculates time interval between dent and peak
		return TimeToPeak
		"""
		time = self.peak[1] - self.dent[1]
		return time

	def findDent(self, cleanData):
		"""
		Finds lowest point between plateau and peak -> Dent
		return: (index, timestamp, force value)
		"""

		dentInd = np.argmin(cleanData[self.plateau[0]:self.peak[0],1])
		dentInd = dentInd + self.plateau[0]
		dentTime = cleanData[dentInd,0]
		dentValue = cleanData[dentInd,1]

		return (dentInd, dentTime, dentValue)

	def findPlateau(self, cleanData):
		"""
		Finds last plateau befor peak.
		param: clean Data
		return: Coordinates of plateau (index, timestamp, force value)
		"""

		peakInd = np.argmax(cleanData[:,1])
		varArr = np.zeros((peakInd, 2))
		varArr[:,0] = cleanData[:peakInd,0]

		for i in range(peakInd):
			varArr[i,1] = np.var(cleanData[i:i+self.varLenght,1])
			

		self.varArrayunreduziert = varArr
		# print(varArr[:,1])
		minVar = np.min(varArr[:,1])
			
			

		if minVar < 0.1:
			minVar = 0.01

		varThresh = minVar * 2.5

		varArr = varArr[varArr[:,1] < varThresh]


		#If you want to merge similar points, you would do it here
		#One could also compare hights of the last two plateus to be sure you didn't find the dent, but I've never noticed to be an issue

		plateauTime = varArr[-1,0]
		plateauInd = self.findNewIndex(plateauTime)
		plateauValue = cleanData[plateauInd][1]

		return (plateauInd, plateauTime, plateauValue)

	def findPeak(self, cleanData):
		"""
		Finds highest peak
		param: clean data
		return: Tuple (index, time, value)
		"""
		peakInd = np.argmax(cleanData[:,1])
		peakTime = cleanData[peakInd, 0]
		peakValue = cleanData[peakInd, 1]

		return (peakInd, peakTime, peakValue)

	def findOldIndex(self, timestamp):
		"""
		param: time position i want to find
		return: index of timestamp on _original_ array
		"""
		indexArr = np.where(self.rawDataBackUp[:,0] == timestamp)[0]

		assert indexArr.size == 1, "timestamp not unique Analyse.findOldIndex()"

		return indexArr[0]

	def findNewIndex(self, timestamp):
		"""
		param: time position i want to find
		return: index of timestamp on _cleand_ array
		"""
		indexArr = np.where(self.cleanData[:,0] == timestamp)[0]

		assert indexArr.size == 1, "timestamp not unique Analyse.findNewIndex()"

		return indexArr[0]

	def cleanUp(self):
		"""
		Cleans up data.
		1. Check for faulty data
		2. Invert values, if necessary. Lowest point at 0.
		3. Remove excess data
		return: Remaining interesting stuff after inverting and trimming.
		"""
		#if not self.checkTime():
		# 	raise ValueError("data corrupted (Analyse.cleanUp())")

		cleanData = self.invertValues(self.rawData)
		cleanData = self.trim(cleanData)
		cleanData = self.correctTimstamps(cleanData)

		return cleanData
	
	def correctTimstamps(self, cleanData):
		firstTimestamp = cleanData[0,0]
		lastTimestamp = cleanData[-1,0]
		neededSlots = int((lastTimestamp -firstTimestamp) // 11)

		currentIndex = 1

		correctedArr = np.zeros((neededSlots,2))
		correctedArr[0,0] = cleanData[0,0]
		correctedArr[0,1] = cleanData[0,1]

		for i in range(cleanData.shape[0] -1):
			if currentIndex >= neededSlots:
				break
			if cleanData[i,0] == cleanData[i+1,0] +11:
				correctedArr[currentIndex,0] = cleanData[i+1,0]
				correctedArr[currentIndex,1] = cleanData[i+1,1]
				currentIndex +=1
			elif cleanData[i,0] == cleanData[i+1,0]:
				continue
			else:
				for k in range(int((cleanData[i+1,0] - cleanData[i,0]) // 11 -1)):
					correctedArr[currentIndex,0] = correctedArr[currentIndex -1,0] +11
					correctedArr[currentIndex,1] = correctedArr[currentIndex-1,1]
					currentIndex +=1
				
				correctedArr[currentIndex,0] = cleanData[i+1,0]
				correctedArr[currentIndex,1] = cleanData[i+1,1]
				currentIndex +=1
		
		assert currentIndex == neededSlots, f"currentIndex: {currentIndex}, neededSlots: {neededSlots}"
		return correctedArr
			



	def checkTime(self):
		"""
		Validates data. Timestamps need to be regular to ensure reliable data.
		Reference value (ie 0.3) may need to be evaluated and adjusted, when more datasets are available.
		param: dataarray
		return True If timestamps show low variance
			   False If data contains holes or other irregularities
		"""
		var = np.var(self.rawData[1:,0] - self.rawData[:-1,0])

		if var > 0.3:
			print("data corrupted. I will try again with ends cut off (Analyse.checkTime())")
			if self.sliceCount >= 5:
				self.sliceCount = 0
				return False

			self.rawData = self.rawData[10:-10,:]
			self.sliceCount += 1
			return self.checkTime()

		return True

	def invertValues(self, rawData):
		"""
		Inverts all values so that plateau and peak are the highest positiv values,
		if necessary. Also lowest point is now 0.
		"""

		positivData = rawData

		if self.peakIsNegativ:
			positivData[:,1] = rawData[:,1] * -1


		#positivData[:,1] = positivData[:,1] - np.min(positivData[:,1])

		return positivData


	def trim(self, positivData):
		"""
		Cuts off all excess data (start and end)
		param: data where peak is positiv
		Return: Array only containing rise of plateau to end of peak.
		"""
		indBeginning = 0
		indEnding = len(positivData)

		for i in range(len(positivData)):
			if positivData[i,1] > self.threshold:
				indBeginning = i
				break
		
		for j in range(len(positivData)):
			index = len(positivData) -j -1
			if positivData[index,1] > self.threshold:
				indEnding = index +2
				break
		
		return positivData[indBeginning:indEnding]

def open_analyse_from_main(loadData=None, **kwargs):
	"""
	Two ways to call:
	1. Call with file name. open_analyse_from_main('fileName')
	2. Call to create a reference and analyse it. open_analyse_from_main(peakHeight='forceValue')
	"""
	if loadData is None:
		rawData = createReference(**kwargs)
	else:
		rawData = np.loadtxt(loadData)

	analyse = Analyse(rawData)

	fig = plt.figure()
	ax1 = fig.add_subplot(131)
	ax1.set_title("Arbeitsdaten")
	ax2 = fig.add_subplot(133)
	ax2.set_title("Varianzverlauf")
	ax3 = fig.add_subplot(132)
	ax3.set_title("Orginaldaten")

	ax1.plot(analyse.cleanData[:,0], analyse.cleanData[:,1])
	ax1.plot(analyse.peak[1], analyse.peak[2], "rx")
	ax1.plot(analyse.dent[1], analyse.dent[2], "rx")
	ax1.plot([analyse.plateau[1], analyse.plateau[1]+analyse.varLenght], [analyse.plateau[2]]*2, "r-")
	ax1.plot([analyse.dent[1]]*2, [analyse.dent[2], analyse.plateau[2]], "r-")

	textX1 = analyse.cleanData[0,0]
	textY1 = analyse.plateau[2] + ((analyse.peak[2] - analyse.plateau[2]) /2)
	ax1.text(textX1, textY1, f"Plateau: {analyse.plateau[2]} \nDelle: {analyse.dent[2]} \nSpannungsabfall: {analyse.dentDepth} \nSpitze: {analyse.peak[2]} \nSteigung: {analyse.slope} \nZeit: {analyse.time}")

	ax2.plot(analyse.varArrayunreduziert[:,0], analyse.varArrayunreduziert[:,1], "r")

	ax3.plot(analyse.rawDataBackUp[:,0], analyse.rawDataBackUp[:,1])
	ax3.plot(analyse.peakCorrect[1], analyse.peakCorrect[2], "rx")
	ax3.plot(analyse.dentCorrect[1], analyse.dentCorrect[2], "rx")
	ax3.plot([analyse.plateauCorrect[1], analyse.plateauCorrect[1]+analyse.varLenght], [analyse.plateauCorrect[2]]*2, "r-")
	ax3.plot([analyse.dentCorrect[1]]*2, [analyse.dentCorrect[2], analyse.plateauCorrect[2]], "r-")

	textX2 = np.min(analyse.rawDataBackUp[:,0])
	textY2 = analyse.plateauCorrect[2] + ((analyse.peakCorrect[2] - analyse.plateauCorrect[2]) /2)
	ax3.text(textX2, textY2, f"Plateau: {analyse.plateauCorrect[2]} \nDelle: {analyse.dentCorrect[2]} \nSpannungsabfall: {analyse.dentDepth} \nSpitze: {analyse.peakCorrect[2]} \nSteigung: {analyse.slope}\nZeit: {analyse.time}")
	
	plt.show() 


class FileComparison:
    """
    Compares to given files for similarities and differences.
    """

    def __init__(self, rawData1, rawData2):
        """
        Initiate with both data arrays.
        First is reference.
        Second is test subjects input.
        """

        self.analyse1 = Analyse(rawData1)
        self.analyse2 = Analyse(rawData2)

        self.difPeak = self.comparePeaks()
        self.difPlateau = self.comparePlateaus()
        self.difTime = self.compareTime()

    def comparePeaks(self):

        peak1 = self.analyse1.peakCorrect[2]
        peak2 = self.analyse2.peakCorrect[2]

        return peak2 - peak1

    def comparePlateaus(self):

        plateau1 = self.analyse1.plateauCorrect[2]
        plateau2 = self.analyse2.plateauCorrect[2]

        return plateau2 - plateau1

    def compareTime(self):

        time1 = self.analyse1.time
        time2 = self.analyse2.time

        return time2 - time1

    def getMeanTimeStep(self):
        timeArray1 = self.analyse1.cleanData[:,0]
        timeArray2 = self.analyse2.cleanData[:, 0]
        minLen = min(timeArray1.shape[0], timeArray2.shape[0])
        timesteps1 = (timeArray1[1:minLen]-timeArray1[:minLen-1])
        timesteps2 = (timeArray2[1:minLen]-timeArray2[:minLen-1])
        meanTimeStep = np.mean(np.abs(timesteps1))
        timestepDiffSum = meanTimeStep -np.mean(np.abs(timesteps2))
        assert timestepDiffSum < 0.05, f"Timesteps differ! Mean of Difference: {timestepDiffSum}"
        return meanTimeStep

    def getMergedArrays(self):
        # start time
        starttime1 = self.analyse1.cleanData[0, 0]
        starttime2 = self.analyse2.cleanData[0, 0]

        #time to peak
        timeToPeak1 = self.analyse1.peak[1]
        timeToPeak2 = self.analyse2.peak[1] 

        #time from peak
        timeFromPeak1 = self.analyse1.cleanData[-1, 0]-timeToPeak1
        timeFromPeak2 = self.analyse2.cleanData[-1, 0] - timeToPeak2

        # merged Times
        mergedTimeToPeak = min(timeToPeak1-starttime1, timeToPeak2-starttime2)
        mergedTimeFromPeak = min(timeFromPeak1,timeFromPeak2)
        # boolean indices 
        ind1 = np.logical_and(self.analyse1.cleanData[:, 0] >= timeToPeak1-mergedTimeToPeak,
                              self.analyse1.cleanData[:, 0] <= timeToPeak1 + mergedTimeFromPeak)
        ind2 = np.logical_and(self.analyse2.cleanData[:, 0] >= timeToPeak2-mergedTimeToPeak,
                              self.analyse2.cleanData[:, 0] <= timeToPeak2 + mergedTimeFromPeak)

        timestep = self.getMeanTimeStep()
        #In some situations one array has 1 more timestep in the desired interval than the other.
        if not np.sum(ind1)== np.sum(ind2):
            if np.sum(ind1) > np.sum(ind2):
                ind1[np.arange(0,ind1.shape[0])[ind1][-1]] = False
            else:
                ind2[np.arange(0, ind2.shape[0])[ind2][-1]] = False
        mergedArray = np.zeros((3, np.sum(ind1)))
        mergedArray[0,:] = np.arange(0,mergedArray.shape[1])*timestep
        mergedArray[2, :np.sum(ind2)] = self.analyse2.cleanData[ind2, 1]

        mergedArray[1, :np.sum(ind1)] = self.analyse1.cleanData[ind1, 1]
        return mergedArray
def filecomp(loaddata, peakHight, plateauHight, plateauLength):
    ref = createReference(peakHight, plateauHight, plateauLength)
    testdata = np.loadtxt(loaddata)
    
    filecomp = FileComparison(ref,testdata)
    mergedArray = filecomp.getMergedArrays()
    
    
    
    plt.plot(mergedArray[0],mergedArray[1], 'b-', label = "Reference")
    plt.plot(mergedArray[0], mergedArray[2], 'r-', label="Datafile")
    plt.figtext(0.15, 0.55 ,f"Absolute Werte: \nPlateau: {filecomp.analyse2.plateau[2]}N \nSpannungsabfall: {filecomp.analyse2.dentDepth}N \nMaximalkraft: {filecomp.analyse2.peak[2]}N \nZeit: {filecomp.analyse2.time}ms", bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.figtext(0.15, 0.35 ,f"Differenz zur Referenz: \nPlateau:{round(filecomp.difPlateau,2)}N \nMaximalkraft: {round(filecomp.difPeak,2)}N \nZeit: {round(filecomp.difTime,2)}ms", bbox={"facecolor":"orange", "alpha":0.5, "pad":5})
    plt.legend()
    plt.xlabel('Zeit[ms]')
    plt.ylabel('Kraft[N]')
    fig = plt.get_current_fig_manager()
    fig.window.wm_iconbitmap('assets/bone.ico')
    plt.gcf().canvas.set_window_title('Analyse') 

    
    plt.show()

def fortschritt(endung, peak):
  peak_list = []
  vorspannung_list =[]
  inzisur_list =[]
  time_list =[]
  
  for (x, y, filenames) in os.walk('ausgabe'):
    
    for file in sorted(filenames):
      name = file.split('.')
      if name[-1] != endung:
        continue 
        
      rawData = np.loadtxt('ausgabe/'+file)
      
      try:
        analyseData=Analyse(rawData)
      except Exception as e:
        print('Fehler:'+str(e))
        pass
      peak_list.append([name[0], (analyseData.peak[2]-peak)])
      vorspannung_list.append([name[0], (analyseData.plateau[2]-(peak/4))])
      inzisur_list.append([name[0], analyseData.dentDepth])
      time_list.append([name[0], (analyseData.time-150)])
  return peak_list, vorspannung_list, inzisur_list, time_list
  


def plot():
  peak_list, vorspannung_list, inzisur_list, time_list = merge()
  fig = plt.figure(num='Lernfortschritt')
  fig_manager = plt.get_current_fig_manager()
  fig_manager.window.wm_iconbitmap('assets/bone.ico')
  
  p1=fig.add_subplot(221)
  p2=fig.add_subplot(222)
  p3=fig.add_subplot(223)
  p4=fig.add_subplot(224)

  p1.plot([item[1] for item in peak_list], label = "Peakverlauf")
  p1.set_title('Peak')   
  p1.set_ylabel('Kraft[N]') 

  p2.plot([item[1] for item in vorspannung_list], label ='Vorspannungsverlauf')
  p2.set_title('Vorspannung')
  p2.set_ylabel('Kraft[N]')

  p3.plot([item[1] for item in inzisur_list], label ='Inzisurverlauf')
  p3.set_title('Inzisurtiefe')
  p3.set_ylabel('Kraft[N]')

  p4.plot([item[1] for item in time_list], label='Zeitverlauf')
  p4.set_title('Impulsdauer')
  p4.set_ylabel('Zeit[ms]')
  fig.set_size_inches((9,6.5))
  
def merge():
  peak_list0=[]
  peak_list1=[]
  peak_list2=[]
  peak_list3=[]
  vorspannung_list0=[]
  vorspannung_list1=[]
  vorspannung_list2=[]
  vorspannung_list3=[]
  inzisur_list0=[]
  inzisur_list1=[]
  inzisur_list2=[]
  inzisur_list3=[]
  time_list0=[]
  time_list1=[]
  time_list2=[]
  time_list3=[]
  try:
    peak_list0, vorspannung_list0, inzisur_list0, time_list0 = fortschritt('tom0', 360)
  except:
      pass
  try:
    peak_list1, vorspannung_list1, inzisur_list1, time_list1 = fortschritt('tom1', 330)
  except:
    pass
  try:
    peak_list2, vorspannung_list2, inzisur_list2, time_list2 = fortschritt('tom2', 300)
  except:
    pass
  try:
    peak_list3, vorspannung_list3, inzisur_list3, time_list3 = fortschritt('tom3', 270)
  except:
    pass
  
  peak_fehler_list =sorted(peak_list0 + peak_list1 + peak_list2 + peak_list3)
  vorspannung_fehler_list = sorted(vorspannung_list0 + vorspannung_list1 + vorspannung_list2 + vorspannung_list3)
  inzisur_fehler_list = sorted(inzisur_list0 + inzisur_list1 + inzisur_list2 + inzisur_list3)
  time_fehler_list = sorted(time_list0 + time_list1 + time_list2 + time_list3)
  return peak_fehler_list, vorspannung_fehler_list, inzisur_fehler_list, time_fehler_list

def Lernfortschritt():
  plot()
  plt.show()


def createReference(peakHeight, plateauHeight = None, plateauLenght = None):
    """
    Creates interpolated funktion and its calculated values according to given values.

    peakHight needs to be given. plateauHight and plateauLenght (in ms) are optional.
    Default value for plateauHeight is 0.25*peakHight.
    Default value for plateaulenght is araund 4000ms.

    return: np array (x, 2)
    arr[:,0] timestamps in ms (11ms steps)
    arr[:,1] calculated force values of reference curve
    """

    if plateauHeight is None:
        plateauHeight = math.floor(peakHeight / 4)
    
    if plateauLenght is None:
        plateauLenght = 4004
    
    plaetauIndexLenght = math.floor(plateauLenght / 11)
    step = math.floor(plaetauIndexLenght / 4)

    start = (0,0)
    start2 = (10,0)
    takeoff = (25,0)
    plateau1 = (100, plateauHeight)
    plateau11 = (plateau1[0] + 0.25*step, plateauHeight)
    plateau12 = (plateau1[0] + 0.5*step, plateauHeight)
    plateau13 = (plateau1[0] + 0.75*step, plateauHeight)
    plateau2 = (plateau1[0] + step, plateauHeight)
    plateau3 = (plateau2[0] + step, plateauHeight)
    plateau4 = (plateau3[0] + step, plateauHeight)
    plateau41 = (plateau4[0] + 0.25*step, plateauHeight)
    plateau42 = (plateau4[0] + 0.5*step, plateauHeight)
    plateau43 = (plateau4[0] + 0.75*step, plateauHeight)
    plateau44 = (plateau4[0] + 0.875*step, plateauHeight)
    plateau5 = (plateau1[0] + plaetauIndexLenght, plateauHeight)
    plateau6 = (plateau5[0]+ 5, plateauHeight + 15)
    peak = (plateau5[0] + 14, peakHeight)
    coolDown = (peak[0] + 20, 0)
    end1 = (coolDown[0] + 5, 0)
    end2 = (end1[0] +5, 0)
    end3 = (end2[0] +5, 0)
    end4 = (end3[0] +5, 0)

    arrayLenght = 100 + plaetauIndexLenght + 14 + 20 + 5 + 5 + 5 + 5+5
    timeLenght = arrayLenght*11

    pointsX = np.array([start[0], start2[0], takeoff[0], plateau1[0], plateau11[0], plateau12[0], plateau13[0], plateau2[0], plateau3[0], plateau4[0],plateau41[0],plateau42[0],plateau43[0], plateau44[0],plateau5[0],plateau6[0], peak[0], coolDown[0], end1[0], end2[0], end3[0], end4[0]])
    pointsY = np.array([start[1], start2[1], takeoff[1], plateau1[1], plateau11[1], plateau12[1], plateau13[1], plateau2[1], plateau3[1], plateau4[1], plateau41[1],plateau42[1],plateau43[1],plateau44[1], plateau5[1], plateau6[1], peak[1], coolDown[1], end1[1], end2[1], end3[1], end4[1]])

    #plt.plot(pointsX,pointsY, 'rx')
    interpolation = interpolate.splrep(pointsX, pointsY)

    newX = np.arange(arrayLenght)
    
    newY = interpolate.splev(newX, interpolation, der=0)

    timeX = np.arange(0, timeLenght, 11)

    finalArr = np.zeros((arrayLenght, 2))
    finalArr[:,0] = timeX
    finalArr[:,1] = newY

    return finalArr
class Reader(tk.Frame):
	def __init__(self, daten,callback,  master=None):
		tk.Frame.__init__(self, master)
		if hasattr(master, 'title'): master.title('Aufnahme')
		self.grid()
		self.daten = daten
		self.callback = callback
		self.font = Font(family='monospace')
		self.flag_update = tk.IntVar(master, 0)
		self.ref = tk.IntVar(master, 0)
		outer_frame = tk.Frame(self)
		f = tk.Frame(outer_frame)
		master.iconbitmap('assets/bone.ico')

		tk.Label(f, font=self.font, text='file name').grid(row = 0, column = 0)
		self.fname = tk.Entry(f, font=self.font)
		self.fname.grid(row = 0, column = 1)
		self.timeName = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%z')
		self.fname.insert(0, self.timeName)
		tk.Label(f, font=self.font, text='Maximalkraft:').grid(row = 1, column=2)
		tk.Radiobutton(f, text='Rechts!', var=self.flag_update, value=0).grid(row = 0, column = 4)
		tk.Radiobutton(f, text='Links!', var=self.flag_update, value=1).grid(row = 0, column = 5)
		tk.Radiobutton(f, text='360N', var=self.ref, value=0).grid(row=1, column=3)
		tk.Radiobutton(f, text='340N', var=self.ref, value=1).grid(row=1, column=4)
		tk.Radiobutton(f, text='300N', var=self.ref, value=2).grid(row=1, column=5)
		tk.Radiobutton(f, text='270N', var=self.ref, value=3).grid(row=1, column=6)
		tk.Radiobutton(f, text='ohne Referenz', var=self.ref, value=4).grid(row=1, column=7)
		self.ref.set(0)
		self.flag_update.set(0)
		
		self.samplecount = tk.Label(f, font=self.font, text='samples')
		self.samplecount.grid(row = 0, column = 6)

		self.btn_start = tk.Button(f, font=self.font, text='start', command=self.start)
		self.btn_start.grid(row = 0, column = 7)
		self.btn_stop = tk.Button(f, font=self.font, text='stop&save', command=self.save, state='disabled')
		self.btn_stop.grid(row = 0, column = 8)

		f.grid()

		self.frame_fakeserial = tk.Frame(outer_frame)
		self.frame_fakeserial.grid(row = 0, column = 9)

		outer_frame.grid()

		self.data = []
		self.recording = False
	
	def name_update(self):
		self.timeName = datetime.datetime.now().strftime('%Y%m%d_%H%M%S%z')
		self.fname.delete(0, 'end')
		self.fname.insert(0, self.timeName)

	def start(self):
		self.recording = True
		self.btn_start.config(state='disabled')
		self.btn_stop.config(state='normal')
		threading.Thread(target=self.reader, daemon=True).start()

	def save(self):
		self.recording = False
		self.btn_start.config(state='normal')
		self.btn_stop.config(state='disabled')
		np.savetxt('ausgabe/'+self.fname.get()+'.tom'+str(self.ref.get()), self.data, fmt='%d')
		self.data.clear()
		self.samplecount['text'] = 'saved'
		self.name_update()
		

	def reader(self):
		
		with self.daten.lock:
			while self.recording:
				if self.flag_update.get()==0:
					
					val = self.daten.r
				else:
					val = self.daten.l

				
				self.data.append((self.daten.t, (val*9.81)))#g= 9,81 F= m*g
				
				self.samplecount['text'] = '%d samples' % len(self.data)
				self.daten.lock.wait()
	
	def on_closing(self):
		self.callback()
		self.master.destroy()
		

def reader(daten, callback):
	root = tk.Tk()
	app = Reader(daten,callback,  master=root)
	root.protocol("WM_DELETE_WINDOW", app.on_closing)
	app.mainloop()

def open_reader_from_main(daten, callback):
	try:
		reader(daten,callback)
	except KeyboardInterrupt:
		pass

if __name__ == '__main__':
    portabfrage(tk.Tk(), "Portabfrage")

