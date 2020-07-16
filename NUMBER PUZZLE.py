
import pygame, sys, random
from pygame.constants import*


from pygame.locals import *



BOARDWIDTH = 5
BOARDHEIGHT = 4
TILESIZE = 65
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

Y=(128,0,128)
RASPBERRY =(255,0,125)
VIOLET = (125,0,255)
OCEAN = (0,125,255)
MAGENTA = (255,0,255)
RED = (255,0,0)
BLUE= (0,0,25)
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BRIGHTBLUE = ( 0, 50, 255)
DARKTURQUOISE = ( 3, 54, 73)
GREEN = ( 0, 204, 0)

MESSAGEBG=MAGENTA
BGCOLOR = VIOLET
TILECOLOR = Y

BUTTONTEXT =GREEN
TEXTCOLOR = WHITE
BORDERCOLOR =MAGENTA
BASICFONTSIZE = 20
TITLEFONTSIZE = 25

BUTTONCOLOR = DARKTURQUOISE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = BLUE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) /2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT -1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def main():
   global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT,NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT,GAME_QUIT

   pygame.init()
   FPSCLOCK = pygame.time.Clock()
   DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
   pygame.display.set_caption('Number Slide')
   BASICFONT = pygame.font.SysFont('Copper Black', BASICFONTSIZE)


   NEW_SURF, NEW_RECT = makeText('RESHUFFLE', BUTTONTEXT, BUTTONCOLOR,WINDOWWIDTH - 490, WINDOWHEIGHT - 90)
   SOLVE_SURF, SOLVE_RECT = makeText('SOLVE FOR YOU', BUTTONTEXT, BUTTONCOLOR,WINDOWWIDTH - 375, WINDOWHEIGHT - 90)
   RESET_SURF, RESET_RECT = makeText('QUIT GAME', BUTTONTEXT, BUTTONCOLOR, WINDOWWIDTH - 230, WINDOWHEIGHT - 90)

   mainBoard, solutionSeq = generateNewPuzzle(80)
   SOLVEDBOARD = getStartingBoard()

   allMoves = []

   while True:
      slideTo = None
      message = ''
      if mainBoard == SOLVEDBOARD:
         message = 'PUZZLE SOLVED!'


      drawBoard(mainBoard, message)
      checkForQuit()

      for event in pygame.event.get():
         if event.type == MOUSEBUTTONUP:
            spotx, spoty = getSpotClicked(mainBoard, event.pos[0],event.pos[1])

            if (spotx, spoty) == (None, None):


               if NEW_RECT.collidepoint(event.pos):
                    mainBoard, solutionSeq = generateNewPuzzle(80)
                    allMoves = []

               elif SOLVE_RECT.collidepoint(event.pos):
                    resetAnimation(mainBoard, solutionSeq + allMoves)
                    allMoves = []

               elif RESET_RECT.collidepoint(event.pos):
                  resetAnimation(mainBoard, sys.exit())

                  allMoves = []



            else:
                blankx, blanky = getBlankPosition(mainBoard)
                if spotx == blankx + 1 and spoty == blanky:
                   slideTo = LEFT

                elif spotx == blankx - 1 and spoty == blanky:
                   slideTo = RIGHT

                elif spotx == blankx and spoty == blanky + 1:
                   slideTo = UP

                elif spotx == blankx and spoty == blanky - 1:
                   slideTo = DOWN


         elif event.type == KEYUP:
              if event.key in (K_LEFT, K_a) and isValidMove(mainBoard,LEFT):
                 slideTo = LEFT

              elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
                   slideTo = RIGHT
              elif event.key in (K_UP, K_w) and isValidMove(mainBoard,UP):
                   slideTo = UP
              elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard,DOWN):
                   slideTo = DOWN



      if slideTo:
        slideAnimation(mainBoard, slideTo,'',1)
        makeMove(mainBoard, slideTo)
        allMoves.append(slideTo)
      pygame.display.update()
      FPSCLOCK.tick(FPS)



def terminate():
     pygame.quit()
     sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def getStartingBoard():
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH-1][BOARDHEIGHT-1] = None
    return board

def getBlankPosition(board):
     for x in range(BOARDWIDTH):
         for y in range(BOARDHEIGHT):
             if board[x][y] == None:
                 return (x, y)

def makeMove(board, move):
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] =board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] =board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx +1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx -1][blanky], board[blankx][blanky]

def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):
    validMoves = [UP, DOWN, LEFT, RIGHT]
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)

    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)

    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)

    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)

    return random.choice(validMoves)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def getSpotClicked(board, x, y):
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)

def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy,TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE/ 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

def makeText(text, color, bgcolor, top, left):
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)

    return (textSurf, textRect)

def drawBoard(board, message):
    DISPLAYSURF.fill(BGCOLOR)

    titleSurf = BASICFONT.render('DIG PUZZLE', 25, WHITE)
    titleRect = titleSurf.get_rect()
    titleRect.topleft = (WINDOWWIDTH - 360, 70)
    DISPLAYSURF.blit(titleSurf, titleRect)

    instSurf = BASICFONT.render('How To Play', 25, BLACK)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 530,100)
    DISPLAYSURF.blit(instSurf, instRect)

    oneSurf = BASICFONT.render('1.To Start a new Game ', 25, WHITE)
    oneRect = oneSurf.get_rect()
    oneRect.topright = (WINDOWWIDTH - 490,115)
    DISPLAYSURF.blit(oneSurf, oneRect)

    instSurf = BASICFONT.render('Reshuffle.', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 561,130)
    DISPLAYSURF.blit(instSurf, instRect)

    instSurf = BASICFONT.render('2.Use Left, Right, Up&', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 500,150)
    DISPLAYSURF.blit(instSurf, instRect)

    instSurf = BASICFONT.render('Down Arrows or  ', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 517,165)
    DISPLAYSURF.blit(instSurf, instRect)

    instSurf = BASICFONT.render('Mouse(Click on a Tile ', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 488,180)
    DISPLAYSURF.blit(instSurf, instRect)

    instSurf = BASICFONT.render('adjacent to Blank', 25,WHITE )
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 519,195)
    DISPLAYSURF.blit(instSurf, instRect)

    instSurf = BASICFONT.render('Tile) for a Move.', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 528,210)
    DISPLAYSURF.blit(instSurf, instRect)


    instSurf = BASICFONT.render('3.Arrange numbers ', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 512,230)
    DISPLAYSURF.blit(instSurf, instRect)


    instSurf = BASICFONT.render('from 1=>19 (top to', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 518,245)
    DISPLAYSURF.blit(instSurf, instRect)


    instSurf = BASICFONT.render('bottom)', 25, WHITE)
    instRect = instSurf.get_rect()
    instRect.topright = (WINDOWWIDTH - 580,260)
    DISPLAYSURF.blit(instSurf, instRect)


    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, MESSAGEBG, 260,410)
        DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width +11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)



def slideAnimation(board, direction, message, animationSpeed):
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()

    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
    if direction == UP:
        drawTile(movex, movey, board[movex][movey], 0, -i)

    if direction == DOWN:
        drawTile(movex, movey, board[movex][movey], 0, i)

    if direction == LEFT:
        drawTile(movex, movey, board[movex][movey], -i, 0)

    if direction == RIGHT:
        drawTile(movex, movey, board[movex][movey], i, 0)

    pygame.display.update()
    FPSCLOCK.tick(FPS)

def generateNewPuzzle(numSlides):
    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    lastMove = None
    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'SHUFFLING NUMBERS...',int(TILESIZE / 4))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move

    return (board, sequence)

def resetAnimation(board, allMoves):
    revAllMoves = allMoves[:]
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, 'SOLVING FOR YOU', int(TILESIZE / 3))
        makeMove(board, oppositeMove)

if __name__ == '__main__':
 main()

