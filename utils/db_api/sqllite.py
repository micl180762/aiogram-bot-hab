import sqlite3


class Database:
    def __init__(self, path_to_db='mail.db') -> None:
        self.path_to_db = path_to_db

    @property  # чтобы не писать кажд раз при инит типа self.connection =...
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = tuple()  # парам всегда должны передаваться tuple-ом
        connection = self.connection
        cursor = connection.cursor()
        connection.set_trace_callback(logger)
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table_users(self):
        sql = """CREATE TABLE IF NOT EXISTS Users 
        (id int NOT NULL, Name varchar(255) NOT NULL, email varchar(255), primary key (id));"""
        self.execute(sql, parameters=None, commit=True)

    def add_user(self, id: int, name: str, email: str = None):
        sql = "INSERT INTO Users(id, Name, email) VALUES(?, ?, ?)"
        param = (id, name, email)
        self.execute(sql, parameters=param, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += ' AND '.join([f'{item} = ?' for item in parameters])
        ty = parameters.values()
        return sql, tuple(parameters.values())

    def select_all_users(self):
        sql = "SELECT id, Name, email FROM Users"
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT id, Name, email FROM Users WHERE "
        sql, params = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=params, fetchone=True)

    def count_users(self):
        return self.execute('SELECT COUNT(*) FROM Users', fetchone=True)

    def update_email(self, email, id):
        return self.execute("UPDATE Users SET email=? WHERE id=?", parameters=(email, id), commit=True)

    def delete_users(self):
        return self.execute("DELETE FROM Users WHERE TRUE", commit=True)

    def delete_user(self, **kwargs):
        sql = "DELETE FROM Users WHERE "
        sql, params = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=params, commit=True)


def logger(statement):
    print(f'{statement}')
