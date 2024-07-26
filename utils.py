import pyxel
import random

def play_sound(sound_id):
    pyxel.play(0, sound_id)

def check_collision(basket, item_x, item_y, item_w, item_h, basked_w, basket_h):
    return (
        basket.x < item_x + item_w and
        basket.x + basked_w > item_x and
        item_y + item_h >= basket.y and
        item_y + item_h <= basket.y + basket_h
    )

def unlock_random_square(censored_grid):
    locked_squares = [
        (i, j) for i in range(len(censored_grid)) 
        for j in range(len(censored_grid[0])) 
        if censored_grid[i][j]
    ]
    if locked_squares:
        i, j = random.choice(locked_squares)
        censored_grid[i][j] = False

def is_grid_fully_unlocked(censored_grid):
    return all(not cell for row in censored_grid for cell in row)

def change_background(game_instance, bg_w, bg_h, square_size):
    if game_instance.background_image_index < len(game_instance.BACKGROUND_LEVEL) - 1:
        game_instance.background_image_index += 1
        game_instance.censored_grid = [
            [True for _ in range(bg_w // square_size)]
            for _ in range(bg_h // square_size)
        ]
        game_instance.full_unlock_awarded = False
    else:
        game_instance.background_image_index = 0
        game_instance.censored_grid = [
            [True for _ in range(bg_w // square_size)]
            for _ in range(bg_h // square_size)
        ]
        game_instance.full_unlock_awarded = False
