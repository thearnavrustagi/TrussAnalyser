import numpy as np
from geometry import Point


class Force:
    """
    name       : name of the force
    acting_on  : the point the force is acting on

    components : components of the force
    magnitude  : the magnitude of the force
    direction  : the unit vector depicting the direction of the force
    """

    def __init__(self, name: str, point: Point, magnitude=1, from_components=False):
        self.name = name
        self.acting_on = point

        if from_components:
            self.components = point.location
            self.magnitude = np.linalg.norm(point.location)
            self.calculate_direction()
            self.components = tuple(
                map(lambda x, y: x * y, self.direction, (magnitude, magnitude))
            )
        else:
            self.magnitude = magnitude
            self.direction = point.location
            self.calculate_components()

    def calculate_components(self):
        l = []
        for i in self.direction:
            l.append(i * self.magnitude)
        self.components = tuple(l)
        return self.components

    def calculate_direction(self):
        l = []
        for i in self.components:
            l.append(i / self.magnitude)
        self.direction = tuple(l)
        return self.direction

    def get_relative_endpoint(self):
        return tuple(map(lambda x, y: x + y, self.acting_on.location, self.components))

    def set_magnitude(self, value: int):
        self.magnitude = value
        self.calculate_components()

    def negate (self,name:str,acting_on:str):
        return Force(name,Point(acting_on,(-1*self.direction[0],-1*self.direction[1])))

    def __str__(self):
        return f"{self.name}, acting on {self.acting_on.name}, components: {self.components} and dir : {self.direction}, mag : {self.magnitude}"
