import math
import pyxel
import random
import config
import basket as bk
import poison as ps
import alcohol as al

class Game(config.GameConfig):
    def __init__(self):
        pyxel.init(
            self.DISPLAY_WIDTH, 
            self.DISPLAY_HEIGHT, 
            title="Drunk Or Strip"
        )
        pyxel.load("../res/assets.pyxres")
        self.reset()
        pyxel.run(self.update, self.draw)
    
    def reset(self):
        self.score = 0
        self.basket = bk.Basket(
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
    
    def update(self):
        if not self.game_over and not self.game_pause:
            self.basket.update()
            self.update_alcohols()
            self.update_poisons()
            self.check_collisions()
            self.update_background()
            if pyxel.btnp(pyxel.KEY_P):
                self.game_pause = True
        else:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            if self.game_pause and pyxel.btnp(pyxel.KEY_P):
                self.game_pause = False
                
    
    def update_alcohols(self):
        self.alcohol_timer += 1
        if self.alcohol_timer > 30:
            self.alcohol_timer = 0
            al_type = random.choice(self.ALCOHOL_TYPES)
            al_start_x = random.randint(0, self.PLAYGROUND_WIDTH - al_type["width"])
            rand_vel = random.randint(self.background_image_index + 1, self.background_image_index + 3)
            new_alcohol = al.Alcohol(al_start_x, 0, rand_vel * self.accumulate_vel, al_type)
            self.alcohols.append(new_alcohol)
        for alcohol in self.alcohols:
            alcohol.update()
        self.alcohols = [alcohol for alcohol in self.alcohols if alcohol.y < self.PLAYGROUND_HEIGHT]
    
    def update_poisons(self):
        self.poison_timer += 1
        if self.poison_timer > 100:
            self.poison_timer = 0
            p_start_x = random.randint(0, self.PLAYGROUND_WIDTH - 15)
            rand_vel = random.randint(self.background_image_index + 1, self.background_image_index + 3)
            new_poison = ps.Poison(p_start_x, 0, rand_vel * self.accumulate_vel)
            self.poisons.append(new_poison)
        for poison in self.poisons:
            poison.update()
        self.poisons = [poison for poison in self.poisons if poison.y < self.PLAYGROUND_HEIGHT]
    
    def update_background(self):
        # Change background image based on score
        if self.score < 100:
            self.background_image_index = 0
        elif self.score < 200:
            self.background_image_index = 1
        elif self.score < 300:
            self.background_image_index = 2
        else:
            self.background_image_index = 3
    
    def check_collisions(self):
        def is_collision(item_x, item_y, item_w, item_h):
            # Check if the bottom of the item hits the top of the basket
            return (self.basket.x < item_x + item_w and
                    self.basket.x + self.BASKET_WIDTH > item_x and
                    item_y + item_h >= self.basket.y and
                    item_y + item_h <= self.basket.y + self.BASKET_HEIGHT)

        # Check collisions with alcohols
        for alcohol in self.alcohols[:]:
            if is_collision(alcohol.x, alcohol.y, alcohol.w, alcohol.h):
                self.alcohols.remove(alcohol)
                self.score += math.floor(alcohol.points * self.accumulate_point)
                self.accumulate_vel += 0.1
                self.accumulate_point += 0.02

        # Check collisions with poisons
        for poison in self.poisons[:]:
            if is_collision(poison.x, poison.y, self.POISON_WIDTH, self.POISON_HEIGHT):
                self.poisons.remove(poison)
                self.game_over = True

    def draw(self):
        pyxel.cls(0)
        
        pyxel.blt(0, 0, 0, 128, 0, self.PLAYGROUND_WIDTH, self.PLAYGROUND_HEIGHT, 0)
        
        img_bank, u, v = self.BACKGROUND_LEVEL[self.background_image_index]["image"]
        pyxel.blt(self.BACKGROUND_WIDTH, 0, img_bank, u, v, self.BACKGROUND_WIDTH, self.BACKGROUND_HEIGHT, 0)
        
        self.basket.draw()
        
        for alcohol in self.alcohols:
            alcohol.draw()
        for poison in self.poisons:
            poison.draw()
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)
        
        if self.game_over:
            pyxel.blt(self.PLAYGROUND_WIDTH // 4, self.PLAYGROUND_HEIGHT // 2 - 7, 0, 0, 64, 64, 14, 0)
            pyxel.text(self.PLAYGROUND_WIDTH // 4 - 4, self.PLAYGROUND_HEIGHT // 2 + 10, "Press R to Restart", pyxel.COLOR_WHITE)

        if self.game_pause:
            pyxel.blt(self.PLAYGROUND_WIDTH // 4, self.PLAYGROUND_HEIGHT // 2 - 8, 0, 64, 64, 64, 16, 0)
            pyxel.text(self.PLAYGROUND_WIDTH // 4 - 4, self.PLAYGROUND_HEIGHT // 2 + 10, "Press P to Resume", pyxel.COLOR_WHITE)


if __name__ == "__main__":
    Game()
