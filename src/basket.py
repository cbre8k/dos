import pyxel
from config import GameConfig


class Basket(GameConfig):
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT) and self.x > 0:
            self.x -= self.vel
        if pyxel.btn(pyxel.KEY_RIGHT) and self.x < self.PLAYGROUND_WIDTH - self.BASKET_HEIGHT:
            self.x += self.vel

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 33, self.BASKET_WIDTH, self.BASKET_HEIGHT, 0)