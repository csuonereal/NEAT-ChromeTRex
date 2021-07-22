import pygame
import os

pygame.init()
pygame.font.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

FPS = 30

GAME_WIDTH = 1750
GAME_HEIGHT = 500

GAME = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))


GROUND_IMG = pygame.image.load(os.path.join("imgs","Other","Track.png"))
GROUND_WIDTH = GROUND_IMG.get_width()
GROUND_DEFAULT_Y = GAME_HEIGHT - 100


DINO_RUNNING = [pygame.image.load(os.path.join("imgs","Dino","DinoRun1.png")),
                pygame.image.load(os.path.join("imgs","Dino","DinoRun2.png"))]

DINO_JUMP = pygame.image.load(os.path.join("imgs","Dino","DinoJump.png"))
DINO_HEIGHT = DINO_JUMP.get_height()
DINO_WIDTH = DINO_JUMP.get_width()
DINO_DEFAULT_X = 200
DINO_DEFAULT_Y = GROUND_DEFAULT_Y - 60
DINO_JUMP_VELOCITY = 9.5


LARGE_CACTUS = [pygame.image.load(os.path.join("imgs","Cactus","LargeCactus1.png")),
                pygame.image.load(os.path.join("imgs","Cactus","LargeCactus2.png")),
                pygame.image.load(os.path.join("imgs","Cactus","LargeCactus3.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("imgs","Cactus","SmallCactus1.png")),
                pygame.image.load(os.path.join("imgs","Cactus","SmallCactus2.png")),
                pygame.image.load(os.path.join("imgs","Cactus","SmallCactus3.png"))]


GAME_SPEED = 75
ANIM_SPEED = 3


SCORE = 0
GEN = 0

FONT = pygame.font.SysFont('comicsans', 44)


def draw_score(score,gen,dinos):
    score_txt = FONT.render("Score:"+str(score), 1, BLACK)
    gen_txt = FONT.render("Gen:"+str(gen), 1, BLACK)
    alive_txt = FONT.render("Alive: " + str(len(dinos)),1,BLACK)
   
   
    GAME.blit(score_txt, (10,10))
    GAME.blit(gen_txt, (10,50))
    GAME.blit(alive_txt, (10,90))


  