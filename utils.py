from math import *
from geometry import Line, Point

size = (width, height) = 1960, 1080
center = (width // 2.5, height // 4)


def join_points(words: list):
    points = words[0].split("-")
    if len(points) != 2:
        raise Exception("There should only be 2 points")
    return tuple(points)


def initialise_points(words: list, scale: int, dimension: int):
    points = eval(words[1])
    l = []
    for point in points:
        l.append(point * scale)
    assert len(l) == dimension
    return Point(words[0], tuple(l), dimension)
