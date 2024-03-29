### nach dem Programm FlaPyBird (MIT-License) von Sourabh Verma ###
###cc Franziska Mohs###


from itertools import cycle
import random
import sys
import pygame
from pygame.locals import *


FPS = 30
SCREENWIDTH  = 288
SCREENHEIGHT = 512
PIPEGAPSIZE  = 70 # gap between upper and lower part of pipe
BASEY        = SCREENHEIGHT * 0.79
# image, sound and hitmask  dicts
IMAGES, SOUNDS, HITMASKS = {}, {}, {}
flag =True
daten = [10, 10.0, 10.0] 
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

def main(Flag, Daten, Callback):
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
        valy = daten.l*9.81
    else:
        valy = daten.r*9.81

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

