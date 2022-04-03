# main file, ma na starosti user input a zobrazovanie aktualneho stavu hry

import pygame as p
import ChessEngine


WIDTH = HEIGHT = 512            # velkost okna
DIMENSION = 8                   # velkost hracieho pola
SQ_SIZE = HEIGHT // DIMENSION   # velkost jednej pozicie
MAX_FPS = 15                    # max fps pre animacie
IMAGES = {}                     # pre ukladanie obrazkov


#nacitavanie obrazkov, toto bude v maine


def load_images():
    pieces = ['wp, wN, wB, wR, wQ, wK, bp, bN, bB, bR, bQ, bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(f'img/${piece}.png'), (SQ_SIZE, SQ_SIZE))
    #transform sluzi nato aby obrazok vzdy vyzeral dobre
    # mame pristup k obrazkom, vieme sa k nim dostat cez 'IMAGES['wp']'


#main kusok kodu, bude sa zaoberat user inputom a updatovanim hry
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState() #vytvorime instanciu hry, gs = game state