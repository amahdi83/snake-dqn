
import numpy as np
from snake import SnakeGame


class SnakeEnv(SnakeGame):
    def __init__(self, render_mode=True):
        self.render_mode = render_mode
        super().__init__()

    def reset(self):
        super().reset()
        self.snake_dir = (0, -self.block_size)  # Start moving up
        self.frame = 0
        return self.get_state()

    def step(self, action):
        self.frame += 1

        # Map action to direction
        if action == 1:  # Left
            self.snake_dir = self.turn_left(self.snake_dir)
        elif action == 2:  # Right
            self.snake_dir = self.turn_right(self.snake_dir)
        # action == 0: straight (no change)

        # Move snake
        new_head = self.snake.copy()
        new_head.move_ip(self.snake_dir)

        # Check collision
        collision = (
            new_head.left < 20 or new_head.right > 580 or
            new_head.top < 20 or new_head.bottom > 580 or
            new_head.collidelist(self.segments[:-1]) != -1
        )

        reward = 0
        done = False

        if collision or self.frame > 100 * self.length:
            reward = -10
            done = True
            return self.get_state(), reward, done

        self.snake = new_head
        self.segments.append(self.snake.copy())

        if self.snake.center == self.food.center:
            self.length += 1
            self.score += 10
            self.food_eaten += 1
            self.food.center = self.get_random_pos()
            reward = 10
        else:
            self.segments = self.segments[-self.length:]

        self.level = 1 + (self.food_eaten // self.food_per_level)
        self.time_Step = max(50, 110 - (self.level - 1) * 5)

        if self.render_mode:
            self.render()

        return self.get_state(), reward, done

    def get_state(self):
        head = self.snake
        food_dx = np.sign(self.food.centerx - head.centerx)
        food_dy = np.sign(self.food.centery - head.centery)
        dir_x = np.sign(self.snake_dir[0])
        dir_y = np.sign(self.snake_dir[1])
        danger_straight = self.check_collision(self.move(head, self.snake_dir))
        danger_left = self.check_collision(self.move(head, self.turn_left(self.snake_dir)))
        danger_right = self.check_collision(self.move(head, self.turn_right(self.snake_dir)))

        return np.array([danger_straight, danger_left, danger_right, food_dx, food_dy, dir_x, dir_y], dtype=np.float32)