# Purpose: Class for input file parsing.
from satinstance import Max2Sat

def parse_cnf(path_to_file):
    sat = None

    with open (path_to_file, "r") as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        if line.strip() == "":
            continue
        if line.strip().startswith("c"):
            continue
        if line.startswith("p"):
            _, _, n, m = line.split()
            n, m = int(n), int(m)
            sat = Max2Sat(n)
            continue

        linesplit = line.split()
        if len(linesplit) != 3:
            raise Exception(f"Line {i + 1}: is not a valid 2sat clause.")
        a, b, zero = linesplit
        if zero != "0":
            raise Exception(f"Line {i + 1}: sequence must terminates with 0, {zero} given.")
        if sat is None:
            raise Exception(f"Line {i + 1}: p cnf n m line must come before any clause.")
        a, b = int(a), int(b)
        if abs(a) > n or abs(b) > n or abs(a) == 0 or abs(b) == 0:
            raise Exception(f"Line {i + 1}: clause {a} {b} is not valid for n = {n}.")
        sat.add_clause(a, b)
    return sat

