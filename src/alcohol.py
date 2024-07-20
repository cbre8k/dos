import pyxel
from config import GameConfig

class Alcohol(GameConfig):
    def __init__(self, x, y, al_type):
        self.x = x
        self.y = y
        self.type = al_type
        self.vel = al_type["vel"]
        self.w = al_type["width"]
        self.h = al_type["height"]
        self.points = al_type["points"]

    def update(self):
        self.y += self.vel

    def draw(self):
        img_bank, u, v = self.type["image"]
        pyxel.blt(self.x, self.y, img_bank, u, v, self.w, self.h, 0)
        
