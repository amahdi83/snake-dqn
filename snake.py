import pygame
import numpy as np
from random import randrange
from pygame import Rect


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.font_path = "assets/fonts/OpenSans-Light.ttf"
        self.h4 = pygame.font.Font(self.font_path, 40)
        self.h5 = pygame.font.Font(self.font_path, 26)

        self.WHITE = (255, 255, 255)
        self.BLACK = (10, 10, 10)
        self.GRAY_1 = (26, 26, 26)
        self.GRAY_2 = (35, 35, 35)
        self.GRAY_3 = (55, 55, 55)

        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()

        self.dirs = {pygame.K_UP: 1, pygame.K_DOWN: 1, pygame.K_LEFT: 1, pygame.K_RIGHT: 1}

        self.block_size = 28
        self.GRID_WIDTH = 20
        self.GRID_HEIGHT = 20
        self.GRID_OFFSET = 20

        self.time, self.time_Step = 0, 110

        self.reset()

    def reset(self):
        self.score = 0
        self.food_eaten = 0
        self.level = 1
        self.food_per_level = 5

        self.snake = pygame.Rect([0, 0, self.block_size - 2, self.block_size - 2])
        self.snake.center = self.get_random_pos()
        self.length = 1
        self.segments = [self.snake.copy()]
        self.snake_dir = (0, 0)

        self.food = self.snake.copy()
        self.food.center = self.get_random_pos()

    def get_random_pos(self):
        x = randrange(self.GRID_OFFSET + self.block_size, self.GRID_WIDTH * self.block_size, self.block_size)
        y = randrange(self.GRID_OFFSET + self.block_size, self.GRID_HEIGHT * self.block_size, self.block_size)
        return [x + self.block_size // 2, y + self.block_size // 2]

    def draw_grid(self):
        for x in range(20, 580, self.block_size):
            for y in range(20, 580, self.block_size):
                pygame.draw.rect(self.screen, self.GRAY_2, Rect(x, y, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, self.GRAY_1, Rect(x, y, self.block_size, self.block_size), 1)

        pygame.draw.rect(self.screen, self.WHITE, pygame.Rect(600, 0, 200, 600))

        text_score = self.h5.render("SCORE", 1, self.BLACK)
        score_value = self.h4.render(str(self.score), 1, self.BLACK)
        text_level = self.h5.render("LEVEL", 1, self.BLACK)
        level_value = self.h4.render(str(self.level), 1, self.BLACK)

        self.screen.blit(text_score, (630, 50))
        self.screen.blit(score_value, (640, 82))
        self.screen.blit(text_level, (630, 150))
        self.screen.blit(level_value, (640, 182))
        
    def check_collision(self, rect):
        if rect.left < 20 or rect.right > 580 or rect.top < 20 or rect.bottom > 580:
            return True
        if rect.collidelist(self.segments[:-1]) != -1:
            return True
        return False

    def move(self, rect, direction):
        new_rect = rect.copy()
        new_rect.move_ip(direction)
        return new_rect

    def turn_left(self, direction):
        x, y = direction
        return (-y, x)

    def turn_right(self, direction):
        x, y = direction
        return (y, -x)


    
    def render(self, delay=0):
        self.update()
        if delay > 0:
            pygame.time.delay(delay)

    
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                new_dir = None
                if event.key == pygame.K_UP:
                    new_dir = (0, -self.block_size)
                elif event.key == pygame.K_DOWN:
                    new_dir = (0, self.block_size)
                elif event.key == pygame.K_LEFT:
                    new_dir = (-self.block_size, 0)
                elif event.key == pygame.K_RIGHT:
                    new_dir = (self.block_size, 0)
    
                if new_dir:
                    # Prevent reversing direction
                    if (new_dir[0] == -self.snake_dir[0] and self.snake_dir[0] != 0) or \
                       (new_dir[1] == -self.snake_dir[1] and self.snake_dir[1] != 0):
                        return
    
                    next_head = self.move(self.snake, new_dir)
                    if not self.check_collision(next_head):
                        self.snake_dir = new_dir
                        
                        

    def update(self):
        self.screen.fill(self.GRAY_1)
        self.draw_grid()

        self_eating = self.snake.collidelist(self.segments[:-1]) != -1
        if (
            self.snake.left < 20
            or self.snake.right > 580
            or self.snake.top < 20
            or self.snake.bottom > 580
            or self_eating
        ):
            pygame.time.delay(500)
            self.reset()

        if self.snake.center == self.food.center:
            self.food.center = self.get_random_pos()
            self.length += 1
            self.score += 10
            self.food_eaten += 1

        pygame.draw.rect(self.screen, "red", self.food)
        for i, segment in enumerate(self.segments):
            color = "orange" if i == len(self.segments) - 1 else "green"
            pygame.draw.rect(self.screen, color, segment)

        time_now = pygame.time.get_ticks()
        if time_now - self.time > self.time_Step:
            self.time = time_now
            self.snake.move_ip(self.snake_dir)
            self.segments.append(self.snake.copy())
            self.segments = self.segments[-self.length:]

        self.level = 1 + (self.food_eaten // self.food_per_level)
        self.time_Step = max(50, 110 - (self.level - 1) * 5)

        pygame.display.flip()
        self.clock.tick(60)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            


if __name__ == "__main__":
    game = SnakeGame()
    game.run()