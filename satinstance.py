# Purpose: Class for representing a Max-2-SAT instance.

class Max2Sat:
    def __init__(self, n):
        self.n = n
        self._clauses = []

    def add_clause(self, a, b):
        assert 1 <= abs(a) <= self.n
        self._clauses.append((a, b))

    def get_n(self):
        return self.n

    def get_clauses(self):
        return self._clauses

    def eval(self, sol):
        assert len(sol) == self.n
        sol_set = set(sol)
        sat_clauses = 0
        for a, b in self._clauses:
            if a in sol_set or b in sol_set:
                sat_clauses += 1
        return sat_clauses

    def __str__(self):
        str_repr = f"p cnf {self.n} {len(self._clauses)}\n"
        for a, b in self._clauses:
            str_repr += f"{a} {b} 0\n"
        return str_repr

