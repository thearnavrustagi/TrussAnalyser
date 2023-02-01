import utils
from geometry import Line


class Truss ():
    def __init__ (self, path, scale=100):
        self.fpath = path
        self.lines = []
        self.points = {}
        self.scale = scale
        self.__initialise_from_specfile()
        self.__load()

    def __initialise_from_specfile (self):
        with open(self.fpath) as file:
            lines=file.read().splitlines()
            for line in lines:
                self.__interpret(line)

    def __interpret (self, line):
        words = line.strip().split()
        match len(words):
            case 0:
                return
            case 1:
                return self.lines.append(utils.join_points(words))
            case 2:
                pt = utils.initialise_points(words,self.scale)
                self.points[pt.name] =  pt
        if len(words) == 1:
            utils.join_points(words)

    def __str__ (self):
        s = """
        points : """+str([str(p[1]) for p in self.points.items()])+"""
        lines  : """+str([str(l) for l in self.lines])+"""
        """
        return s
    
    def __load (self):
        lines = []
        for line in self.lines:
            lines.append(Line(self.points[line.A],self.points[line.B]))
        self.lines = lines
