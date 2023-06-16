import sys
import neat
import pygame
import pickle
from AIdrivesCar import Car
track = pygame.image.load('track.png')
width, height = track.get_width(), track.get_height()
window = pygame.display.set_mode((width, height))
sf = pygame.font.SysFont("comicsans", 50)
ef = pygame.font.SysFont("comicsans", 50)
finish = pygame.image.load('finish.png')
current_generation = 0
laps = 0
nets = []
def run_simulation(genomes, config):
    
    cars = []
    genos = []
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    for i, g in genomes:
        g.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        cars.append(Car())
        genos.append(g)

    clock = pygame.time.Clock()
    game_map = pygame.image.load('track.png').convert()

    global current_generation
    current_generation += 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pickle.dump(nets[0], open('winner.pkl', 'wb'))
                sys.exit(0)

        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10
            elif choice == 1:
                car.angle -= 10
                
        still_alive = 0
        screen.blit(game_map, (0, 0))
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map)
                genos[i].fitness += 0.1
                car.draw(screen)
                if car.position[0] > 495 and car.position[0] < 505:
                    genos[i].fitness += 10
            else:
                genos[i].fitness -= 2
                cars.pop(i)
                nets.pop(i)
                genos.pop(i)

        if still_alive == 0:
            break

        scoreLabel = ef.render("Gen:"+str(current_generation),1,(0,0,255))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 130, 500))
        
        scoreLabel = ef.render("Alive:"+str(still_alive),1,(0,0,255))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 110, 580))

        pygame.display.flip()
        clock.tick(100)