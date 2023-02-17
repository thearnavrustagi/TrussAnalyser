import pygame

pygame.init()
from truss import Truss
import sys
from random import randint
import numpy as np
from math import atan2, degrees, pi, sin, cos, radians
from geometry import Point
import TrussPlotter
import ResultsVisualiser
import TrussSolver

truss_path = "./truss.truss"
for argv in sys.argv:
    if "." in argv:
        truss_path = argv

if __name__ == "__main__":
    if "-n" in sys.argv or "--no-plot" in sys.argv:
        TrussSolver.solve_truss(truss_path)
    if "-p" in sys.argv or "--plot" in sys.argv:
        TrussPlotter.plot_truss()
        sys.exit()
    ResultsVisualiser.visualise_results()
