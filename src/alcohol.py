import pyxel
import config

class Alcohol(config.GameConfig):
    def __init__(self, x, y, vel, al_type):
        self.x = x
        self.y = y
        self.vel = vel
        self.type = al_type
        self.w = al_type["width"]
        self.h = al_type["height"]
        self.points = al_type["points"]

    def update(self):
        self.y += self.vel

    def draw(self):
        img_bank, u, v = self.type["image"]
        pyxel.blt(self.x, self.y, img_bank, u, v, self.w, self.h, 0)
        
