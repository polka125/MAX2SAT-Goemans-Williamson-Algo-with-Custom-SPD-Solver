# Purpose: Class for representing a SDP instance.

import numpy.typing as npt
import numpy as np
from typing import List
from app import LogObject


# we use the following SDP format:
# minimize tr<C, X>
# subject to tr<A_i, X> = b_i, i = 1, ..., m
# X >> 0
class SDPinstance:
    def __init__(self, n: int, c: npt.ArrayLike, a_list: List[npt.ArrayLike], b_list: List[float]):
        """@param: n: int, number of variables, X is positive semidefinite n x n matrix
        @param: c: n x n matrix, objective function, goal is to minimize tr<C, X>
        @param: a_list: list of n x n matrices, constraints, tr<A_i, X> = b_i, i = 1, ..., m
        @param: b_list: list of floats, constraints, tr<A_i, X> = b_i, i = 1, ..., m
        """
        self.n = n
        self.c = c
        self.a_list = a_list
        self.b_list = b_list

    def __str__(self):
        return f"SDPinstance(n={self.n}, c={self.c}, a_list={self.a_list}, b_list={self.b_list})"
