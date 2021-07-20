import pygame
from constants import *

class Dino:
    def __init__(self):
        self.img = DINO_RUNNING[0]
        self.img_ind = 0
        self.dino_x = DINO_DEFAULT_X
        self.dino_y = DINO_DEFAULT_Y
        self.jump_vel = 0
        self.time = 0
        self.acceleration = 2

        self.dino_jump = False
        self.dino_run = True
        self.shape = self.img.get_rect().move(self.dino_x, self.dino_y)

    def jump(self):
        if self.dino_jump:
            return
        else:
            self.time = 0
            self.jump_vel = -DINO_JUMP_VELOCITY


    def move(self):
        self.time += 1
        # s = u*t + 0.5*a*t^2
        displacement = self.jump_vel*self.time + 0.5*self.acceleration*self.time**2
        if displacement > 20:
            displacement = 20
        elif displacement < 0:
            displacement -= 3

        self.dino_y += displacement
        self.shape.y = self.dino_y
        if self.dino_y >= DINO_DEFAULT_Y:
            self.dino_jump = False
            self.dino_y  = DINO_DEFAULT_Y
        else:
            self.dino_jump = True
       
        

    def animate(self):
        self.img_ind += 1
        if self.img_ind <= ANIM_SPEED:
            self.img = DINO_RUNNING[0]
        elif self.img_ind <= ANIM_SPEED*2:
            self.img = DINO_RUNNING[1]
        elif self.img_ind <= ANIM_SPEED*3:
            self.img_ind = DINO_RUNNING[0]
            self.img_ind = 0

        if self.dino_jump and  self.dino_y < DINO_DEFAULT_Y:
            self.img = DINO_JUMP
            self.img_ind = 0
       
        GAME.blit(self.img, (self.dino_x, self.dino_y))

    def draw(self):
        self.animate()

   