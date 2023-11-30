from database.connection import DBConnection


if __name__ == '__main__':

    dbc = DBConnection('postgres', 'jacobbickerstaff', 'postgres', 'localhost', 5432)
    cur = dbc.get_cursor()
    print('success!')


