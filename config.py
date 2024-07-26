class GameConfig:
    DISPLAY_WIDTH = 256
    DISPLAY_HEIGHT = 240
    
    PLAYGROUND_WIDTH = 128
    PLAYGROUND_HEIGHT = 240
    
    BACKGROUND_WIDTH = 128
    BACKGROUND_HEIGHT = 240
    
    BACKGROUND_DURATION = 10
    
    ALCOHOL_SPAWN_RATE = 25
    POISON_SPAWN_RATE = 80
    
    ACCUMULATE_POINT_INCREMENT = 0.005
    
    SQUARE_SIZE = 16
    POINTS_PER_SQUARE = 3
    BIG_POINT_BONUS = 50
    
    BASKET_WIDTH = 32
    BASKET_HEIGHT = 25
    BASKET_VEL = 5
    
    POISON_WIDTH = 16
    POISON_HEIGHT = 32
    
    ALCOHOL_TYPES = [
        {"image": (0, 0, 0), "points": 2, "height": 32, "width": 10}, 
        {"image": (0, 16, 0), "points": 3, "height": 32, "width": 32},
        {"image": (0, 48, 2), "points": 4, "height": 30, "width": 14},
        {"image": (0, 64, 0), "points": 5, "height": 32, "width": 11},
        {"image": (0, 78, 4), "points": 6, "height": 28, "width": 11},
    ]
    
    BACKGROUND_LEVEL = [
        {"image": (1, 0, 0)},
        {"image": (1, 128, 0)},
        {"image": (2, 0, 0)},
        {"image": (2, 128, 0)},
    ]
    
    MENU_BUTTON = [
        {"start": (0, 0, 82), "height": 13, "width": 25},
        {"exit": (0, 0, 98), "height": 13, "width": 25},
        {"select": (0, 1, 113), "height": 5, "width": 5},
    ]
