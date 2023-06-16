
import pygame
from running import runSim
from AIdrivesCar import Car
from trainedModelPlays import runTheGame

if __name__ == "__main__":
    
    runSim()
    car = Car()
    value = True
    while value:
        car.reset()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                value = False
                break
    pygame.display.update()
    while True:
        runTheGame()
    
    