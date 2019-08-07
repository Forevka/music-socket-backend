import sqlite3
from loguru import logger

class DBWorker:
    def __init__(self):
        self.connect_db()
        logger.info(self.cursor)



    def connect_db(self):
        self.conn = sqlite3.connect("DB.db")
        self.cursor = self.conn.cursor()



    def add_new_user(self, login, password):
        self.cursor.execute('''INSERT INTO "users_info" (login, password, role)
                        VALUES ('{}', '{}', '{}') ON CONFLICT DO NOTHING'''.format(login, password, "guest"))
        self.conn.commit()
        logger.info(self.cursor.lastrowid)
        if self.cursor.lastrowid:
            return self.cursor.lastrowid
        return False


    def get_user(self, login):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' '''.format(login))
        k = self.cursor.fetchall()
        if k:
            return k
        return False

    def authentication(self, login, password):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' and password = '{}' '''.format(login, password))
        k = self.cursor.fetchone()
        logger.info(k)
        if k:
            return [k[1], k[2], k[3]]
        return False
