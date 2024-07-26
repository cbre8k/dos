for module_path in ("basket.py", "poison.py", "alcohol.py", "config.py"):
    open(module_path).close()

import pyxel
import math
import time
import random

from basket import Basket
from poison import Poison
from alcohol import Alcohol
from config import GameConfig

class Game(GameConfig):
    def __init__(self):
        pyxel.init(
            self.DISPLAY_WIDTH, 
            self.DISPLAY_HEIGHT, 
            title="Dos"
        )
        pyxel.load("res/dos.pyxres")
        self.reset()
        pyxel.run(self.update, self.draw)

    def reset(self):
        self.score = 0
        self.basket = Basket(
            self.PLAYGROUND_WIDTH // 2 - self.BASKET_WIDTH // 2, 
            self.PLAYGROUND_HEIGHT - self.BASKET_HEIGHT - 10, 
            self.BASKET_VEL
        )
        self.alcohols = []
        self.poisons = []
        self.alcohol_timer = 0
        self.poison_timer = 0
        self.game_over = False
        self.game_pause = False
        self.accumulate_vel = 1
        self.accumulate_point = 1
        self.background_image_index = 0
        self.censored_grid = [
            [True for _ in range(self.BACKGROUND_WIDTH // self.SQUARE_SIZE)]
            for _ in range(self.BACKGROUND_HEIGHT // self.SQUARE_SIZE)
        ]
        self.points_until_next_unlock = self.POINTS_PER_SQUARE
        self.full_unlock_time = 0
        self.full_unlock_awarded = False

    def update(self):
        if not self.game_over and not self.game_pause:
            self.basket.update()
            self.update_items()
            self.check_collisions()
            self.update_censored_grid()
            if pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
                pyxel.play(0, 1)
                self.game_pause = True
        else:
            if (pyxel.btnp(pyxel.KEY_R) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_B)) and not self.game_pause:
                pyxel.play(0, 0)
                self.reset()
            if self.game_pause and (pyxel.btnp(pyxel.KEY_P) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A)):
                pyxel.play(0, 2)
                self.game_pause = False

    def update_items(self):
        self.alcohol_timer += 1
        self.poison_timer += 1

        if self.alcohol_timer > self.ALCOHOL_SPAWN_RATE:
            self.alcohol_timer = 0
            self.spawn_alcohol()

        if self.poison_timer > self.POISON_SPAWN_RATE:
            self.poison_timer = 0
            self.spawn_poison()

        self.alcohols = [
            alcohol for alcohol in self.alcohols 
            if alcohol.y < self.PLAYGROUND_HEIGHT
        ]
        self.poisons = [
            poison for poison in self.poisons 
            if poison.y < self.PLAYGROUND_HEIGHT
        ]

        for alcohol in self.alcohols:
            alcohol.update()
        for poison in self.poisons:
            poison.update()

    def spawn_alcohol(self):
        al_type = random.choice(self.ALCOHOL_TYPES)
        al_start_x = random.randint(0, self.PLAYGROUND_WIDTH - al_type["width"])
        rand_vel = random.randint(
            self.background_image_index + 1, self.background_image_index + 3
        )
        new_alcohol = Alcohol(
            al_start_x, 0, rand_vel * self.accumulate_vel, al_type
        )
        self.alcohols.append(new_alcohol)

    def spawn_poison(self):
        p_start_x = random.randint(0, self.PLAYGROUND_WIDTH - 15)
        rand_vel = random.randint(
            self.background_image_index + 1, self.background_image_index + 3
        )
        new_poison = Poison(p_start_x, 0, rand_vel * self.accumulate_vel)
        self.poisons.append(new_poison)

    def update_censored_grid(self):
        while self.score >= self.points_until_next_unlock:
            self.points_until_next_unlock += self.POINTS_PER_SQUARE
            self.unlock_random_square()

        if self.is_grid_fully_unlocked() and not self.full_unlock_awarded:
            pyxel.play(0, 4)
            self.full_unlock_awarded = True
            self.score += self.BIG_POINT_BONUS
            self.full_unlock_time = time.time()

        if self.full_unlock_awarded and time.time() - self.full_unlock_time >= self.BACKGROUND_DURATION and not self.background_image_index == len(self.BACKGROUND_LEVEL):
            pyxel.play(0, 5)
            self.change_background()

    def unlock_random_square(self):
        locked_squares = [
            (i, j) for i in range(len(self.censored_grid)) 
            for j in range(len(self.censored_grid[0])) 
            if self.censored_grid[i][j]
        ]
        if locked_squares:
            i, j = random.choice(locked_squares)
            self.censored_grid[i][j] = False

    def is_grid_fully_unlocked(self):
        return all(not cell for row in self.censored_grid for cell in row)

    def change_background(self):
        if self.background_image_index < len(self.BACKGROUND_LEVEL) - 1:
            self.background_image_index += 1
            self.censored_grid = [
                [True for _ in range(self.DISPLAY_WIDTH // self.SQUARE_SIZE)]
                for _ in range(self.DISPLAY_HEIGHT // self.SQUARE_SIZE)
            ]
            self.full_unlock_awarded = False

    def check_collisions(self):
        for alcohol in self.alcohols[:]:
            if self.is_collision(alcohol.x, alcohol.y, alcohol.w, alcohol.h):
                pyxel.play(0, 3)
                self.alcohols.remove(alcohol)
                self.score += math.floor(alcohol.points * self.accumulate_point)
                self.accumulate_vel += self.ACCUMULATE_VEL_INCREMENT
                self.accumulate_point += self.ACCUMULATE_POINT_INCREMENT

        for poison in self.poisons[:]:
            if self.is_collision(poison.x, poison.y, self.POISON_WIDTH, self.POISON_HEIGHT):
                pyxel.play(0, 6)
                self.poisons.remove(poison)
                self.game_over = True

    def is_collision(self, item_x, item_y, item_w, item_h):
        return (
            self.basket.x < item_x + item_w and
            self.basket.x + self.BASKET_WIDTH > item_x and
            item_y + item_h >= self.basket.y and
            item_y + item_h <= self.basket.y + self.BASKET_HEIGHT
        )

    def draw(self):
        pyxel.cls(0)
        pyxel.blt(0, 0, 0, 128, 0, self.PLAYGROUND_WIDTH, self.PLAYGROUND_HEIGHT, 0)
        self.draw_censored_background()
        self.basket.draw()
        for alcohol in self.alcohols:
            alcohol.draw()
        for poison in self.poisons:
            poison.draw()
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)
        if self.game_over:
            self.draw_game_over()
        if self.game_pause:
            self.draw_game_pause()

    def draw_censored_background(self):
        img_bank, u, v = self.BACKGROUND_LEVEL[self.background_image_index]["image"]
        pyxel.blt(
            self.BACKGROUND_WIDTH, 0, img_bank, u, v, 
            self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT, 0
        )
        for i, row in enumerate(self.censored_grid):
            for j, is_censored in enumerate(row):
                if is_censored:
                    color = random.randint(0, 7)
                    pyxel.rect(
                        self.BACKGROUND_WIDTH + j * self.SQUARE_SIZE, 
                        i * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE, 
                        color
                    )

    def draw_game_over(self):
        pyxel.blt(
            self.PLAYGROUND_WIDTH // 4, self.PLAYGROUND_HEIGHT // 2 - 7, 
            0, 0, 64, 64, 14, 0
        )
        pyxel.text(
            self.PLAYGROUND_WIDTH // 4 - 4, self.PLAYGROUND_HEIGHT // 2 + 10, 
            "Press R to Restart", pyxel.COLOR_WHITE
        )

    def draw_game_pause(self):
        pyxel.blt(
            self.PLAYGROUND_WIDTH // 4, self.PLAYGROUND_HEIGHT // 2 - 8, 
            0, 64, 64, 64, 16, 0
        )
        pyxel.text(
            self.PLAYGROUND_WIDTH // 4 - 4, self.PLAYGROUND_HEIGHT // 2 + 10, 
            "Press P to Resume", pyxel.COLOR_WHITE
        )

Game()
