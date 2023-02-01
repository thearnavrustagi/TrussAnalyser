import pygame
from truss import Truss
import sys

pygame.init()

size = width, height = 960, 720
background = (0,0,0)
truss_path = "./truss.spec"

screen = pygame.display.set_mode(size)

def __render():
    while True:
        if pygame.QUIT in pygame.event.get(): sys.exit()
        truss = Truss(truss_path)

        screen.fill(background)
        render_lines(truss)
        pygame.display.flip()

def render_lines(truss):
    for line in truss.lines:
        print(line.A.location)
        print(line.B.location)
        pygame.draw.line(screen, (255,255,255),line.A.location,line.B.location)
if __name__ == "__main__":
    __render()
