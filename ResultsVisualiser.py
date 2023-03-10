import pygame
from truss import Truss
import sys
from random import randint
import numpy as np
from math import atan2, degrees, pi, sin, cos, radians
from geometry import Point
from utils import *

background = (0, 0, 0)
truss_path = "./truss.truss"
for a in sys.argv:
    if a.endswith(".truss"):
        truss_path = a
force_color = "#ffffff"  # (randint(0,255),randint(0,255),randint(0,255))
compression = pygame.image.load("./assets/compression.png")
elongation = pygame.image.load("./assets/elongation.png")
neutral = pygame.image.load("./assets/neutral.png")
joint = pygame.image.load("./assets/joint.png")
tension = pygame.image.load("./assets/tension.png")
reaction = pygame.image.load("./assets/reaction.png")
external = pygame.image.load("./assets/external.png")
font = pygame.font.Font("./assets/font.ttf", 24)
screen = pygame.display.set_mode(size)


def visualise_results(at=center):
    global screen
    truss = Truss(truss_path)
    clock = pygame.time.Clock()
    scale = 1
    new_truss = truss.balance(1)
    refactor_truss(new_truss)
    while True:
        if pygame.QUIT in pygame.event.get():
            sys.exit()
        clock.tick(60)
        screen.fill(background)
        render_truss(new_truss, at)
        pygame.display.update()
        scale += 1


def add(t1, t2):
    return tuple(map(lambda x, y: x + y, t1, t2))


def refactor_truss(truss):
    points = []
    for _, point in truss.points.items():
        points.append(point.location[1])
    max_point = max(points)
    for key, pts in truss.points.items():
        truss.points[key].location = (pts.location[0], max_point - pts.location[1])
    for _, force in truss.forces.items():
        force.refactor()


def render_truss(truss, at):
    global compression, elongation
    forces = []
    for _, value in truss.external_forces.items():
        # print(value)
        forces.append((value, external))
    for i, line in enumerate(truss.rods):
        A, B = line.edges[0], line.edges[1]
        A, B = A.location, B.location
        center = ((A[0] + B[0]) // 2, (A[1] + B[1]) // 2)
        image = None
        if line.tensions[0].magnitude > 0:
            image = compression.copy()
        else:
            image = elongation.copy()
        if abs(line.tensions[0].magnitude) < 1:
            image = neutral.copy()
        C = np.subtract(B, A)
        width = np.linalg.norm(tuple(C))
        angle = degrees(atan2(-C[1], C[0]) if C[0] else pi / 2)
        x, y = A[0] if A[0] < B[0] else B[0], A[1] if A[1] < B[1] else B[1]
        image = pygame.transform.scale(image, (width, 64))
        image = pygame.transform.rotate(image, angle)
        loc = np.subtract((x, y), (32, 32))
        screen.blit(image, np.add(loc, at))
    for name, point in truss.points.items():
        rect = pygame.Rect(np.add((at[0] - 48, at[1] - 48), point.location), (96, 96))
        if rect.collidepoint(pygame.mouse.get_pos()):
            for force in point.forces:
                if abs(force.magnitude) < 1:
                    continue
                if force.name[0] != "R":
                    forces.append((force, tension.copy()))
                else:
                    forces.append((force, reaction.copy()))
        screen.blit(joint, np.add(point.location, (at[0] - 48, at[1] - 48)))

    forces = forces[::-1]
    for force, image in forces:
        # print(force)
        A = force.acting_on.location
        if force.name[0] == "R":
            force.invert()
        magnitude = np.log2(abs(force.magnitude)) / np.log2(1.2)
        x = 160 * force.direction[0]  # + np.log2(magnitude))*force.direction[0]
        y = 160 * force.direction[1]  # + np.log2(magnitude))*force.direction[1]
        B = np.add(A, (x, y))
        C = force.components
        angle = degrees(
            atan2(-C[1], C[0]) if C[0] else (-pi / 2 if C[1] > 0 else pi / 2)
        )
        x, y = A[0] if A[0] < B[0] else B[0], A[1] if A[1] < B[1] else B[1]
        #        image = pygame.transform.scale(image,(64,96))
        image = pygame.transform.rotate(image, (-90 + angle))
        loc = np.subtract(
            (x, y), (abs(80 * sin(radians(angle))), abs(80 * cos(radians(angle))))
        )
        screen.blit(image, np.add(loc, at))

    if "--visual" in sys.argv or "-v" in sys.argv:
        render_text(truss, at)


def render_text(truss, at):
    for name, point in truss.points.items():
        text = font.render(name, True, "#ffffff")
        textRect = text.get_rect()
        __at = np.subtract(at, (8, 16))
        screen.blit(text, np.add(__at, point.location))

    y = 64
    __y = 0
    for _, value in truss.external_forces.items():
        # print(value)
        text = font.render(
            f"External Force : {int(abs(value.magnitude))} N", True, "white"
        )
        screen.blit(text, (32, __y))
        __y += 32

    y = y + __y

    for i, line in enumerate(truss.rods):
        A, B = line.edges[0], line.edges[1]
        A, B = A.location, B.location
        center = ((A[0] + B[0]) // 2, (A[1] + B[1]) // 2)
        text = font.render(str(i + 1), True, "white")
        textRect = text.get_rect()
        screen.blit(text, np.add(center, (at[0] - 8, at[1] - 16)))

        force = truss.forces[f"T{i+1}1"]
        text = font.render(
            f"Tension in rod {i+1} : {int(abs(force.magnitude))} N", True, "white"
        )
        screen.blit(text, (32, y))
        y += 32

    y += 32
    for _, value in truss.forces.items():
        if value.name[0] == "R":
            text = font.render(
                f"Reaction {value.name} : {int(abs(value.magnitude))} N", True, "white"
            )
            screen.blit(text, (32, y))
            y += 32
