import pyxel
import config

class Poison(config.GameConfig):
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel
        
    def update(self):
        self.y += self.vel
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 96, 0, self.POISON_WIDTH, self.POISON_HEIGHT, 0)
