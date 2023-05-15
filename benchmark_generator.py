import random
from random import seed
seed(42)

import numpy as np
np.random.seed(42)

import os




# n variables m clauses k files per instance
dataset = [
    (5, 10, 10),
    (5, 20, 10),
    (5, 50, 10),
    (10, 20, 10),
    (10, 50, 10),
    (10, 200, 10),
    (20, 40, 10),
    (20, 200, 10),
    (20, 800, 10),
    (50, 100, 10),
    (50, 2500 // 2, 10),
    (50, 2500 * 2, 10),
    (100, 200, 10),
    (100, 10000 // 2, 10),
    (100, 10000 * 2, 10),
]

from randomsatgenerator import get_randodm_instance


print(os.getcwd())
for n, m, k in dataset:
    for i in range(k):
        sat = get_randodm_instance(n, m)
        with open(os.path.join("benchmarks", f"random_{n}_{m}_{i}.cnf"), "w") as f:
            f.write(str(sat))