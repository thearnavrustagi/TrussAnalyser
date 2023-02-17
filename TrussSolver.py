from truss import Truss
import sys
from random import randint
import numpy as np
from geometry import Point


def solve_truss(truss_path):
    truss = Truss(truss_path, scale=150)
    truss = truss.balance(3000)
    print(
        f"External Force : {int(abs(truss.external_forces[truss.FORCE_NAME].magnitude))} N"
    )

    for i, line in enumerate(truss.rods):
        print(f"Tension in rod {i+1} : {int(abs(force.magnitude))} N")
