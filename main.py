import pygame
import neat
from constants import *
from dinosaur import *
from ground import *
from cactus import *



def draw_screen(dinos,obstacles,ground,score):
    GAME.fill(WHITE)
    ground.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for dino in dinos:
        dino.draw()
    draw_score(score)

def main(genomes,config):

    global SCORE
    SCORE  = 0

    dinos = []
    genomes_ = [] # it will allow me to reach genomes whenever i want.
    nets = []

    ground = Ground()
    obstacles = [Cactus()]

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        dinos.append(Dino())
        genomes_.append(genome)


    clock = pygame.time.Clock()
    run = True
    while run and len(dinos) > 0:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
        user_input = pygame.key.get_pressed()
        obstacle_dino_ground_controller(obstacles,dinos,ground,nets,genomes_)

        SCORE += 1
        draw_screen(dinos,obstacles,ground,SCORE)
        pygame.display.update()


def obstacle_dino_ground_controller(obstacles,dinos,ground,nets,genomes):
    for obstacle in obstacles:
        obstacle.move()
        if obstacle.cactus_x < -5:
            obstacles.remove(obstacle)
            obstacles.append(Cactus())
    
    for index,dino in enumerate(dinos):
        genomes[index].fitness += 0.1
        dino.move()
        output = nets[index].activate((dinos[index].dino_y,
                                      abs(dinos[index].dino_x - obstacles[len(obstacles)-1].cactus_x),
                                      obstacles[len(obstacles)-1].img.get_width(),
                                     obstacles[len(obstacles)-1].img.get_height()))
        if output[0] > 0.5:
            dino.jump()  
    
    for obstacle in obstacles:
        for index,dino in enumerate(dinos):
            if obstacle.collision_control(dino):
                genomes[index].fitness -= 1
                genomes.pop(index)
                nets.pop(index)
                dinos.pop(index)

            else:
                if obstacle.cactus_x < dino.dino_x:
                    genomes[index].fitness += 5

    ground.move()





def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_file)
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    winner = population.run(main,66)
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neatconf.txt")
    run(config_path)

