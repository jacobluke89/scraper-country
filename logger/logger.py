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

def logger(message):
    def decorator_logger(func):
        db_connection = DBManager(db, user, pw, host, port)

        @wraps(func)
        def wrapper_logger(*args, **kwargs):
            print(f'Function name: {func.__name__}')
            print(f'Logger args: {args}')
            print(f'Message: {message}')
            db_connection.save_log(func.__name__, LogLevel.INFO, LoggerNameLevel.INFO, message)
            result = func(*args, **kwargs)
            return result
        return wrapper_logger
    return decorator_logger


