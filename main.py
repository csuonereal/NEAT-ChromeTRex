import pygame
import neat
from constants import *
from dinosaur import *
from ground import *
from cactus import *
import pickle



def draw_screen(dinos,obstacles,ground,score,gen):
    GAME.fill(WHITE)
    ground.draw()
    for obstacle in obstacles:
        obstacle.draw()
    for dino in dinos:
        dino.draw()
    draw_score(score,gen,dinos)

def main(genomes,config):

    global SCORE, GEN
    SCORE  = 0
    GEN += 1

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
        if SCORE >= 1000: 
            break
        draw_screen(dinos,obstacles,ground,SCORE,GEN)
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
    winner = population.run(main,50)
    print('\nBest genome:\n{!s}'.format(winner))



    with open("winner.pkl", "wb") as f:
        pickle.dump(winner, f)
        f.close()


def replay_genome(config_path, genome_path="winner.pkl"):
    # Load requried NEAT config
    config = neat.config.Config(neat.DefaultGenome, 
                                neat.DefaultReproduction, 
                                neat.DefaultSpeciesSet, 
                                neat.DefaultStagnation, config_path)

    # Unpickle saved winner
    with open(genome_path, "rb") as f:
        genome = pickle.load(f)

    # Convert loaded genome into required data structure
    genomes = [(1, genome)]

    # Call game with only the loaded genome
    main(genomes, config)




if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"neatconf.txt")
    run(config_path)
    #replay_genome(config_path)
