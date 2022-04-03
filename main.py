#importujem kniznice
from os import kill
import pygame
import time
import sys

#init :)
pygame.init()

# wuhu farbicky a nastavovacky
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

# otvorenie okna
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("sach")

#board
board = [[' ' for i in range(8)] for i in range(8)]

#vytvorime si triedu ktora ukaze v akom time je figurka, ci ju moze zabit ina figurka alebo nemoze
class Piece:
    def __init__ (self, team, type, image, killable = False):
        self.team = team
        self.type = type
        self.image = image
        self.killable = killable

#importneme si figurky

#PRVY PARAMETER JE TEAM A DRUHY URCUJE O AKU FIGURKU IDE
bp = Piece('b', 'p', 'img/bp.png') #pesiak
wp = Piece('w', 'p', 'img/wB.png') 

bk = Piece('b', 'k', 'img/bK.png') #kral
wk = Piece('w', 'k', 'img/wK.png')

br = Piece('b', 'r', 'img/bR.png') #veza
wr = Piece('w', 'r', 'img/wR.png')

bb = Piece('b', 'b', 'img/bB.png') #strelec
wb = Piece('w', 'b', 'img/wB.png')

bq = Piece('b', 'q', 'img/bQ.png') #kralovna
wq = Piece('w', 'q', 'img/wQ.png')

wkh = Piece('w', 'kh', 'img/wN.png') #kon
bkh = Piece('b', 'kh', 'img/bN.png')


#zobrazenie na ploche
starting_order = {(0, 0): pygame.image.load(br.image), (1, 0): pygame.image.load(bkh.image),
                  (2, 0): pygame.image.load(bb.image), (3, 0): pygame.image.load(bk.image),
                  (4, 0): pygame.image.load(bq.image), (5, 0): pygame.image.load(bb.image),
                  (6, 0): pygame.image.load(bkh.image), (7, 0): pygame.image.load(br.image),
                  (0, 1): pygame.image.load(bp.image), (1, 1): pygame.image.load(bp.image),
                  (2, 1): pygame.image.load(bp.image), (3, 1): pygame.image.load(bp.image),
                  (4, 1): pygame.image.load(bp.image), (5, 1): pygame.image.load(bp.image),
                  (6, 1): pygame.image.load(bp.image), (7, 1): pygame.image.load(bp.image),
                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                  (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                  (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,                  
                  (0, 6): pygame.image.load(wp.image), (1, 6): pygame.image.load(wp.image),
                  (2, 6): pygame.image.load(wp.image), (3, 6): pygame.image.load(wp.image),
                  (4, 6): pygame.image.load(wp.image), (5, 6): pygame.image.load(wp.image),
                  (6, 6): pygame.image.load(wp.image), (7, 6): pygame.image.load(wp.image),
                  (0, 7): pygame.image.load(wr.image), (1, 7): pygame.image.load(wkh.image),
                  (2, 7): pygame.image.load(wb.image), (3, 7): pygame.image.load(wk.image),
                  (4, 7): pygame.image.load(wq.image), (5, 7): pygame.image.load(wb.image),
                  (6, 7): pygame.image.load(wkh.image), (7, 7): pygame.image.load(wr.image),
            
}

#kreslenie boardu

#treba urobit zobrazovanie na boarde
def create_board(board):
    board[0] = [br, b, bb, bq, bk, Piece('b', 'b', 'b_bishop.png'), \ 
               Piece('b', 'kn', 'b_knight.png'), Piece('b', 'r', 'b_rook.png')]

    board[7] = [Piece('w', 'r', 'w_rook.png'), Piece('w', 'kn', 'w_knight.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'q', 'w_queen.png'), Piece('w', 'k', 'w_king.png'), Piece('w', 'b', 'w_bishop.png'), \
               Piece('w', 'kn', 'w_knight.png'), Piece('w', 'r', 'w_rook.png')]

    for i in range(8):
        board[1][i] = Piece('b', 'p', 'b_pawn.png')
        board[6][i] = Piece('w', 'p', 'w_pawn.png')
    return board



# main loop
while True:
 