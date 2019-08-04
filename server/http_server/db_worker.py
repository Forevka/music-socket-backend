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
        if not self.check_availability_login(login):
            self.cursor.execute('''INSERT INTO "users_info" (login, password)
                            VALUES ('{}', '{}')'''.format(login, password))
            self.conn.commit()
            logger.info("successfully added")
            return self.cursor.lastrowid
        return False




    def check_availability_login(self, login):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' '''.format(login))
        self.conn.commit()
        k = self.cursor.fetchall()
        logger.info(k)
        if k:
            return True
        return False

    def return_id(self, login):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' '''.format(login))
        self.conn.commit()
        k = self.cursor.fetchall()
        if k:
            return k[0][0]
        return False

    def authentication(self, login, password):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' and password = '{}' '''.format(login, password))
        self.conn.commit()
        k = self.cursor.fetchall()
        logger.info(k)
        if k:
            return True
        return False
