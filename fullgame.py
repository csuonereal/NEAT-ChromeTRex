# this py file does not include ai, only game :)
import os
from random import randint
import pygame


pygame.init()
pygame.font.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

FPS = 30

GAME_WIDTH = 1750
GAME_HEIGHT = 500
GAME = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

CLOUD_IMG = pygame.image.load(os.path.join("Assets", "Other","Cloud.png"))


BIRD_IMG = [pygame.image.load(os.path.join("Assets", "Bird", "Bird1.png")),
            pygame.image.load(os.path.join("Assets","Bird","Bird2.png"))]


GROUND_IMG = pygame.image.load(os.path.join("Assets","Other","Track.png"))
GROUND_WIDTH = GROUND_IMG.get_width()
GROUND_DEFAULT_Y = GAME_HEIGHT - 100


DINO_RUNNING = [pygame.image.load(os.path.join("Assets","Dino","DinoRun1.png")),
                pygame.image.load(os.path.join("Assets","Dino","DinoRun2.png"))]

DINO_JUMP = pygame.image.load(os.path.join("Assets","Dino","DinoJump.png"))
DINO_DUCK = [pygame.image.load(os.path.join("Assets","Dino","DinoDuck1.png")),
             pygame.image.load(os.path.join("Assets","Dino","DinoDuck2.png"))]

DINO_DEAD = pygame.image.load(os.path.join("Assets","Dino","DinoDead.png"))
DINO_START = pygame.image.load(os.path.join("Assets","Dino","DinoStart.png"))

DINO_HEIGHT = DINO_JUMP.get_height()
DINO_WIDTH = DINO_JUMP.get_width()
DINO_DEFAULT_X = 200
DINO_DEFAULT_Y = GROUND_DEFAULT_Y - 60
DINO_JUMP_VELOCITY = 11.5


LARGE_CACTUS = [pygame.image.load(os.path.join("imgs","Cactus","LargeCactus1.png")),
                pygame.image.load(os.path.join("imgs","Cactus","LargeCactus2.png")),
                pygame.image.load(os.path.join("imgs","Cactus","LargeCactus3.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("imgs","Cactus","SmallCactus1.png")),
                pygame.image.load(os.path.join("imgs","Cactus","SmallCactus2.png")),
                pygame.image.load(os.path.join("imgs","Cactus","SmallCactus3.png"))]


GAME_SPEED = 35
ANIM_SPEED = 3


SCORE = 0

FONT = pygame.font.SysFont('comicsans', 44)

class Rex:
    def __init__(self):
        self.jump_velocity = 0
        self.time  = 0
        self.acceralation = 2
        self.dino_jump = False
        self.dino_duck = False
        self.dino_run = True
        self.y = DINO_DEFAULT_Y
        self.x = DINO_DEFAULT_X
        self.img = DINO_START
        self.img_count = 0
        self.shape = self.img.get_rect().move(self.x,self.y)

    def jump(self):
        if self.y == DINO_DEFAULT_Y:
            self.jump_velocity = -DINO_JUMP_VELOCITY
            self.time = 0    
            self.dino_jump = False
        
 

    def move(self):
        #displacement = velocity * time + 1/2 * acceleration * time^2
        self.time += 1
        displacement = self.jump_velocity * self.time + 0.5 * self.acceralation * self.time**2
        self.y += displacement
        

        if displacement < 0 :
            self.y -= 3
        
        if self.y >= DINO_DEFAULT_Y:
            self.y = DINO_DEFAULT_Y
  

        
        self.shape.y = self.y

    def apply_movement(self, input):
   
        if self.dino_jump:
            self.jump()
    
        self.move()     
        if input[pygame.K_UP] :
            self.key += 1
            if self.key == 1:
                self.dino_jump = True
                self.dino_run = False
                self.dino_duck = False

    
        elif input[pygame.K_DOWN] and self.y == DINO_DEFAULT_Y:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False

        elif not (self.dino_jump or input[pygame.K_DOWN]):
            self.dino_run = True
            self.dino_jump = False
            self.dino_duck = False
            self.key = 0
  
    def animate(self):
        self.img_count += 1
        if self.dino_run:
            if self.img_count <= ANIM_SPEED:
                self.img = DINO_RUNNING[0]
            elif self.img_count <= ANIM_SPEED*2:
                self.img = DINO_RUNNING[1]
            elif self.img_count <= ANIM_SPEED*3:
                self.img = DINO_RUNNING[0]
                self.img_count = 0
        if self.dino_jump:
            self.img = DINO_JUMP
            self.img_count = 0
        if self.dino_duck: 
            self.y = DINO_DEFAULT_Y + 30
            if self.img_count <= ANIM_SPEED:
                self.img = DINO_DUCK[0]
            elif self.img_count <= ANIM_SPEED*2:
                self.img = DINO_DUCK[1]
            elif self.img_count <= ANIM_SPEED*3:
                self.img = DINO_DUCK[0]
                self.img_count = 0
        self.shape = self.img.get_rect().move(self.x, self.y)
        GAME.blit(self.img, (self.x, self.y))

    def draw(self):
        self.animate()


class Bird:
    def __init__(self):
        
        self.y = randint(DINO_DEFAULT_Y - 150, DINO_DEFAULT_Y - 30)
        self.x = GAME_WIDTH
        self.img = BIRD_IMG[0]
        self.shape = self.img.get_rect().move(self.x,self.y)
        self.img_count = 0
    def move(self):
        self.x -= GAME_SPEED + 10
        self.shape.x = self.x
    def draw(self):
        self.animate()

    def collision_control(self,dino):
        if self.shape.colliderect(dino.shape):
            return True
        else:
            return False
    def animate(self):
        self.img_count += 1
        if self.img_count <= ANIM_SPEED:
            self.img = BIRD_IMG[0]
        elif self.img_count <= ANIM_SPEED*2:
            self.img = BIRD_IMG[1]
        elif self.img_count <= ANIM_SPEED*3:
            self.img = BIRD_IMG[0]
            self.img_count = 0
        self.shape = self.img.get_rect().move(self.x, self.y)
        GAME.blit(self.img, (self.x, self.y))

        


class Cloud:
    def __init__(self):
        self.y = randint(25,50)
        self.x = GROUND_WIDTH
        self.img = CLOUD_IMG

    def create_random_cloud(self):
        if self.x + self.img.get_width() < 0:
            self.y = randint(25,50)
            self.x = GROUND_WIDTH

    def move(self):
        self.x -= GAME_SPEED - 20

    def draw(self):
        self.create_random_cloud()
        GAME.blit(self.img, (self.x, self.y))
    

class Floor:
    def __init__(self):
        self.y = GROUND_DEFAULT_Y
        self.x1 = 0
        self.x2 = GROUND_WIDTH

    def move(self):
        self.x1 -= GAME_SPEED
        self.x2 -= GAME_SPEED

        if self.x1 + GROUND_WIDTH < 0:
            self.x1 = GROUND_WIDTH + self.x2
        if self.x2 + GROUND_WIDTH < 0:
            self.x2 = GROUND_WIDTH + self.x1
            

    def draw(self):
        GAME.blit(GROUND_IMG, (self.x1, self.y))
        GAME.blit(GROUND_IMG, (self.x2, self.y))
       
            
class Cactus:
    def __init__(self):
        self.x = GAME_WIDTH
        self.y = GROUND_DEFAULT_Y - 70
        self.generate_random_cactus()

    def generate_random_cactus(self):
        self.type = randint(0,1)
        if self.type == 0:
            self.cactus_amount = randint(0,2)
            self.y = self.y + 40
            self.img = SMALL_CACTUS[self.cactus_amount]
            self.shape = self.img.get_rect().move(self.x, self.y)
        elif self.type == 1:
            self.cactus_amount = randint(0,2)
            self.img = LARGE_CACTUS[self.cactus_amount]
            self.shape = self.img.get_rect().move(self.x, self.y)

    def move(self):
        self.x -= GAME_SPEED
        self.shape.x = self.x

    def collision_control(self,dino):
        if self.shape.colliderect(dino.shape):
            return True
        else:
            return False
    
    def draw(self):
        GAME.blit(self.img, (self.x, self.y))



def draw_screen(rex,floor,obstacles, cloud):
    GAME.fill(WHITE)
    floor.draw()
    rex.draw()
    cloud.draw()
    for obstacle in obstacles:
        obstacle.draw()
  
   

    pygame.display.update()

def main():

    rex = Rex()
    floor = Floor()
    bird_or_cactus = randint(0,1)
    obstacles = []
    if bird_or_cactus == 0:
        print("cac")
        obstacles = [Cactus()]
    elif bird_or_cactus == 1:
        print("bird")
        obstacles = [Bird()]
    cloud = Cloud()
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =False
                pygame.quit()
                quit()
        user_inputs = pygame.key.get_pressed()
        dino_ground_obstacle_controller(user_inputs, rex, floor, obstacles, cloud)
        draw_screen(rex,floor,obstacles, cloud)


def dino_ground_obstacle_controller(inputs, dino, ground, obstacles, cloud):
    dino.apply_movement(inputs)
    bird_or_cactus = randint(0,1)
    for obstacle in obstacles:
        obstacle.move()

        if obstacle.x < -5:
            obstacles.remove(obstacle)
            if bird_or_cactus == 0:
                obstacles.append(Cactus())
            elif bird_or_cactus == 1:
                obstacles.append(Bird())


        if obstacle.collision_control(dino):
            print("dino died")
            quit()

        ground.move()
        cloud.move()

            

if __name__ == '__main__':
    main()