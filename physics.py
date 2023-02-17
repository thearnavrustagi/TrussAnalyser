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

    def __init__(
        self,
        name: str,
        point: Point,
        dimension: int,
        magnitude: float = 1,
        from_components: bool = False,
    ):
        self.name = name
        self.dimension = dimension
        assert dimension == len(point.location)
        self.acting_on = point

        if from_components:
            self.components = point.location
            self.magnitude = np.linalg.norm(point.location)
            self.calculate_direction()
            self.INITIAL_DIRECTION = self.direction
            print(self)
        else:
            self.magnitude = magnitude
            self.direction = point.location
            self.INITIAL_DIRECTION = self.direction
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
        self.calculate_direction()

    def negate(self, name: str, acting_on: str):
        return Force(
            name, Point(acting_on, (-1 * self.direction[0], -1 * self.direction[1]))
        )

    def invert(self):
        self.direction = tuple(-e for e in self.direction)
        self.components = tuple(e for e in self.components)

    def refactor(self):
        self.components = (self.components[0], -self.components[1])
        self.direction = (self.direction[0], -self.direction[1])

    def __str__(self):
        return f"{self.name}, acting on {self.acting_on.name}, components: {self.components} and dir : {self.direction}, mag : {self.magnitude}"
