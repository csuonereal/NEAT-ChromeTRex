from constants import *

class Ground:
    def __init__(self):
        self.ground_y = GROUND_DEFAULT_Y
        self.ground_x1 = 0
        self.ground_x2 = GROUND_WIDTH
        

    def move(self):
        self.ground_x1 -= GAME_SPEED
        self.ground_x2 -= GAME_SPEED

        if self.ground_x1 + GROUND_WIDTH < 0:
            self.ground_x1 = GROUND_WIDTH + self.ground_x2
        if self.ground_x2 + GROUND_WIDTH < 0:
            self.ground_x2 =  GROUND_WIDTH + self.ground_x1


    def draw(self):
        GAME.blit(GROUND_IMG, (self.ground_x1, self.ground_y)) 
        GAME.blit(GROUND_IMG, (self.ground_x2, self.ground_y))