import pygame
from pygame.locals import *
import time
import random

class Food:
    def __init__(self, parent_screen, screen_size, block_size):
        self.parent_screen = parent_screen
        self.x = block_size[0] * random.randint(1, screen_size[0]//block_size[0] -1)
        self.y = block_size[1] * random.randint(1, screen_size[1]//block_size[1] -1)
        self.screen_size = screen_size
        self.block_size = block_size
    
        block = pygame.image.load("./game/resources/snake_food.jpg").convert()
        self.image = pygame.transform.scale(block, block_size)

    def move(self):
        num_x_blocks = self.screen_size[0]//self.block_size[0]
        num_y_blocks = self.screen_size[1]//self.block_size[1]
        rand_x = random.randint(1, num_x_blocks-1)
        rand_y = random.randint(1, num_y_blocks-1)
        self.x  = rand_x * self.block_size[0]
        self.y = rand_y * self.block_size[1]

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

class Snake:
    def __init__(self, parent_screen, screen_size, block_size, length):
        self.parent_screen = parent_screen
        self.x = [block_size[0] * (screen_size[0]//block_size[0])//2] * length
        self.y = [block_size[1] * (screen_size[1]//block_size[1])//2] * length
        self.screen_size = screen_size
        self.block_size = block_size
        self.direction = 'right'
        self.length = length

        # choose block
        block = pygame.image.load("./game/resources/snake_block.jpg").convert()
        self.block = pygame.transform.scale(block, block_size)

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((0,0,0))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= self.block_size[1]
            
        if self.direction == 'down':
            self.y[0] += self.block_size[1]
            
        if self.direction == 'left':
            self.x[0] -= self.block_size[0]
            
        if self.direction == 'right':
            self.x[0] += self.block_size[0]

        self.draw()

class Game:
    def __init__(self):
        self.screen_size = (1000, 1000)
        self.block_size = (20, 20)
        self.score = 0
        pygame.init()

        # create game canvas
        self.surface = pygame.display.set_mode(self.screen_size)

        # fill the background
        self.surface.fill((0,0,0))

        # create snake object
        self.snake = Snake(self.surface, self.screen_size, self.block_size, 2)
        self.snake.draw()

        # create food object
        self.food = Food(self.surface, self.screen_size, self.block_size)
        self.food.draw()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + self.block_size[0] and y1 >= y2 and y1 < y2 + self.block_size[1]:
            return True
        return False

    def play(self):
        self.snake.walk()
        self.food.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.food.x, self.food.y):
            self.snake.increase_length()
            self.food.move()
            self.score += 1

        # snake hit itself
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                raise "Game Over"
            
        # snake go out of bounds
        if self.snake.x[0] <= 0 or self.snake.y[0] <= 0 or self.snake.x[0] >= self.screen_size[0] or self.snake.y[0] >= self.screen_size[1]:
            raise "Game Over"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.surface.blit(score, (self.screen_size[0]-200, 10))

    def game_over(self):
        self.surface.fill((0,0,0))
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"GAME OVER", True, (255, 255, 255))
        text_rect1 = line1.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2-50))
        self.surface.blit(line1, text_rect1)
        line2 = font.render(f"Score: {self.score}", True, (255, 255, 255))
        text_rect2 = line2.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2))
        self.surface.blit(line2, text_rect2)

        line3 = font.render("Click Enter to play again, Escape to exit", True, (255, 255, 255))
        text_rect3 = line3.get_rect(center=(self.screen_size[0]//2, self.screen_size[1]//2+50))
        self.surface.blit(line3, text_rect3)
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, self.screen_size, self.block_size, 2)
        self.food = Food(self.surface, self.screen_size, self.block_size)
        self.score = 0

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    running = False

                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pause = False

                    if not pause:
                        if event.key == K_UP:
                            if self.snake.direction != 'down':
                                self.snake.move_up()

                        if event.key == K_DOWN:
                            if self.snake.direction != 'up':
                                self.snake.move_down()

                        if event.key == K_LEFT:
                            if self.snake.direction != 'right':
                                self.snake.move_left()

                        if event.key == K_RIGHT:
                            if self.snake.direction != 'left':
                                self.snake.move_right()

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            time.sleep(0.1)

if __name__=='__main__':
    game = Game()
    game.run()