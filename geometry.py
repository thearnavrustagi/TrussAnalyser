from math import sqrt
from algebra import Equation
import numpy as np


class Point:
    def __init__(self, name: str, location: tuple):
        self.name = name
        self.location = location
        self.lines = []
        self.equation = {"X": Equation(), "Y": Equation()}
        self.forces = []

    def __str__(self):
        return f"{self.name} : {self.location}, lines : {len(self.lines)}, forces : {len(self.forces)}"

    def __get_item__(self, key):
        return self.location[key]

    def form_equation(self):
        forces = self.forces.copy()[:]
        self.equation = {"X": Equation([], []), "Y": Equation([], [])}
        for force in forces:
            self.equation["X"].add(force.components[0], force.name)
            self.equation["Y"].add(force.components[1], force.name)

        return self.equation

    def __sub__(self, other):
        return Point("", tuple(map(lambda x, y: x - y, self.location, other.location)))


class Line:
    def __init__(self, a: Point, b: Point,number:int=-1):
        self.number = number
        self.edges = (a, b)
        self.center = tuple(map(lambda x, y: (x + y) / 2, a.location, b.location))
        self.length = np.linalg.norm(
            tuple(map(lambda x, y: x - y, a.location, b.location))
        )
        """
        these forces act relative to the
        center of the line
        """
        self.tensions = []
        self.tension_equation = Equation()

    def __str__(self):
        return f"from {self.edges[0].name} to {self.edges[1].name}, tensions: {len(self.tensions)}"

    def __get_item__(self, key):
        return self.edges[key]

    def form_tension_equations(self):
        self.tension_equation = Equation()
        self.tension_equation.add(-1,self.tensions[0].name)
        self.tension_equation.add(1,self.tensions[1].name)

