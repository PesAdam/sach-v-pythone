# main file, ma na starosti user input a zobrazovanie aktualneho stavu hry
import pygame as p
import ChessEngine

p.init()
WIDTH = HEIGHT = 512            # velkost okna
DIMENSION = 8                   # velkost hracieho pola
SQ_SIZE = HEIGHT // DIMENSION   # velkost jednej pozicie
MAX_FPS = 15                    # max fps pre animacie
IMAGES = {}                     # pre ukladanie obrazkov


#nacitavanie obrazkov, toto bude v maine
def load_images():
    pieces = ['wp', 'wN', 'wB', 'wR', 'wQ', 'wK', 'bp', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for piece in pieces:
        print(piece)
        IMAGES[piece] = p.transform.scale(p.image.load("img/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #transform sluzi nato aby obrazok vzdy vyzeral dobre
    # mame pristup k obrazkom, vieme sa k nim dostat cez 'IMAGES['wp']'


#main kusok kodu, bude sa zaoberat user inputom a updatovanim hry
def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState() #vytvorime instanciu hry, gs = game state
    validMoves = gs.getValidMoves()
    moveMade = False            #flag var, ked sa vykona pohyb
    load_images()               #nacitame obrzky, robime to iba raz!!!  
    running = True              #bezime? bezime!
    sqSelected =  ()            #toto je tuple, kde bude ukladat poziciu kliknutia, od zaiatku je pozicia prazdna,
                                # (tuple(row,col))
    playerClicks = []           # tu bude ukladat kliknutia, ktore bude hrac zadavat 
    gameOver = False

    while running:                  #ak bezi tak sa pozre ci nahodou neni niekde beziaci pygame event
        for e in p.event.get():     #ak je niekde event, tak ho vypne
            if e.type == p.QUIT:    #ak je to quit event, tak sa ukonci
                running = False
            #myska
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos()  #ziskaj x,y poziciu mysi
                    row = location[1] // SQ_SIZE     #zistime ktory riadok
                    col = location[0] // SQ_SIZE     #zistime ktory stlpec
                    if sqSelected == (row, col):    #ak je kliknutie na rovnaku poziciu, tak sa odstrani zoznam
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)         #zapiseme do tuple
                        playerClicks.append(sqSelected) #zapiseme do zoznamu
                    if len(playerClicks) == 2:          #po druhom kliku
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board) #bere si prvu poziciu, poslednu a board
                        print(move.getChessNotation())
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                        sqSelected = ()     #reset uzivateloveho kliku
                        playerClicks = []
            
            #klavesnica
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #krok spat ked stlacim z
                    gs.undoMoves()
                    moveMade = True
                    
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        draw_game_state(screen, gs, validMoves, sqSelected) #vykreslime stav hry
        
        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'cierna vyhrala')
            else:
                drawText(screen, 'biela vyhrala')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, 'Koniec hry')

        clock.tick(MAX_FPS)         #nastavime fps
        p.display.flip()            #vykresli hru 

#bude vyznacovat poziciu kliknutia a kam sa moze panacik posunut
def highlightSquare(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):       #sqSelected je figurka ktorou sa mozem pohnut
            #highlight vybraneho stvorca
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(50)  #prehliadnost
            s.fill(p.Color('green'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            #highlight pohybu
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

#Zodpovedna za vsetky kreslenia

def draw_game_state(screen, gs, validMoves, sqSelected):
    drawBoard(screen)               #nakreslime hraciu plochu
    drawPieces(screen, gs.board)    #nakreslime figurky
    highlightSquare(screen, gs, validMoves, sqSelected)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]    #dame sivu aby sme tie cierne figurky potom videli
    for i in range(DIMENSION):                      #pre kazdy riadok      
        for j in range(DIMENSION):                  #pre kazdy stlpec
            color = colors[(i + j) % 2]             #dame farbu podla pocitadla
            p.draw.rect(screen, color, p.Rect(i * SQ_SIZE, j * SQ_SIZE, SQ_SIZE, SQ_SIZE)) #vykreslime poziciu


# nakreslime figurky pomocou aktualne gamestate.board
def drawPieces(screen, board):
    for r in range(DIMENSION):                                                                  #pre kazdy riadok   
        for c in range(DIMENSION):                                                              #pre kazdy stlpec 
            piece = board[r][c]
            if piece != "--":                                                                   #ak je tam nejaka figurka
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))  #vykreslime ju

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT / 2 - textObject.get_height() / 2) #vzorec aby bol text vzdy v strede
    screen.blit(textObject, textLocation)
    


if __name__ == "__main__":
    main()