import pygame
import random
import numpy as np
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font("arial.ttf", 25)


# reset
# reward
# play(action) -> direction
# game_teration
# is_collision

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple("Point", "x,y")

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
BACKGROUND = (175, 215, 70)


class SnakeGameAI:

    def __init__(self, w=640, h=480):

        self.direction = None
        self.BLOCK_SIZE = 20
        self.SPEED = 15
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        # init game state
        self.reset()

    def reset(self):
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [self.head, Point(self.head.x - self.BLOCK_SIZE, self.head.y),
                      Point(self.head.x - (2 * self.BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0

    def _place_food(self):
        x = random.randint(0, (self.w - self.BLOCK_SIZE) // self.BLOCK_SIZE) * self.BLOCK_SIZE
        y = random.randint(0, (self.h - self.BLOCK_SIZE) // self.BLOCK_SIZE) * self.BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):
        self.frame_iteration += 1
        # 1 collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        # move snake
        self._move(action)
        self.snake.insert(0, self.head)

        # check if game over
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # place new food or move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        # update ui and clock
        self._update_ui()
        self.clock.tick(self.SPEED)
        # return game over and score
        game_over = False

        return reward, game_over, self.score

    def is_collision(self, point=None):
        if point is None:
            point = self.head
        # hits boundary
        if point.x > self.w - self.BLOCK_SIZE or point.x < 0 or point.y > self.h - self.BLOCK_SIZE or point.y < 0:
            return True
        # hits itself
        if point in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BACKGROUND)

        for point in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(point.x, point.y, self.BLOCK_SIZE, self.BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(point.x + 4, point.y + 4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, self.BLOCK_SIZE, self.BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, BLACK)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # [straight ,right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]  # no change
        elif np.array_equal(action, [0, 1, 0]):  # clockwise r->d->l->u
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        elif np.array_equal(action, [0, 1, 0]):  # counter clockwise r->u->l->d
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += self.BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= self.BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= self.BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += self.BLOCK_SIZE

        self.head = Point(x, y)

# if __name__ == "__main__":
#     game = SnakeGame()
#
#     # game loop
#     while True:
#         game_over, score = game.play_step()
#
#         if game_over == True:
#             break
#
#     print("Final score", score)
#     # break if game over
#
#     pygame.quit()
