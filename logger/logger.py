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
    MESSAGE = 4

class LoggerNameLevel:
    DEBUG = 'debug'
    ERROR = 'error'
    INFO = 'info'
    MESSAGE = 'message'


class SingleDBManager:
    _instance = None

    @classmethod
    def get_instance(cls) -> DBManager:
        if cls._instance is None:
            cls._instance = DBManager(db, user, pw, host, port)
        return cls._instance

def save_to_db(fun_name: str, message: str, db_manager: DBManager, log_level: int = LogLevel.INFO):
    """
    This function saves logs to a database.

    Args:
        fun_name (str): The name of the function we're logging about.
        message (str): The message we wish to save.
        db_manager(DBManager): The DBManager allows you to connect to the database, it's created in
        the function
        log_level (int, optional): The log level integer value. Defaults to LogLevel.INFO.

    Returns:
        None
    """

    level_to_name = {
        LogLevel.DEBUG: LoggerNameLevel.DEBUG,
        LogLevel.ERROR: LoggerNameLevel.ERROR,
        LogLevel.INFO: LoggerNameLevel.INFO,
        LogLevel.MESSAGE: LoggerNameLevel.MESSAGE
    }
    log_level_name = level_to_name.get(log_level, 'UNKNOWN LEVEL')

    db_manager.save_log(fun_name, log_level, log_level_name, message)


def logger(message: str = '', db_manager: DBManager = None):
    """
    A decorator that logs messages related to the execution of a function.

    Args:
        message (str, optional): A message to log alongside the function's name.
                                    Defaults to an empty string.
        db_manager (DBManager): The db manager for the logger if required.

    Returns:
        function: A decorator that takes a function and returns a wrapped function.
    """

    def decorator_logger(func):
        @wraps(func)
        def wrapper_logger(*args, **kwargs):
            if db_manager is None:
                local_db_manager = SingleDBManager.get_instance()
            else:
                local_db_manager = db_manager
            try:
                save_to_db(func.__name__, message, db_manager=local_db_manager)
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                exception_message = f"Exception in {func.__name__}: {str(e)}"
                save_to_db(func.__name__, exception_message, db_manager=local_db_manager, log_level=LogLevel.ERROR)
                raise
        return wrapper_logger
    return decorator_logger


def message_logger(message: str,
                   message_level: int,
                   db_manager: DBManager = SingleDBManager.get_instance()):
    """
    Logs a message to the database with the name of the calling function.

    This function retrieves the name of the function that called `message_logger`
    using the `inspect` module and then logs the provided message to a database.
    The logging is handled by the `save_to_db` function.

    Args:
        message (str): The message to be logged.
        message_level (int): should be an integer from the enum class LogLevel.
        db_manager (SingleDBManager): DBManager instance

    Returns:
        None
    """
    caller_name = inspect.currentframe().f_back.f_code.co_name
    save_to_db(caller_name, f'MESSAGE LOGGER: {message}', db_manager, log_level=message_level)
