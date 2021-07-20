import pygame
import random
from constants import *
from dinosaur import *
from ground import *
from cactus import *



def draw_screen(dino,obstacles,ground,score):
    GAME.fill(WHITE)
    ground.draw()
    for obstacle in obstacles:
        obstacle.draw()
    dino.draw()
    draw_score(SCORE)

def main():

    ground = Ground()
    dino = Dino()
    obstacles = [Cactus()]


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        user_input = pygame.key.get_pressed()
        obstacle_dino_ground_controller(obstacles,dino,ground,user_input)

        global SCORE 
        SCORE += 1
        draw_screen(dino,obstacles,ground,SCORE)
        pygame.display.update()


def obstacle_dino_ground_controller(obstacles,dino,ground,user_input):
    for obstacle in obstacles:
        obstacle.move()
        if obstacle.cactus_x < -5:
            obstacles.remove(obstacle)
            obstacles.append(Cactus())

    dino.apply_movement(user_input)
    for obstacle in obstacles:
        if obstacle.collision_control(dino):
             print("player died")
             quit()

    ground.move()





if __name__ == "__main__":
    main()
