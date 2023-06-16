import math
import pygame

carX = 100   
carY = 100
track = pygame.image.load('track.png')
finish = pygame.image.load('finish.png')
width, height = track.get_width(), track.get_height()
window = pygame.display.set_mode((width, height))
pygame.font.init()
sf = pygame.font.SysFont("comicsans", 50)
ef = pygame.font.SysFont("comicsans", 50)

current_generation = 0

class Car:

    def __init__(self):
        self.carImage = pygame.transform.scale(pygame.image.load('car.png'), (carX, carY))
        self.rotatedCarImage = self.carImage 

        self.position = [500, 670]
        self.angle = 0
        self.speed = 0

        self.center = [self.position[0] + carX / 2, self.position[1] + carY / 2]

        self.radars = []
        self.drawing_radars = []

        self.alive = True

        self.distance = 0
        self.time = 0

    def draw(self, screen):
        screen.blit(self.rotatedCarImage, self.position)
        self.draw_radar(screen)
        
    def drawWithoutRadar(self, screen):
        screen.blit(self.rotatedCarImage, self.position)

    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        self.alive = True
        for point in self.corners:
            if game_map.get_at((int(point[0]), int(point[1]))) == (255,255,255,255):
                self.alive = False
                break

    def check_radar(self, degree, game_map):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)
        
        while not game_map.get_at((x, y)) == (255,255,255,255) and length < 250:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])
    
    def update(self, game_map):
        self.speed = 5

        self.rotatedCarImage = self.rotate_center(self.carImage, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(self.position[0], 20)
        self.position[0] = min(self.position[0], width - 120)

        self.distance += self.speed
        self.time += 1
        
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(self.position[1], 20)
        self.position[1] = min(self.position[1], width - 120)

        self.center = [int(self.position[0]) + carX / 2, int(self.position[1]) + carY / 2]

        length = 0.5 * carX
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        self.check_collision(game_map)
        self.radars.clear()

        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        return self.alive

    def get_reward(self):
        return self.distance / (carX/2)

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image
    
    def reset(self):
        self.position = [500, 670]
        self.is_alive = True
        window.blit(track, (0, 0))
        window.blit(finish, (600, 670))
        window.blit(self.rotatedCarImage, self.position)
        pygame.draw.rect(window, (0,0,0), pygame.Rect(450, 150, 500, 500))
        pygame.draw.rect(window, (0, 255, 0), pygame.Rect(450, 150, 500, 500), 2)
        scoreLabel = ef.render("AI Trained!",1,(0,255,0))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 510, 250))
        scoreLabel = ef.render("Press any key",1,(0,255,0))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 510, 350))
        scoreLabel = ef.render("to continue.",1,(0,255,0))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 510, 450))
        pygame.display.update()
        
    def collisionScreen(self, time):
        self.position = [500, 670]
        self.is_alive = True
        window.blit(track, (0, 0))
        window.blit(finish, (600, 670))
        window.blit(self.rotatedCarImage, self.position)
        pygame.draw.rect(window, (0,0,0), pygame.Rect(450, 150, 500, 500))
        pygame.draw.rect(window, (0, 255, 0), pygame.Rect(450, 150, 500, 500), 2)
        scoreLabel = ef.render("AI collided",1,(0,255,0))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 510, 250))
        scoreLabel = ef.render("Time elapsed:-",1,(0,255,0))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 510, 350))
        scoreLabel = ef.render(str("%.2f"%time),1,(0,255,0))
        window.blit(scoreLabel, (width - scoreLabel.get_width() - 510, 450))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                quit()
        
    def getPos(self):
        return self.position
