class GameConfig:
    DISPLAY_WIDTH = 256
    DISPLAY_HEIGHT = 240

    PLAYGROUND_WIDTH = 128
    PLAYGROUND_HEIGHT = 240

    BACKGROUND_WIDTH = 128
    BACKGROUND_HEIGHT = 240

    BASKET_WIDTH = 32
    BASKET_HEIGHT = 25
    BASKET_VEL = 5

    POISON_WIDTH = 16
    POISON_HEIGHT = 32
    POISON_VEL = 2
    
    ALCOHOL_TYPES = [
        {"image": (0, 0, 0), "points": 1, "vel": 1, "height": 32, "width": 10},  # ken
        {"image": (0, 16, 0), "points": 2, "vel": 2, "height": 32, "width": 32},
        {"image": (0, 48, 2), "points": 3, "vel": 2, "height": 30, "width": 14},
        {"image": (0, 64, 0), "points": 4, "vel": 3, "height": 32, "width": 11},
        {"image": (0, 78, 4), "points": 5, "vel": 3.5, "height": 28, "width": 11},
    ]

    BACKGROUND_LEVEL = [
        {"image": (1, 0, 0)},
        {"image": (1, 128, 0)},
        {"image": (2, 0, 0)},
        {"image": (2, 128, 0)},
    ]
