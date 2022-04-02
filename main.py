import pygame
pygame.init()

# otvorenie okna
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My First Game")

# wuhu farbicky
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)


while True:
    screen.fill(0,0,0)


pygame.quit()
