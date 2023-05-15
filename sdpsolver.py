# Purpose: Class for an SDP solver.
import numpy.linalg as la
import numpy as np

from app import LogObject

def is_nonneg_def(x):
    return np.all(np.linalg.eigvals(x) >= 0)

def newton_direction(W, mu, X):
    n = X.shape[0]
    lhs = []
    rhs = []
    Z = mu * la.inv(X) - W
    for i in range(n):
        XeeTX = X[:, i].reshape((n, 1)) @ X[i, :].reshape((1, n))
        # print(X)
        # print(XeeTX)
        lhs.append(np.diagonal(XeeTX).copy())
        rhs.append(-np.trace(XeeTX @ Z))
    y = la.solve(lhs, rhs)
    D = X @ (np.diag(y) + Z) @ X / mu
    return D, y


def newton_phase_0(W, mu, beta, X_init=None):
    """output: X, y for given tolerance beta"""
    n = W.shape[0]

    LogObject.log("NEWTON_PHASE_0_BEGIN")
    LogObject.log(f"n {n} mu {mu} beta {beta}")

    if X_init is None:
        X_curr = np.eye(n, dtype=np.float64)
        L_curr = np.eye(n, dtype=np.float64)
    else:
        X_curr = X_init
        L_curr = la.cholesky(X_curr)
    iter_n = 0
    while True:
        D, y = newton_direction(W, mu, X_curr)
        S = W - np.diag(y)

        criteria = la.norm(la.inv(L_curr) @ D @ la.inv(L_curr.T))
        LogObject.log(f"iter {iter_n} criteria {criteria}")
        if criteria < beta:
            break

        alpha = 0.2 / criteria

        X_curr = X_curr + alpha * D
        L_curr = la.cholesky(X_curr)

        iter_n += 1

    LogObject.log("NEWTON_PHASE_0_END")

    return X_curr, y, S


class SDPSpherical:
    def __init__(self, W, tolerance=1e-4, max_iter=1000):
        self.W = W
        self.tolerance = tolerance
        self.max_iter = max_iter


    def solve(self):

        n = self.W.shape[0]
        beta = 0.5
        mu = 0.1

        LogObject.log("SDP_SOLVER_START")

        X_curr, y, S = newton_phase_0(self.W, mu, beta)

        # while np.abs(n * mu * (1 - beta)) > self.tolerance:

        criteria = np.abs(np.trace(X_curr @ S))
        iter_n = 0

        while criteria > self.tolerance:
            LogObject.log(f"iter_n {iter_n} n {n} beta {beta} mu {mu} gap {criteria}")
            alpha = 1 - (np.sqrt(beta) - beta) / (np.sqrt(beta) + np.sqrt(n))
            mu = alpha * mu
            D, y = newton_direction(self.W, mu, X_curr)

            if not is_nonneg_def(X_curr):
                raise Exception("Newton direction is not positive definite.")
            # backtracking line search
            alpha = 1.0
            discount = 0.9
            while not is_nonneg_def(X_curr + alpha * D):
                alpha = discount * alpha
            X_curr = X_curr + alpha * D

            S = self.W - np.diag(y)
            iter_n += 1
            criteria = np.abs(np.trace(X_curr @ S))
            # print("Integrality Gap:", np.trace(X_curr @ S))

        LogObject.log("SDP_SOLVER_END")
        return X_curr


if __name__ == "__main__":
    # pass
    from encoder import *

    LogObject.bind_file("log.txt")
    n = 50
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

    W, a_list, b_list = max2sat_to_sdp(sat)

    # mu = 0.1
    # X, y, S = newton_phase_0(W, mu)
    # L = la.cholesky(X)

    # print(np.diag(X))
    # print(la.norm(np.diag(y) + S - W))
    # print(la.norm(np.eye(n + 1) - L.T @ S @ L / mu))

    solver = SDPSpherical(W)
    X = solver.solve()
    print(X)

    import cvxpy as cp

    X_cvx = cp.Variable((n + 1, n + 1), symmetric=True)
    constraints = [X_cvx >> 0]
    for a, b in zip(a_list, b_list):
        constraints.append(cp.trace(a @ X_cvx) == b)

    prob = cp.Problem(cp.Minimize(cp.trace(W @ X_cvx)), constraints)
    prob.solve()

    print(np.max(np.abs(X_cvx.value - X)))


    print(np.max(np.abs(X_cvx.value - X)))

    LogObject.print_log()