from satinstance import Max2Sat
from random import randint

def get_randodm_instance(var_n: int, clause_n: int):
    mcnt = clause_n
    sat = Max2Sat(var_n)

    while mcnt > 0:
        a, b = randint(1, var_n), randint(1, var_n)
        if a == b:
            continue
        mcnt -= 1
        asign, bsign = randint(0, 1) * 2 - 1, randint(0, 1) * 2 - 1
        sat.add_clause(asign * a, bsign * b)
    return sat