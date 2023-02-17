import numpy as np
from math import isnan


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

    def __len__(self):
        assert len(self.coeffecients) == len(variables)
        return len(self.coeffecients)


def solve(equations: list, forces: list, fvals: list):
    matrix = form_matrix(equations, forces)
    # print(tuple(enumerate(forces)))
    RHS = np.transpose(fvals + [0] * (len(matrix) - len(fvals)))
    # print("RHS",RHS)
    try:
        a = np.linalg.solve(matrix, RHS)
        # print(a)
        return a
    except Exception as e:
        # print(e)
        return [1] * len(matrix)


def form_matrix(equations: list, forces: list):
    matrix = []
    for _ in range(len(forces)):
        matrix.append([0] * len(forces))

    if len(equations) >= len(forces):
        equations = equations[: len(forces)]
    else:
        raise Exception(
            f"number of equations: {len(equations)}, number of variables: {len(forces)}"
        )

    for i, force in enumerate(forces):
        for j, equation in enumerate(equations):
            # print(equation)
            for coeff, var in zip(equation.coeffecients, equation.variables):
                if var == force:
                    matrix[j][i] = coeff

    # print("\n".join([" ".join([str(e) for e in row]) for row in matrix]))
    return matrix
