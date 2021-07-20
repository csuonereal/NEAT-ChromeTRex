import pygame
import os
import random


pygame.init()


WHITE = (255,255,255)
BLACK = (0,0,0)

FPS = 30

GAME_WIDTH = 1100
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


LARGE_CACTUS = [pygame.image.load(os.path.join("imgs","Cactus","LargeCactus1.png")),
                pygame.image.load(os.path.join("imgs","Cactus","LargeCactus2.png")),
                pygame.image.load(os.path.join("imgs","Cactus","LargeCactus3.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("imgs","Cactus","SmallCactus1.png")),
                pygame.image.load(os.path.join("imgs","Cactus","SmallCactus2.png")),
                pygame.image.load(os.path.join("imgs","Cactus","SmallCactus3.png"))]


GAME_SPEED = 20
ANIM_SPEED = 3


SCORE = 0
FONT = pygame.font.SysFont('comicsans', 44)

def draw_score(score):
    txt = FONT.render("Score:"+str(score), 1, BLACK)
    GAME.blit(txt, (10,10))
   

def show_assets(ground, dino, obstacles, score):
    GAME.fill(WHITE)
    ground.draw()
    for obstacle in obstacles:
        obstacle.draw()
    dino.draw()
    
    draw_score(score)

    pygame.display.update()

def main():

    run = True
    clock = pygame.time.Clock()

    ground = Ground()
    dino = Dino()
    obstacles = [Cactus()]

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        
        user_input = pygame.key.get_pressed()


        for obstacle in obstacles:
            obstacle.move()
            if obstacle.cactus_x < 0:
                obstacles.remove(obstacle)
                obstacles.append(Cactus())
        
            
     


        dino.movement_scheme(user_input)

        for obstacle in obstacles:
            if obstacle.collide(dino):
                print("player died")
                quit()

        ground.move()

        global SCORE 
        SCORE += 1
        show_assets(ground,dino,obstacles, SCORE)



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

class Dino:
    JUMP_VELOCITY = 8.5
    def __init__(self):
        self.img = DINO_RUNNING[0]
        self.img_index = 0
        self.dino_x = DINO_DEFAULT_X
        self.dino_y = DINO_DEFAULT_Y
        self.jump_velocity = self.JUMP_VELOCITY
        self.is_jumping = False
        self.is_running = True
        #self.shape = pygame.Rect(self.dino_x, self.dino_y, DINO_WIDTH, DINO_HEIGHT)
        self.shape = self.img.get_rect().move(self.dino_x, self.dino_y)


    def jump(self):
        self.img = DINO_JUMP
        self.img_index = 0
        if self.is_jumping:
            self.dino_y -= self.jump_velocity * 4
            self.shape.y = self.dino_y
            self.jump_velocity -= 0.8
        if self.jump_velocity < - self.JUMP_VELOCITY:
            self.is_jumping = False
            self.jump_velocity = self.JUMP_VELOCITY
       

         
    
    def run(self):
        self.dino_y = DINO_DEFAULT_Y
        self.dino_x = DINO_DEFAULT_X

    def movement_scheme(self,inp):
        if self.is_jumping:
            self.jump()
        if self.is_running:
            self.run()

        if inp[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.is_running = False

        elif not self.is_jumping:
            self.is_running = True
            self.is_jumping = False


        #elif not (inp[pygame.K_SPACE]):
         
       

    def animate(self):
        self.img_index += 1
        if self.img_index <= ANIM_SPEED:
            self.img = DINO_RUNNING[0]
        elif self.img_index <= ANIM_SPEED*2:
            self.img = DINO_RUNNING[1]
        elif self.img_index <= ANIM_SPEED*3:
            self.img_index = DINO_RUNNING[0]
            self.img_index = 0

        
            

        GAME.blit(self.img, (self.shape.x, self.shape.y))


    def draw(self):
        self.animate()

   
       

class Cactus:
    def __init__(self):
        self.cactus_x = GAME_WIDTH
        self.cactus_y = GROUND_DEFAULT_Y - 70
        self.passed = False
        self.generate_random_cactus()
    def generate_random_cactus(self):
        self.type = random.randint(0,1)
        if self.type == 0:
            self.large_scale = random.randint(0,2)
            self.cactus_y = self.cactus_y + 40
            self.img = SMALL_CACTUS[self.large_scale]
            self.shape = self.img.get_rect().move(self.cactus_x, self.cactus_y)
        elif self.type == 1:
            self.large_scale = random.randint(0,2)
            self.img = LARGE_CACTUS[self.large_scale]
            self.shape = self.img.get_rect().move(self.cactus_x, self.cactus_y)

    def move(self):
        self.cactus_x -= GAME_SPEED
        self.shape.x = self.cactus_x


    def collide(self,dino):
        if self.shape.colliderect(dino.shape):
            return True

        else:
            return False


    def draw(self):
        GAME.blit(self.img, (self.cactus_x, self.cactus_y))



if __name__ == "__main__":
    main()