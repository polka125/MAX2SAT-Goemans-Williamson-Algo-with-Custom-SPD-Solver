# Purpose: Class for storing the application configurations.

import datetime

class App:
    """Application configuration class."""
    __conf = {
        "benchmark_path": "benchmarks",
        "benchmark_output": "benchmarks-exp-res",
        "benchmark_exact_ans": "benchmarks-sol",
        "random_trials": 100,
    }

    @staticmethod
    def config(name):
        return App.__conf[name]

    @staticmethod
    def set(name, value):
        App.__conf[name] = value

class LogObject:
    """Log object class."""
    __log = {
        "log": [],
    }
    @staticmethod
    def get_log():
        return LogObject.__log["log"]

    @staticmethod
    def log(log):
        LogObject.__log["log"].append(log)

    @staticmethod
    def bind_file(f):
        LogObject.__log["f"] = open(f, "a")

        # write logger started + current time
        LogObject.__log["f"].write("LOGGER_STARTED " + str(datetime.datetime.now()) + "\n")

    @staticmethod
    def get_file():
        if "f" not in LogObject.__log:
            return None
        return LogObject.__log["f"]

    @staticmethod
    def print_log():
        if LogObject.get_file() is not None:
            LogObject.__log["f"].write("\n".join(LogObject.__log["log"]))
        else:
            print("\n".join(LogObject.__log["log"]))

    @staticmethod
    def clear_buffer():
        LogObject.__log["log"] = []

    @staticmethod
    def flush():
        LogObject.print_log()
        LogObject.clear_buffer()