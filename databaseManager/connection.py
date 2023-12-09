import psycopg2
from contextlib import contextmanager
from psycopg2 import pool

class DBManager:
    def __init__(self, database, user, pw, host, port):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                                                                  database=database,
                                                                  user=user,
                                                                  password=pw,
                                                                  host=host,
                                                                  port=port)

    def close_all_connections(self):
        self.connection_pool.closeall()

    @contextmanager
    def get_cursor(self):
        connection = self.connection_pool.getconn()
        try:
            yield connection.cursor()
            connection.commit()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
        finally:
            self.connection_pool.putconn(connection)
