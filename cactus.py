import random
from constants import *



class Cactus:
    def __init__(self):
        self.cactus_x = GAME_WIDTH
        self.cactus_y = GROUND_DEFAULT_Y - 70
        self.passed = False
        self.generate_random_cactus()

    def generate_random_cactus(self):
        self.type = random.randint(0,1)
        if self.type == 0:
            self.cactus_amount = random.randint(0,2)
            self.cactus_y = self.cactus_y + 40
            self.img = SMALL_CACTUS[self.cactus_amount]
            self.shape = self.img.get_rect().move(self.cactus_x, self.cactus_y)
        elif self.type == 1:
            self.cactus_amount = random.randint(0,2)
            self.img = LARGE_CACTUS[self.cactus_amount]
            self.shape = self.img.get_rect().move(self.cactus_x, self.cactus_y)

    def move(self):
        self.cactus_x -= GAME_SPEED
        self.shape.x = self.cactus_x

    def collision_control(self,dino):
        if self.shape.colliderect(dino.shape):
            return True
        else:
            return False
    
    def draw(self):
        GAME.blit(self.img, (self.cactus_x, self.cactus_y))
