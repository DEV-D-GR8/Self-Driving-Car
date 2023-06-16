
import neat
import pickle
from runGame import run_simulation, nets

def runSim():
    
    config_path = "./configList.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    population.run(run_simulation, 1000)
    
    pickle.dump(nets[0], open('winner.pkl', 'wb'))
    
    