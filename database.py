import sqlite3
import os


class Database(object):

    def __init__(self, dataname):
        self.dataname = dataname
        if not os.path.isfile(self.dataname):
            cursor, connect = self.__connect_database()
            self.__create_tables(cursor)
            cursor.close()
            connect.close()

    def __create_tables(self, cursor):
        cursor.execute('''CREATE TABLE citizens (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           import_id INTEGER,
                           citizens_id INTEGER,
                           town TEXT,
                           street TEXT,
                           building TEXT,
                           apartment INTEGER,
                           name TEXT,
                           birth_date TEXT,
                           gender TEXT
                           );
                           
                           CREATE TABLE relatives (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           import_id INTEGER,
                           citizen_id INTEGER,
                           relative_id INTEGER
                           );
                        ''')

    def __connect_database(self):
        is_ok = False
        try:
            con = sqlite3.connect(self.dataname, isolation_level=None)
        except sqlite3.Error as e:
            print(e)
        else:
            is_ok = True
        finally:
            if is_ok:
                return con.cursor(), con
            exit(0)

    def execute_query(self, query):
        cursor, connect = self.__connect_database()
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        connect.close()
        return data
