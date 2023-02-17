import utils
from geometry import Line
from physics import Force
from algebra import solve, Equation


class Truss:
    """
    instance variables:
    fpath  : the file path of the specification file for the truss
    lines  : a list of the rods in the truss
    points : a list of all the points in the truss
    forces : a list of all the forces in the truss
    scale  : scale of the truss in the diagram
    """

    def __init__(self, path: str, scale: int = 125, dimension: int = 2):
        self.fpath = path
        self.dimension = dimension
        self.rods = []
        self.points = {}
        self.forces = {}
        self.external_forces = {}
        self.scale = scale
        self.__initialise_from_specfile()
        self.__link_all()

    def __initialise_from_specfile(self):
        with open(self.fpath) as file:
            lines = file.read().splitlines()
            for line in lines:
                self.__interpret(line)

    def __interpret(self, line):
        words = line.strip().split()
        match len(words):
            case 0:
                return
            case 1:
                self.rods.append(utils.join_points(words))
                return
            case 2:
                if words[0][0] == "#":
                    if words[0].upper() == "#DIM":
                        self.dimension = int(words[1])
                        return
                pt = utils.initialise_points(
                    words, self.scale, dimension=self.dimension
                )
                self.points[pt.name] = pt
            case 3:
                force_pt = utils.initialise_points(
                    words[1:], 1, dimension=self.dimension
                )
                self.forces[words[0]] = Force(
                    words[0], force_pt, dimension=self.dimension
                )
            case 4:
                if words[0] == "~":
                    force_pt = utils.initialise_points(
                        words[2:], 1, dimension=self.dimension
                    )
                    self.forces[words[1]] = Force(
                        words[1],
                        force_pt,
                        dimension=self.dimension,
                        from_components=True,
                    )
                    self.external_forces[words[1]] = self.forces[words[1]]

    def __str__(self):
        s = (
            """
points :\n"""
            + "\n".join([str(p[1]) for p in self.points.items()])
            + """
lines  :\n"""
            + "\n".join([str(l) for l in self.rods])
            + """
forces :\n"""
            + "\n".join([str(f[1]) for f in self.forces.items()])
            + """
        """
        )
        return s

    def __link_all(self):
        lines = []
        for i, line in enumerate(self.rods):
            line = Line(
                self.points[line[0]],
                self.points[line[1]],
                number=i,
                dimension=self.dimension,
            )
            diff = line.edges[0] - line.edges[1]
            diff.name = line.edges[1].name
            line.tensions.append(
                Force(f"T{i+1}1", diff, from_components=True, dimension=self.dimension)
            )
            diff = line.edges[1] - line.edges[0]
            diff.name = line.edges[0].name
            line.tensions.append(
                Force(f"T{i+1}2", diff, from_components=True, dimension=self.dimension)
            )
            for tension in line.tensions:
                self.forces[tension.name] = tension
            lines.append(line)
            line.form_tension_equations()
            line.edges[0].lines.append(line)
            line.edges[1].lines.append(line)

        self.rods = lines
        # print("rods",self.rods)
        for key, force in self.forces.items():
            force.acting_on = self.points[force.acting_on.name]
            self.points[force.acting_on.name].forces.append(force)

    def balance(self, force_scale=1):
        truss = self.copy()
        truss.update_forces(force_scale)
        equations = truss.form_point_equations()
        forces = self.forces.copy()
        # print('\n'.join([str(i) for i in equations]),forces)
        values = []
        for _, force in self.external_forces.items():
            values.append(force.magnitude * force_scale)
        solution = solve(equations, forces, values)
        # print(solution)
        truss.model_on_solution(solution, forces)
        # print("solution",solution)
        return truss

    def copy(self):
        return Truss(self.fpath)

    def update_forces(self, force_scale):
        return
        # print(force_scale)
        for key in self.external_forces:
            self.forces[key].set_magnitude(force_scale)

    def model_on_solution(self, solution, forces):
        for i, force_name in enumerate(forces):
            self.forces[force_name].set_magnitude(solution[i])

    def form_point_equations(self):
        equations = []
        # print("extforces",self.external_forces)
        for key in self.external_forces:
            # print("forming point equations",key)
            equations.append(Equation([1], [key]))
            # print(equations[0])
        for _, point in self.points.items():
            equation = point.form_equation()
            # print(equation)
            # print("NEW EQUATION")
            for i in equation:
                if len(equation) == 0:
                    continue
                # print(i)
                equations.append(i)
        for i, line in enumerate(self.rods):
            equations.append(line.tension_equation)
        # print("\n".join([str(i) for i in equations]))
        return equations
