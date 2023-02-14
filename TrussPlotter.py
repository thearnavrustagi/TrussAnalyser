import pygame
from truss import Truss
import sys
from random import randint
import numpy as np
from math import atan2, degrees, pi, sin, cos, radians
from geometry import Point

pygame.init()

size = width, height = 1960, 1080
center = (width//4,height//5)
background = (0, 0, 0)
truss_path = "./truss.truss"
for a in sys.argv:
    if a.endswith(".truss"): truss_path = a
force_color = "#ffffff"  # (randint(0,255),randint(0,255),randint(0,255))
compression = pygame.image.load("./assets/compression.png")
elongation = pygame.image.load("./assets/elongation.png")
neutral = pygame.image.load("./assets/neutral.png")
joint = pygame.image.load("./assets/joint.png")
tension = pygame.image.load("./assets/tension.png")
reaction = pygame.image.load("./assets/reaction.png")
external = pygame.image.load("./assets/external.png")
font = pygame.font.Font("./assets/font.ttf",24)

screen = pygame.display.set_mode(size)

def plot_truss(at=center):
    global screen
    truss = Truss(truss_path,scale=250)
    print(truss)
    clock = pygame.time.Clock()
    scale = 1
    while True: 
        if pygame.QUIT in pygame.event.get():
            sys.exit()
        clock.tick(24)
        screen.fill(background)
        render_truss(truss,at)
        pygame.display.update()
        scale += 1

def add (t1,t2):
    return tuple(map(lambda x,y:x+y,t1,t2))

def render_truss(truss,at):
    global compression, elongation
    forces = [(truss.external_forces[truss.FORCE_NAME],external)]
    for i,line in enumerate(truss.rods):
        A, B = line.edges[0], line.edges[1]
        A, B = A.location, B.location
        center = ((A[0]+B[0])//2,(A[1]+B[1])//2)
        image = neutral.copy()
        C=np.subtract(B,A)
        width = np.linalg.norm(tuple(C))
        angle = degrees(atan2(-C[1],C[0]) if C[0] else pi/2)
        x,y = A[0] if A[0] < B[0] else B[0], A[1] if A[1] < B[1] else B[1]
        image=pygame.transform.scale(image,(width,64))
        image = pygame.transform.rotate(image,angle)
        loc = np.subtract((x,y),(32,32))
        screen.blit(image,np.add(loc,at))
    for name,point in truss.points.items():
        rect=pygame.Rect(np.add((at[0]-48,at[1]-48),point.location),(96,96))
        if rect.collidepoint(pygame.mouse.get_pos()):
            for force in point.forces:
                if abs(force.magnitude) < 1: continue
                if force.name[0] != "R":
                    forces.append((force,tension.copy()))
                else:
                    forces.append((force,reaction.copy()))
        screen.blit(joint,np.add(point.location,(at[0]-48,at[1]-48)))


    forces.append(forces[0])
    del forces[0]
    for force,image in forces:
        A = force.acting_on.location
        magnitude = np.log2(abs(force.magnitude))/np.log2(1.2)
        x=160*force.direction[0]#+ np.log2(magnitude))*force.direction[0]
        y=160*force.direction[1]#+ np.log2(magnitude))*force.direction[1]
        B = np.add(A,(x,y))
        C=force.components
        angle = degrees(atan2(-C[1],C[0]) if C[0] else (-pi/2 if C[1] > 0 else pi/2))
        x,y = A[0] if A[0] < B[0] else B[0], A[1] if A[1] < B[1] else B[1]
#        image = pygame.transform.scale(image,(64,96))
        image = pygame.transform.rotate(image,(-90+angle))
        loc = np.subtract((x,y),(abs(80*sin(radians(angle))),abs(80*cos(radians(angle)))))
        screen.blit(image,np.add(loc,at))

    if "--visual" in sys.argv or "-v" in sys.argv:
        render_text(truss,at)

def render_text(truss,at):
    for name, point in truss.points.items():
        text = font.render(name,True,"#ffffff")
        textRect = text.get_rect()
        __at = np.subtract(at,(8,16))
        screen.blit(text,np.add(__at,point.location))

    y = 64
    text = font.render(f"External Force : 0 N",True,"white")
    screen.blit(text,(32,0))
    for i, line in enumerate(truss.rods):
        A, B = line.edges[0], line.edges[1]
        A, B = A.location, B.location
        center = ((A[0]+B[0])//2,(A[1]+B[1])//2)
        text = font.render(str(i+1),True,"white")
        textRect = text.get_rect()
        screen.blit(text,np.add(center,(at[0]-8,at[1]-16)))

        force = truss.forces[f"T{i+1}1"]
        text = font.render(f"Tension in rod {i+1} : 0 N",True,"white")
        screen.blit(text,(32,y))
        y += 32
        
