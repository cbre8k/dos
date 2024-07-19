import pyxel

class Entity:
    TYPE_PLAYER = 0
    TYPE_BEER = 1
    TYPE_POISON = 2

    def __init__(self, img, img_x, img_y, tile_x, tile_y):
        self.img = img
        self.img_x = img_x
        self.img_y = img_y
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.type = -1

    def update(self):
        raise NotImplementedError

    def draw(self, cam):
        if (
            self.tile_x * 8 + 8 < cam.x
            or self.tile_x >= cam.x + cam.w
            or self.tile_y * 8 <= cam.y - 8
            or self.tile_y * 8 >= cam.y + cam.h
        ):
            return
        # blt(x, y, img, u, v, w, h, [colkey])
        pyxel.blt(
            40 + self.tile_x * 8 - cam.x,
            8 + self.tile_y * 8 - cam.y,
            self.img,
            self.img_x,
            self.img_y,
            8,
            8,
        )