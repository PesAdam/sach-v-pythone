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
    load_images()               #nacitame obrzky, robime to iba raz!!!
    running = True              #bezime? bezime!
    while running:                  #ak bezi tak sa pozre ci nahodou neni niekde beziaci pygame event
        for e in p.event.get():     #ak je niekde event, tak ho vypne
            if e.type == p.QUIT:    #ak je to quit event, tak sa ukonci
                running = False     
        draw_game_state(screen, gs) #vykreslime stav hry
        clock.tick(MAX_FPS)         #nastavime fps
        p.display.flip()            #vykresli hru 

#Zodpovedna za vsetky kreslenia

def draw_game_state(screen, gs):
    drawBoard(screen)               #nakreslime hraciu plochu
    
    drawPieces(screen, gs.board)    #nakreslime figurky


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]    #dame sivu aby sme tie cierne figurky potom videli
    for i in range(DIMENSION):                      #pre kazdy riadok      
        for j in range(DIMENSION):                  #pre kazdy stlpec
            color = colors[(i + j) % 2]             #dame farbu podla pocitadla
            p.draw.rect(screen, color, p.Rect(i * SQ_SIZE, j * SQ_SIZE, SQ_SIZE, SQ_SIZE)) #vykreslime poziciu


# nakreslime figurky pomocou aktualne gamestate.board
def drawPieces(screen, board):
    for row in range(DIMENSION):                #pre kazdy riadok
        for col in range(DIMENSION):            #pre kazdy stlpec
            piece = board[row][col]             #zoberieme figurku
            if piece != "--":                   #ak neni prazdno
                screen.blit(IMAGES[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE)) #nakreslime ju
    
if __name__ == "__main__":
    main()