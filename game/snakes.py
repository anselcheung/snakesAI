import pygame
from pygame.locals import *

class Snake:
    def __init__(self, parent_screen, screen_size, block_size):
        self.parent_screen = parent_screen
        self.x = screen_size[0]//2
        self.y = screen_size[1]//2
        self.screen_size = screen_size
        self.block_size = block_size

        # choose block
        block = pygame.image.load("./game/resources/snake_block.jpg").convert()
        self.block = pygame.transform.scale(block, block_size)

    def draw(self):
        self.parent_screen.fill((0,0,0))
        self.parent_screen.blit(self.block, (self.x, self.y))
        pygame.display.flip()
    
    def move_left(self):
        self.x -= self.block_size[0]
        self.draw()

    def move_right(self):
        self.x += self.block_size[0]
        self.draw()

    def move_up(self):
        self.y -= self.block_size[1]
        self.draw()

    def move_down(self):
        self.y += self.block_size[1]
        self.draw()
        

class Game:
    def __init__(self):
        self.screen_size = (1000, 1000)
        self.block_size = (20, 20)
        pygame.init()

        # create game canvas
        self.surface = pygame.display.set_mode(self.screen_size)

        # fill the background
        self.surface.fill((0,0,0))

        # create snake object
        self.snake = Snake(self.surface, self.screen_size, self.block_size)
        self.snake.draw()

    def run(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False
                
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.snake.move_up()

                    if event.key == K_DOWN:
                        self.snake.move_down()

                    if event.key == K_LEFT:
                        self.snake.move_left()

                    if event.key == K_RIGHT:
                        self.snake.move_right()

if __name__=='__main__':
    game = Game()
    game.run()