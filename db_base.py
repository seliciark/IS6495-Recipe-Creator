# DBbase file

# Import packages
import sqlite3
class DBbase:

    # Variables
    _conn = None
    _cursor = None


    # Constructor passing in an argument indicating a DB name so that it can be reused
    def __init__(self, db_name):
        self._db_name = db_name
        # when the instance is first created, connect will be automatically called
        self.connect()

    # Function/method: creates connection to the DB
    def connect(self):
        # passes in the DB (file/path) name that we want to connect to
        self._conn = sqlite3.connect(self._db_name)
        # cursor that is our portal that allows us to interact with the DB
        self._cursor = self._conn.cursor()

    # Function/method: passes in and executes raw SQL
    def execute_script(self, sql_string):
        try:
            self._cursor.executescript(sql_string)
        except Exception as e:
            print(f"An error occured: {e}")

    # Function/method: resets the database
    def reset_database(self):
        raise  NotImplementedError("Must implement from the derived class")

    # Function/method: closes the connection
    def close_db(self):
        self._conn.close()

    # decorator
    @property
    # function/method: getter, which makes it read-only
    def get_cursor(self):
        return self._cursor

    @property
    # function/method: getter
    def get_connection(self):
        return self._conn
