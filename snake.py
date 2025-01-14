import pygame
from pygame.locals import *

WINDOWS_WIDTH = 600
WINDOWS_HEIGHT = 600

pygame.init()

window = pygame.display.set_mode((WINDOWS_WIDTH,WINDOWS_HEIGHT))

while True:
    window.fill((72,61,139))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()