import sys
import os
import neat
import pygame
import pickle
import time
from AIdrivesCar import Car
track = pygame.image.load('track.png')
width, height = track.get_width(), track.get_height()
window = pygame.display.set_mode((width, height))
finish = pygame.image.load('finish.png')
ef = pygame.font.SysFont("comicsans", 50)

def runTheGame():
    laps = 0
    ld = 0
    pygame.init()
    car = Car()
    neuralNetwork = pickle.load(open('winner.pkl', 'rb'))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        start = time.time()
        output = neuralNetwork.activate(car.get_data())
        choice = output.index(max(output))
        if choice == 0:
            car.angle += 10
        elif choice == 1:
            car.angle -= 10

        if (car.position[0] > 501 and car.position[0] < 505) and (car.position[1] > 672 and car.position[1] < 677):
            if ld == 0:
                ld = 1
                laps += 1
                print(car.position)
            
        if car.is_alive():
            car.update(track)
        else:
            end = time.time()
            while True:
                car.collisionScreen(end-start)
            
        window.blit(track, (0, 0))
        window.blit(finish, (600, 670))
        car.drawWithoutRadar(window)
        scoreLabel = ef.render("Laps: "+str(laps),1,(0,0,255))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 80, 540))
        pygame.display.flip()
        clock.tick(200)
        
        if car.position[0] > 505:
            ld = 0