# Purpose: Class for Max-2-Sat solver.

from satinstance import Max2Sat
from encoder import max2sat_to_sdp
from sdpsolver import SDPSpherical
import numpy as np
from typing import *
from random import *

def random_solver(sat: Max2Sat, n_trial) -> List[int]:
    """tries n_trial random assignments and returns the best one"""

    n = sat.get_n()

    best_sol = None
    max_clause_sat = -1

    for _ in range(n_trial):
        sol = (np.random.randint(2, size=n) * 2 - 1) * np.arange(1, n + 1)
        clause_sat = sat.eval(sol)

        if clause_sat > max_clause_sat:
            max_clause_sat = clause_sat
            best_sol = np.copy(sol)

    return list(best_sol)


def sdp_relaxation_solver(sat: Max2Sat, n_trial) -> List[int]:
    """tries n_trial random assignments and returns the best one"""

    n = sat.get_n()
    W, _, _ = max2sat_to_sdp(sat)
    sdp_solver = SDPSpherical(W)

    X = sdp_solver.solve()
    Y = np.linalg.cholesky(X)

    best_sol = []
    max_clause_sat = -1

    for _ in range(n_trial):
        rand_unit_v = np.random.rand(n + 1)
        rand_unit_v = rand_unit_v / np.linalg.norm(rand_unit_v)

        random_proj = np.dot(Y, rand_unit_v).reshape((-1, 1))
        # print(random_proj.shape)

        sol = []
        for i in range(1, n + 1):
            if random_proj[0] * random_proj[i] > 0:
                sol.append(i)
            else:
                sol.append(-i)

        clause_sat = sat.eval(sol)

        if clause_sat > max_clause_sat:
            max_clause_sat = clause_sat
            best_sol = np.copy(sol)
    return best_sol

if __name__ == "__main__":
    n = 50
    sat = Max2Sat(n)
    m = 200
    mcnt = m

    while mcnt > 0:
        a, b = randint(1, n), randint(1, n)
        if a == b:
            continue
        mcnt -= 1
        asign, bsign = randint(0, 1) * 2 - 1, randint(0, 1) * 2 - 1
        sat.add_clause(asign * a, bsign * b)

    print("Random solver: ", sat.eval(random_solver(sat, 100)), sep="")

    print("SDP solver: ", sat.eval(sdp_relaxation_solver(sat, 100)), sep="")
