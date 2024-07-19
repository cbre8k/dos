import entity

class Alcohol(entity.Entity):
    def __init__(self, img, img_x, img_y, tile_x, tile_y):
        super().__init__(img, img_x, img_y, tile_x, tile_y)
        self.type = self.TYPE_BEER

    def update(self):
        pass

    def drink(self, player):
        raise NotImplementedError
    
class Wine(Alcohol):
    def __init__(self, tile_x, tile_y):
        super().__init__(0, 56, 64, tile_x, tile_y)
        
    def drink(self, player):
        player.point += 5

class Beer(Alcohol):
    def __init__(self, tile_x, tile_y):
        super().__init__(0, 56, 64, tile_x, tile_y)

    def drink(self, player):
        player.point += 10
        
class Rum(Alcohol):
    def __init__(self, tile_x, tile_y):
        super().__init__(0, 56, 64, tile_x, tile_y)
        
    def drink(self, player):
        player.point += 15

class Chivas(Alcohol):
    def __init__(self, tile_x, tile_y):
        super().__init__(0, 56, 64, tile_x, tile_y)
        
    def drink(self, player):
        player.point += 20
        
