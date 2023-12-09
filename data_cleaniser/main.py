from databaseManager.connection import DBManager

def run():
    dbc = DBManager('postgres', 'jacobbickerstaff', 'postgres', 'localhost', 5432)
    cur = dbc.get_cursor()
    print('success!')
