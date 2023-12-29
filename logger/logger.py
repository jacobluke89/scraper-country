import inspect
from functools import wraps

from database_manager.connection import DBManager
from utils.globals import db, user, pw, host, port


"""
   Example:
       To use this logger decorator, simply place it above a function definition:

       @logger(message="Example function execution")
       def example_function(param1, param2):
           # Function implementation
           
    Example:
        To use `message_logger` within a function:
        from 
        def example_function():
            # Function implementation
            message_logger("Example message")

   Notes:
       - The database connection details (db, user, pw, host, port) should be
         predefined or accessible within the scope of the decorator.
       - The `save_to_db` function is used to save logs to the database.
"""

class LogLevel:
    DEBUG = 1
    ERROR = 2
    INFO = 3

class LoggerNameLevel:
    DEBUG = 'debug'
    ERROR = 'error'
    INFO = 'info'


def save_to_db(fun_name: str, message: str, log_level: int = LogLevel.INFO):
    """
    This function saves logs to a database.

    Args:
        fun_name (str): The name of the function we're logging about.
        message (str): The message we wish to save.
        log_level (int, optional): The log level integer value. Defaults to LogLevel.INFO.

    Returns:
        None
    """
    level_to_name = {
        LogLevel.DEBUG: LoggerNameLevel.DEBUG,
        LogLevel.ERROR: LoggerNameLevel.ERROR,
        LogLevel.INFO: LoggerNameLevel.INFO
    }
    log_level_name = level_to_name.get(log_level, 'UNKNOWN LEVEL')
    db_connection = DBManager(db, user, pw, host, port)
    db_connection.save_log(fun_name, log_level, log_level_name, message)


def logger(message: str = ''):
    """
       A decorator that logs messages related to the execution of a function.

       Args:
           message (str, optional): A message to log alongside the function's name.
                                    Defaults to an empty string.

       Returns:
           function: A decorator that takes a function and returns a wrapped function.
       """
    def decorator_logger(func):
        @wraps(func)
        def wrapper_logger(*args, **kwargs):
            try:
                save_to_db(func.__name__, message)
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                exception_message = f"Exception in {func.__name__}: {str(e)}"
                save_to_db(func.__name__, exception_message, LogLevel.ERROR)
                raise
        return wrapper_logger
    return decorator_logger


def message_logger(message):
    """
    Logs a message to the database with the name of the calling function.

    This function retrieves the name of the function that called `message_logger`
    using the `inspect` module and then logs the provided message to a database.
    The logging is handled by the `save_to_db` function.

    Args:
        message (str): The message to be logged.

    Returns:
        None
    """
    caller_name = inspect.currentframe().f_back.f_code.co_name
    save_to_db(caller_name, f'MESSAGE LOGGER: {message}')
