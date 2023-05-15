# Purpose: Class for encoding a SAT instance into a SDP problem.

from random import *

import numpy as np
from scipy import sparse
import numpy.typing as npt
from sdpinstance import SDPinstance
from satinstance import Max2Sat

from typing import *

def max2sat_to_sdp(max2sat: Max2Sat):
    n = max2sat.get_n()
    """@param: max2sat: Max2Sat, a Max-2-SAT instance
    @return: SDPinstance, an SDP instance
    """
    def encode_clause(cl: List[Union[int, int]], n: int, weight: float = 1):
        """@param: cl: tuple[int, int], a clause
        @param: n: int, number of variables
        @param: weight: float, weight of the cl ause
        @return: two dimentional n x n matrix W, tr<W, X> = weight if clause is satisfies, 0 otherwise
        """
        row = []
        col = []
        val = []

        a, b = cl
        signa = 1 if a > 0 else -1
        signb = 1 if b > 0 else -1

        absa, absb = signa * a, signb * b

        ya0 = signa / 4
        yb0 = signb / 4
        yab = -signa * signb / 4

        row = [absa ,    0,   absb,     0,  absa,  absb]
        col = [0    , absa,      0,  absb,  absb,  absa]
        val = [ya0/2, ya0/2, yb0/2, yb0/2, yab/2, yab/2]

        # print(row)
        # print(col)
        # print(val)

        matrix = -weight * sparse.coo_matrix((val, (row, col)), shape=(n + 1, n + 1))
        return matrix

    W = np.zeros((n + 1, n + 1), dtype=np.float64)
    for cl in max2sat.get_clauses():
        W += encode_clause(cl, max2sat.n)

    # print("here:")
    # print(W)

    a_list = []
    b_list = []
    for i in range(n + 1):
        a_list.append(sparse.coo_matrix(([1], ([i], [i])), shape=(n + 1, n + 1)).todense())
        b_list.append(1)

    return W, a_list, b_list

if __name__ == "__main__":
    # test with cvx
    import cvxpy as cp

    n = 20
    sat = Max2Sat(n)
    m = 100
    mcnt = m

    while mcnt > 0:
        a, b = randint(1, n), randint(1, n)
        if a == b:
            continue
        mcnt -= 1
        asign, bsign = randint(0, 1) * 2 - 1, randint(0, 1) * 2 - 1
        sat.add_clause(asign * a, bsign * b)

    X = cp.Variable((n + 1, n + 1), symmetric=True)
    constraints = [X >> 0]


    w, a_list, b_list = max2sat_to_sdp(sat)

    for a, b in zip(a_list, b_list):
        constraints.append(cp.trace(a @ X) == b)

    prob = cp.Problem(cp.Minimize(cp.trace(w @ X)), constraints)
    prob.solve()

    print("The optimal value is", prob.value)
    print("A solution X is")
    print(X.value)

    sol_rand = []
    rand_v = np.random.rand(n + 1) - 0.5
    for i in range(1, n + 1):
        if rand_v[i] > 0:
            sol_rand.append(i)
        else:
            sol_rand.append(-i)

    sol_sdp = []
    for i in range(1, n + 1):
        if X.value[0][i] > 0:
            sol_sdp.append(i)
        else:
            sol_sdp.append(-i)
    print("SDP solution: ", sat.eval(sol_sdp), sep="")
    print("Random solution: ", sat.eval(sol_rand), sep="")
