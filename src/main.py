import pyxel
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
            title="Drunk Or Strip"
        )
        pyxel.load("../res/assets.pyxres")
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
        self.background_image_index = 0
    
    def update(self):
        if not self.game_over:
            self.basket.update()
            self.update_alcohols()
            self.update_poisons()
            self.check_collisions()
            self.update_background()
        else:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
    
    def update_alcohols(self):
        self.alcohol_timer += 1
        if self.alcohol_timer > 30:
            self.alcohol_timer = 0
            al_type = random.choice(self.ALCOHOL_TYPES)
            al_start_x = random.randint(0, self.PLAYGROUND_WIDTH - al_type["width"])
            new_alcohol = Alcohol(al_start_x, 0, al_type)
            self.alcohols.append(new_alcohol)
        for alcohol in self.alcohols:
            alcohol.update()
        self.alcohols = [alcohol for alcohol in self.alcohols if alcohol.y < self.PLAYGROUND_HEIGHT]
    
    def update_poisons(self):
        self.poison_timer += 1
        if self.poison_timer > 100:
            self.poison_timer = 0
            p_start_x = random.randint(0, self.PLAYGROUND_WIDTH - 15)
            new_poison = Poison(p_start_x, 0, self.POISON_VEL)
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
            return (self.basket.x < item_x + item_w and
                    self.basket.x + self.BASKET_WIDTH > item_x and
                    self.basket.y < item_y + item_h and
                    self.basket.y + self.BASKET_HEIGHT > item_y)
        
        # Check collisions with alcohols
        for alcohol in self.alcohols[:]:
            if is_collision(alcohol.x, alcohol.y, alcohol.w, alcohol.h):
                self.alcohols.remove(alcohol)
                self.score += alcohol.points

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
            pyxel.text(self.PLAYGROUND_WIDTH // 2 - 40, self.PLAYGROUND_HEIGHT // 2, "GAME OVER", pyxel.COLOR_RED)
            pyxel.text(self.PLAYGROUND_WIDTH // 2 - 50, self.PLAYGROUND_HEIGHT // 2 + 10, "Press R to Restart", pyxel.COLOR_RED)

if __name__ == "__main__":
    Game()
