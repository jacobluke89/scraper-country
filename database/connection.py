import psycopg2

class DBConnection:

    def __init__(self, database, user, pw, host, port):
        self.database = database
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port


    def get_cursor(self):
        conn = psycopg2.connect(
            database = self.database,
            user = self.user,
            password = self.pw,
            host = self.host,
            port = self.port
        )
        self.conn = conn
        conn.autocommit = True

        self.cursor = conn.cursor()
