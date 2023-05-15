import os
from satinstance import Max2Sat
import sys

TIMEOUT = 1


files = os.listdir("benchmarks")

for i, f in enumerate(files):
    if not f.endswith(".cnf"):
        continue

    print(f"now: {f} {i}/{len(files)}")
    _, n, m, k = f.split("_")
    n, m = int(n), int(m)
    sat = Max2Sat(n)

    with open(os.path.join("benchmarks", f), "r") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("p"):
                continue
            a, b, _ = line.split()
            sat.add_clause(int(a), int(b))

    # execute system util uwrmaxsat on the file and save the result
    os.system(f"timeout {TIMEOUT} uwrmaxsat benchmarks/{f} -m -v0 > benchmarks-sol/{f}.sol")

    # read the result
    with open(f"benchmarks-sol/{f}.sol", "r") as file:
        lines = file.readlines()

    with open(f"benchmarks-sol/{f}.sol", "a") as file:
        opt = -1
        for line in lines:
            if line.startswith("v"):
                sol = line.split()[1:]
                sol = list(map(int, sol))
                opt = sat.eval(sol)
                break
        file.write(f"OPT {opt}\n")
