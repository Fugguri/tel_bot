import sqlite3


class DB:

    def __init__(self, db_file) -> None:

        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create(self):
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    telegram_id INTEGER NOT NULL UNIQUE ON CONFLICT IGNORE
                    );""")

    def add_user(self, telegram_id):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO users(telegram_id) VALUES({})".format(telegram_id))

    def is_user_exist(self, telegram_id):
        with self.connection:
            exist = self.cursor.execute(
                "SELECT EXISTS(SELECT telegram_id FROM users WHERE telegram_id = {}) ".format(telegram_id)).fetchone()[0]
            return exist
