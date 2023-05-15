import os

from app import LogObject, App
from satinstance import Max2Sat
from satsolver import random_solver, sdp_relaxation_solver
from parser import parse_cnf


def run_experiment(file_name):
    LogObject.bind_file(os.path.join(App.config("benchmark_output"), file_name + ".log"))
    LogObject.log(f"INSTANCE_BEGIN {file_name}")

    path_to_instance = os.path.join(App.config("benchmark_path"), file_name)
    instance = parse_cnf(path_to_instance)

    # solving with random solver
    LogObject.log("RANDOM_SOLVER_BEGIN")
    solution_random = random_solver(instance, App.config("random_trials"))
    OPT_random = instance.eval(solution_random)
    LogObject.log(f"SOLUTION_FOUND {solution_random}")
    LogObject.log(f"OPT {OPT_random}")
    LogObject.log("RANDOM_SOLVER_END")


    # solving with sdp relaxation solver
    LogObject.log("SDP_SOLVER_BEGIN")
    solution_sdp = sdp_relaxation_solver(instance, App.config("random_trials"))
    OPT_sdp = instance.eval(solution_sdp)
    LogObject.log(f"SOLUTION_FOUND {solution_sdp}")
    LogObject.log(f"OPT {OPT_sdp}")
    LogObject.log("SDP_SOLVER_END")


    # looking for exact solution
    LogObject.log("EXACT_SOLVER_BEGIN")
    path_to_exact_solution = os.path.join(App.config("benchmark_exact_ans"), file_name + ".sol")
    with open(path_to_exact_solution, "r") as f:
        lines = f.readlines()
    exact_solution = None
    OPT_opt = -1
    for line in lines:
        if line.startswith("v"):
            exact_solution = [int(x) for x in line.split(" ")[1:]]
            OPT_opt = instance.eval(exact_solution)
    if exact_solution is not None:
        LogObject.log(f"EXACT_SOLUTION_FOUND {exact_solution}")
        LogObject.log(f"OPT {OPT_opt}")
    else:
        LogObject.log(f"EXACT_SOLUTION_FOND None")
        LogObject.log(f"OPT {OPT_opt}")
    LogObject.log("EXACT_SOLVER_END")


    LogObject.log(f"SUMMARY_BEGIN")
    LogObject.log(f"RANDOM_SOLVER {OPT_random}")
    LogObject.log(f"SDP_SOLVER {OPT_sdp}")
    LogObject.log(f"EXACT_SOLVER {OPT_opt}")
    LogObject.log(f"SUMMARY_END")

    LogObject.log(f"INSTANCE_END {file_name}")

    LogObject.flush()


if __name__ == "__main__":
    for i, file_name in enumerate(os.listdir(App.config("benchmark_path"))):
        try:
            print(f"Running experiment {i + 1} / {len(os.listdir(App.config('benchmark_path')))}: {file_name}")
            if file_name.endswith(".cnf"):
                run_experiment(file_name)

        except Exception as e:
            print(f"Exception occured during experiment {file_name}: {e}")
            with open("failed_experiments.txt", "a") as f:
                f.write(f"{file_name}\n{e}\n")