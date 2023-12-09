from functools import wraps

from databaseManager.connection import DBManager
from utils.globals import db, user, pw, host, port

class LogLevel:
    DEBUG = 1
    ERROR = 2
    INFO = 3


def  logger(func):
    db_connection = DBManager(db, user, pw, host, port)
    cursor = db_connection.get_cursor()

    @wraps(func)
    def wrapper_logger(*args, **kwargs):
        print(f'logger {args}')
        print(f'logger {kwargs}')

    return wrapper_logger

