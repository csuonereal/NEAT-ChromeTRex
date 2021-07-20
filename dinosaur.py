import pygame
from constants import *

class Dino:
    def __init__(self):
        self.img = DINO_RUNNING[0]
        self.img_ind = 0
        self.dino_x = DINO_DEFAULT_X
        self.dino_y = DINO_DEFAULT_Y
        self.jump_vel = DINO_JUMP_VELOCITY
        self.coeff = 4

        self.dino_jump = False
        self.dino_run = True
        self.shape = self.img.get_rect().move(self.dino_x, self.dino_y)

    def jump(self):
        if self.dino_jump:
            self.dino_y -= self.jump_vel*self.coeff
            self.shape.y = self.dino_y
            self.jump_vel -= 0.8
        if self.jump_vel < - DINO_JUMP_VELOCITY:
            self.dino_jump = False
            self.jump_vel = DINO_JUMP_VELOCITY

    def run(self):
        self.dino_y = DINO_DEFAULT_Y
        self.dino_x = DINO_DEFAULT_X

        self.shape.y = self.dino_y

    def apply_movement(self,inp):
        if self.dino_jump:
            self.jump()
        elif self.dino_run:
            self.run()

        if inp[pygame.K_SPACE] and not self.dino_jump:
            self.dino_jump = True
            self.dino_run = False

        elif not self.dino_jump:
            self.dino_run = True
            self.dino_jump = False

    def animate(self):
        self.img_ind += 1
        if self.img_ind <= ANIM_SPEED:
            self.img = DINO_RUNNING[0]
        elif self.img_ind <= ANIM_SPEED*2:
            self.img = DINO_RUNNING[1]
        elif self.img_ind <= ANIM_SPEED*3:
            self.img_ind = DINO_RUNNING[0]
            self.img_ind = 0

        if self.dino_jump:
            self.img = DINO_JUMP
            self.img_ind = 0
       
        GAME.blit(self.img, (self.dino_x, self.dino_y))

    def draw(self):
        self.animate()