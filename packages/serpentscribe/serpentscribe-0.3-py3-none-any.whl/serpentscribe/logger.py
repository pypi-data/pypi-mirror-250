import functools
import logging
import json
import datetime
import sys


class Logger:
    def __init__(self, level, log_file=None):
        """
        Initializes the Logger instance with a specified log level and log file.

        Args:
            level (str): The level of logging (ex. DEBUG, INFO, WARNING, ERROR, CRITICAL).
            log_file (str): The path to the log file. Defaults to None which means logs will be written to stdout.
        """
        self.level = level.upper()
        if log_file is None:
            self.handler = logging.StreamHandler(sys.stdout)
        else:
            self.handler = logging.FileHandler(log_file)
        # self.logger = self.setup_logger()

    @property
    def logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(self.level)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.handler.setFormatter(formatter)
        logger.addHandler(self.handler)

        return logger

    def log(self, func_name, args, kwargs, result):
        """
        Logs the function call details to the log file in JSON format.

        Args:
            func_name (str): The name of the function being logged.
            args (tuple): The positional arguments passed to the function.
            kwargs (dict): The keyword arguments passed to the function.
            result: The result returned by the function.
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "function": func_name,
            "arguments": {"args": args, "kwargs": kwargs},
            "result": result,
        }
        if self.level == "DEBUG":
            self.logger.debug(json.dumps(log_entry))
        elif self.level == "INFO":
            self.logger.info(json.dumps(log_entry))


def log_output(level, output_file=None):
    """
    A decorator that wraps a function and logs its calls to a file.

    The decorator logs the function name, its arguments, and its return value.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function.
    """
    logging.basicConfig(level=logging.INFO)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """
            The wrapper function around the decorated function.

            Args:
                *args: Variable length argument list for the decorated function.
                **kwargs: Arbitrary keyword arguments for the decorated function.

            Returns:
                The result of the decorated function.
            """
            result = func(*args, **kwargs)
            logger = Logger(level, output_file)
            logger.log(func.__name__, args, kwargs, result)
            return result

        return wrapper

    return decorator
