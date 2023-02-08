import pygame
from truss import Truss
import sys
from random import randint

pygame.init()

size = width, height = 1960, 1080
center = (width//3,height//4)
background = (0, 0, 0)
truss_path = "./truss.spec"
force_color = "#ffffff"  # (randint(0,255),randint(0,255),randint(0,255))
compression = "#00bb88"
elongation = "#ff0000"

screen = pygame.display.set_mode(size)


def __render(at=center):
    global screen
    truss = Truss(truss_path,scale=500)
    print(truss)
    clock = pygame.time.Clock()
    scale = 1
    while True:
        if pygame.QUIT in pygame.event.get():
            sys.exit()
        clock.tick(5)
        new_truss = truss.balance(scale)
        screen.fill(background)
        render_truss(new_truss,at)
        pygame.display.update()
        scale += 1

def add (t1,t2):
    return tuple(map(lambda x,y:x+y,t1,t2))

def render_truss(truss,at):
    global compression, elongation
    for line in truss.rods:
        color = compression if line.tensions[0].magnitude > 0 else elongation
        pygame.draw.line(
            screen, color, add(line.edges[0].location,at), add(line.edges[1].location,at)
        )
    for _, force in truss.forces.items():
        color = force_color
        if force.name[0] == "R": color = "#0088ff"
        pygame.draw.line(
            screen, color, add(force.acting_on.location,at), add(force.get_relative_endpoint(),at)
        )

if __name__ == "__main__":
    __render()
