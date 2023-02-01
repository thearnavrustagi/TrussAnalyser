from math import *
from geometry import Line, Point

def join_points (words):
    points = words[0].split('-')
    if len(points) != 2: raise Exception("There should only be 2 points")
    return Line(points[0],points[1])

def initialise_points (words, scale):
    points = eval(words[1])
    l = []
    for point in points:
        l.append(point*scale)
    return Point(words[0],tuple(l))
