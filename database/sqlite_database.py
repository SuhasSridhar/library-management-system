import sqlite3

class SQLiteDatabase:
    def __init__(self, database_name: str):
        self.connection = sqlite3.connect(database_name)
        self.connection.execute("PRAGMA foreign_keys = ON")

    def get_connection(self) -> sqlite3.Connection:
        return self.connection

    def close(self) -> None:
        self.connection.close()