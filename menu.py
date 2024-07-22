open("config.py").close()
import pyxel
from config import GameConfig

class Menu(GameConfig):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.options = ["Start Game", "Exit"]
        self.selected_option = 0
        self.prev_selected_option = 0  # Track the previously selected option
        self.active = True
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            pyxel.play(0, 0)
            self.selected_option = (self.selected_option - 1) % len(self.options)
        if pyxel.btnp(pyxel.KEY_DOWN):
            pyxel.play(0, 0)
            self.selected_option = (self.selected_option + 1) % len(self.options)
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.selected_option == 0:
                self.active = False
            elif self.selected_option == 1:
                pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        
        # Draw  options
        pyxel.blt(self.DISPLAY_WIDTH // 2 - 12.5 , self.DISPLAY_HEIGHT // 2 - 13, 0, 0, 82, 25, 13, 0)
        pyxel.blt(self.DISPLAY_WIDTH // 2 - 12.5 , self.DISPLAY_HEIGHT // 2 + 13, 0, 0, 98, 25, 13, 0)
        
        y = -9 if self.selected_option == 0 else 17
        current_y = self.height // 2 + y
        pyxel.blt(self.width // 2 - 20, current_y, 0, 1, 113, 5, 5, 0)

        if self.selected_option != self.prev_selected_option:
            prev_y = self.height // 2 + y
            pyxel.blt(self.width // 2 - 20, prev_y, 0, 0, 0, 0, 0, 0) 
            self.prev_selected_option = self.selected_option
