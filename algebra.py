import numpy as np

class Equation:
    def __init__(self, coeff: list = list(), var: list = list()):
        self.coeffecients = coeff[:]
        self.variables = var[:]

    def add(self, coeffecient, variable):
        self.coeffecients.append(coeffecient)
        self.variables.append(variable)

    def __str__(self):
        s = ""
        for coeff, var in zip(self.coeffecients, self.variables):
            s += str(coeff) + "x" + str(var) + " + "
        return s[:-3]


def solve(equations: list, forces: list,fval:int):
    matrix = form_matrix(equations, forces)
    print(tuple(enumerate(forces)))
    RHS=np.transpose([fval]+[0]*(len(matrix)-1))
    print("RHS",RHS)
    return np.linalg.solve(matrix,RHS)


def form_matrix(equations: list, forces: list):
    matrix = []
    for _ in range(len(forces)):
        matrix.append([0] * len(forces))
    
    if len(equations) >= len(forces):
        equations = equations[:len(forces)]
    else:
        pass
        #raise Exception(f"number of equations: {len(equations)}, number of variables: {len(forces)}")


    for i, force in enumerate(forces):
        for j,equation in enumerate(equations):
            for coeff,var in zip(equation.coeffecients,equation.variables):
                if var == force:
                    matrix[j][i] = coeff

    print(matrix)
    print("\n".join([" ".join([str(e) for e in row]) for row in matrix]))
    return matrix
