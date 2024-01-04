from datetime import datetime

import psycopg2
from contextlib import contextmanager
from psycopg2 import pool

class DBManager:
    def __init__(self, database, user, pw, host, port=None):
        self.connection_pool = psycopg2.pool.SimpleConnectionPool(1, 10,
                                                                  database=database,
                                                                  user=user,
                                                                  password=pw,
                                                                  host=host,
                                                                  port=port)
        self.db = database

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

    def save_log(self, fn_name, err_lvl, lvl_name, info):
        print('DB IS ', self.db)
        insert_query = f"""
        INSERT INTO {self.db}.logger(function_name, date_time, error_level, level_name, info)
        VALUES (%s, %s, %s, %s, %s)
        """
        current_time = datetime.now()
        with self.get_cursor() as cursor:
            cursor.execute(insert_query, (fn_name, current_time, err_lvl, lvl_name, info))


