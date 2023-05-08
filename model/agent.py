import torch 
import random
import numpy as np
from collections import deque
from game.snakes import *
from model.model import Linear_QNet, QTrainer
from model.helper import plot

MAX_MEMORY = 100000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, LR, self.gamma)

    def get_state(self, game):
        state = []
        snake_head = (game.snake.x[0], game.snake.y[0])

        clockwise_dir = ['right', 'down', 'left', 'up']
        curr_dir_idx = clockwise_dir.index(game.snake.direction)

        points = {
            'right': (snake_head[0] + game.block_size[0], snake_head[1]),
            'down': (snake_head[0], snake_head[1] + game.block_size[1]),
            'left': (snake_head[0] - game.block_size[0], snake_head[1]),
            'up': (snake_head[0], snake_head[1] - game.block_size[1])
            }

        snake_left = points[clockwise_dir[(curr_dir_idx+1)%4]]
        snake_right = points[clockwise_dir[(curr_dir_idx-1)%4]]
        snake_straight = points[clockwise_dir[curr_dir_idx]]

        # dangers
        for danger in [snake_left, snake_right, snake_straight]:
            is_danger = 0

            # check if collision with body
            for i in range(1, game.snake.length):
                if game.is_collision(danger[0], danger[0], game.snake.x[i], game.snake.y[i]):
                    is_danger = 1
                    break

            # check if collision with wall
            if danger[0] < 0 or danger[0] < 0 or danger[0] >= game.screen_size[0] or danger[0] >= game.screen_size[1]:
                is_danger = 1

            state.append(is_danger)

        # directions
        for direction in ['left', 'right', 'up', 'down']:
            if game.snake.direction == direction:
                state.append(1)
            else:
                state.append(0)

        # food
        state.append(int(game.food.x < snake_head[0]))
        state.append(int(game.food.x > snake_head[0]))
        state.append(int(game.food.y < snake_head[1]))
        state.append(int(game.food.y > snake_head[1]))

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, game_over):
        self.memory.append((state, action, reward, next_state, game_over))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, game_overs = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, game_overs)

    def train_short_memory(self, state, action, reward, next_state, game_over):
        self.trainer.train_step(state, action, reward, next_state, game_over)

    def get_action(self, state):
        # random moves:
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0,2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record =  0
    agent = Agent()
    game = Game()
    
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, game_over, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, game_over)

        # store in memory
        agent.remember(state_old, final_move, reward, state_new, game_over)

        if game_over:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print(f"Game {agent.n_games}, Score {score}, Record {record}")

            plot_scores.append(score)
            total_score += score
            mean_score = total_score/agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__=='__main__':
    train()