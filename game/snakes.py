import pygame
from pygame.locals import *

if __name__=='__main__':
    pygame.init()

    # create game canvas
    surface = pygame.display.set_mode((500, 500))

    # fill the background
    surface.fill((0,0,0))
    pygame.display.flip()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False