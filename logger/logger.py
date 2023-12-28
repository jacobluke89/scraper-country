import inspect
from functools import wraps

from databaseManager.connection import DBManager
from utils.globals import db, user, pw, host, port

class LogLevel:
    DEBUG = 1
    ERROR = 2
    INFO = 3

class LoggerNameLevel:
    DEBUG = 'debug'
    ERROR = 'error'
    INFO = 'info'


def save_to_db(fun_name: str, message: str, log_level: int = LogLevel.INFO, log_level_name: str = LoggerNameLevel.INFO):
    db_connection = DBManager(db, user, pw, host, port)
    db_connection.save_log(fun_name, log_level, log_level_name, message)


def logger(message: str = ''):
    def decorator_logger(func):
        db_connection = DBManager(db, user, pw, host, port)
        @wraps(func)
        def wrapper_logger(*args, **kwargs):
            try:
                save_to_db(func.__name__, message)
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                exception_message = f"Exception in {func.__name__}: {str(e)}"
                save_to_db(func.__name__, exception_message, LogLevel.ERROR, LoggerNameLevel.ERROR)
                raise
        return wrapper_logger
    return decorator_logger


def message_logger(message):
    caller_name = inspect.currentframe().f_back.f_code.co_name
    save_to_db(caller_name, f'MESSAGE LOGGER: {message}')

