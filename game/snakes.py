import pygame
import time

if __name__=='__main__':
    pygame.init()

    # create game canvas
    surface = pygame.display.set_mode((500, 500))

    # fill the background
    surface.fill((0,0,0))
    surface.display.flip()

    # test