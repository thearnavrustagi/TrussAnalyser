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

    def __init__(self, path: str, scale: int = 200,FORCE_NAME:str="F"):
        self.fpath = path
        self.rods = []
        self.points = {}
        self.forces = {}
        self.external_forces = {}
        self.scale = scale
        self.FORCE_NAME = FORCE_NAME
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
                return self.rods.append(utils.join_points(words))
            case 2:
                pt = utils.initialise_points(words, self.scale)
                self.points[pt.name] = pt
            case 3:
                force_pt = utils.initialise_points(words[1:], 1)
                self.forces[words[0]] = Force(words[0], force_pt)
            case 4:
                if words[0] == "~":
                    force_pt = utils.initialise_points(words[2:], 1)
                    self.forces[words[1]] = Force(words[1], force_pt)
                    self.external_forces[words[1]] = self.forces[words[1]]
                    self.FORCE_NAME = words[1]
        if len(words) == 1:
            utils.join_points(words)

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
            line = Line(self.points[line[0]], self.points[line[1]])
            diff = line.edges[0] - line.edges[1]
            diff.name = line.edges[1].name
            line.tensions.append(Force(f"T{i+1}1", diff, from_components=True))
            diff = line.edges[1] - line.edges[0]
            diff.name = line.edges[0].name
            line.tensions.append(Force(f"T{i+1}2", diff, from_components=True))
            for tension in line.tensions:
                self.forces[tension.name] = tension
            lines.append(line)
            line.form_tension_equations()
            line.edges[0].lines.append(line)
            line.edges[1].lines.append(line)

        self.rods = lines
        #print("rods",self.rods)
        for key, force in self.forces.items():
            force.acting_on = self.points[force.acting_on.name]
            self.points[force.acting_on.name].forces.append(force)

    def balance(self, force_scale=1):
        truss = self.copy()
        truss.update_forces(force_scale)
        equations = truss.form_point_equations()
        forces = [force for force in self.forces]
        solution=solve(equations, forces,force_scale)
        truss.model_on_solution(solution,forces)
        #print("solution",solution)
        return truss

    def copy(self):
        return Truss(self.fpath)

    def update_forces(self, force_scale):
        return
        #print(force_scale)
        for key in self.external_forces:
            self.forces[key].set_magnitude(force_scale)

    def model_on_solution(self,solution,forces):
        for i,force_name in enumerate(forces):
            self.forces[force_name].set_magnitude(solution[i])


    def form_point_equations(self):
        equations = [Equation([1],[self.FORCE_NAME])]
        for _, point in self.points.items():
            equation = point.form_equation()
            equations.append(equation["X"])
            equations.append(equation["Y"])
        for i,line in enumerate(self.rods):
            equations.append(line.tension_equation)
        #print("\n".join([str(i) for i in equations]))
        return equations
