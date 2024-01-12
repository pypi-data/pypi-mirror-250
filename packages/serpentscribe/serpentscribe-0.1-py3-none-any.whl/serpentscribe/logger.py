import functools
import json
import datetime

class Logger:
    """
    A simple logger class that logs function calls to console in JSON format.

    Attributes:
        log_file (str): The path to the log file where entries will be written.

    Methods:
        log(func_name, args, kwargs, result): Logs the function call details.
    """

    def __init__(self, log_file='function_log.json'):
        """
        Initializes the Logger instance with a specified log file.

        Args:
            log_file (str): The path to the log file. Defaults to 'function_log.json'.
        """
        self.log_file = log_file

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
            'timestamp': datetime.datetime.now().isoformat(),
            'function': func_name,
            'arguments': {'args': args, 'kwargs': kwargs},
            'result': result
        }
        print(json.dumps(log_entry))

def log_output(func=None):
    """
    A decorator that wraps a function and logs its calls to a file.

    The decorator logs the function name, its arguments, and its return value.

    Args:
        func (callable): The function to be decorated.

    Returns:
        callable: The wrapped function.
    """

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
            logger = Logger()
            logger.log(func.__name__, args, kwargs, result)
            return result
        return wrapper
    return decorator
