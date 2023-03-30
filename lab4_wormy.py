# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys, time
from pygame.locals import *

FPS = 15
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)

#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
BLUE      = (137, 207, 240) #Requirement No. 1: color for the 2nd worm
DARKBLUE  = (  0,   0, 255) #Requirement No. 1: color for the 2nd worm
YELLOW    = (255, 255,   0) #Requirement No. 2: color for the new object
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head
score= 0


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, score

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        runGame()
        showGameOverScreen()


def runGame():
    global direction1, score
    start = time.time()
    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    # Requirement No. 1: setting start coordinates for 2nd worm
    startx1 = random.randint(5, CELLWIDTH - 6)
    starty1 = random.randint(5, CELLHEIGHT - 6)

    wormCoords = [{'x': startx,     'y': starty},
                  {'x': startx - 1, 'y': starty},
                  {'x': startx - 2, 'y': starty}]
    direction = RIGHT

    # Requirement No. 1: setting coordinates and direction for 2nd worm
    wormCoords1 = [{'x': startx1, 'y': starty1},
                  {'x': startx1 - 1, 'y': starty1},
                  {'x': startx1 - 2, 'y': starty1}]
    direction1 = LEFT

    # Start the apple in a random place.
    apple = getRandomLocation()
    # Requirement No. 2: start two new object in random places
    yellowApple = getRandomLocation()
    blueApple = getRandomLocation()
    extraPoints = 0 #new variable for adding extra points to the score

    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit itself or the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            return # game over
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # Requirement No. 1: random moving direction

        if direction1 == LEFT:
            direction1 = random.choice([UP, DOWN, LEFT])
        elif direction1 == RIGHT:
            direction1 = random.choice([UP, DOWN, RIGHT])
        elif direction1 == UP:
            direction1 = random.choice([LEFT, RIGHT, UP])
        elif direction1 == DOWN:
            direction1 = random.choice([RIGHT, DOWN, LEFT])

        if direction1 == UP:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] - 1}
        elif direction1 == DOWN:
            newHead1 = {'x': wormCoords1[HEAD]['x'], 'y': wormCoords1[HEAD]['y'] + 1}
        elif direction1 == LEFT:
            newHead1 = {'x': wormCoords1[HEAD]['x'] - 1, 'y': wormCoords1[HEAD]['y']}
        elif direction1 == RIGHT:
            newHead1 = {'x': wormCoords1[HEAD]['x'] + 1, 'y': wormCoords1[HEAD]['y']}

        #Requirement No. 1: if second worm touches the first worm add plus one segment to the second worm
        if ((time.time() - start) > 20):
            if wormCoords1[HEAD]['x'] == wormCoords[HEAD]['x'] and wormCoords1[HEAD]['y'] == wormCoords[HEAD]['y']:
                pass
            else:
                del wormCoords1[-1]

        # check if worm has eaten an apply
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            apple = getRandomLocation() # set a new apple somewhere
        elif wormCoords1[HEAD]['x'] == wormCoords[HEAD]['x'] and wormCoords1[HEAD]['y'] == wormCoords[HEAD]['y'] and ((time.time() - start) > 20):
            pass
        else:
            del wormCoords[-1] # remove worm's tail segment

        # Requirement No. 1: check if worm has eaten extra object
        if wormCoords[HEAD]['x'] == blueApple['x'] and wormCoords[HEAD]['y'] == blueApple['y']:
            blueApple = {'x': -1, 'y': -1}
            extraPoints += 3
        if wormCoords[HEAD]['x'] == yellowApple['x'] and wormCoords[HEAD]['y'] == yellowApple['y']:
            yellowApple = {'x': -1, 'y': -1}
            extraPoints += 3

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        score = (len(wormCoords) - 3) + extraPoints # Requirement No. 2: new formula for score
        drawScore(score)
        # Requirement No. 1: draw the second worm
        if ((time.time() - start) > 20):
            wormCoords1.insert(0, newHead1)
            drawWorm1(wormCoords1)
        # Requirement No. 2: appear for 5 seconds every 5 seconds
        if ((time.time() - start) % 10 > 5):
            drawBlueApple(blueApple)
        # Requirement No. 2: appear once for 7 seconds
        if ((time.time() - start) < 7):
            drawYellowApple(yellowApple)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WINDOWWIDTH - 200, WINDOWHEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)


def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Wormy!', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame


def terminate():
    pygame.quit()
    sys.exit()


def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}


def showGameOverScreen():
    global score
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)

    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()

    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)

    # Requirement No. 2: add score to the gameOver screen
    scoreFont = pygame.font.Font('freesansbold.ttf', 16)
    scoreSurf = scoreFont.render('Score: ' + str(score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.midtop = (WINDOWWIDTH / 2, 450)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    # Requirement No. 3: add start and quit buttons
    buttonFont = pygame.font.Font('freesansbold.ttf', 30)
    startSurf = buttonFont.render('Start from the beggining', True, GREEN, DARKGRAY)
    quitSurf = buttonFont.render('Quit', True, GREEN, DARKGRAY)
    startRect = startSurf.get_rect()
    quitRect = quitSurf.get_rect()
    startRect.midtop = (WINDOWWIDTH / 2, 350)
    quitRect.midtop = (WINDOWWIDTH / 2, 400)
    DISPLAYSURF.blit(startSurf, startRect)
    DISPLAYSURF.blit(quitSurf, quitRect)

    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        # Requirement No. 3: start and quit buttons func
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if startRect.collidepoint(pygame.mouse.get_pos()):
                    return
                if quitRect.collidepoint(pygame.mouse.get_pos()):
                    terminate()

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)

#Requirement No. 1: function for drawing the second worm
def drawWorm1(wormCoords1):
    for coord in wormCoords1:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKBLUE, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, BLUE, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

#REQUIREMENT No. 2: draw two new objects
def drawYellowApple(coord):
    color1 = YELLOW
    color2 = GREEN
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    for i in range(3):
        color1, color2 = color2, color1
        appleYellowRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color1, appleYellowRect)
        pygame.display.update()
        #FPSCLOCK.tick(FPS)

def drawBlueApple(coord):
    color1 = BLUE
    color2 = DARKBLUE
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    for i in range(3):
        color1, color2 = color2, color1
        appleBlueRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, color1, appleBlueRect)
        pygame.display.update()
        # FPSCLOCK.tick(FPS)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))


if __name__ == '__main__':
    main()