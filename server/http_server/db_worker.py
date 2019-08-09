import sqlite3
from loguru import logger
import settings

class DBWorker:
    def __init__(self):
        self.connect_db()
        logger.info(self.cursor)



    def connect_db(self):
        self.conn = sqlite3.connect("DB.db")
        self.cursor = self.conn.cursor()



    def add_new_user(self, login, password):
        img_url = settings.image_url.format(login)
        logger.info(img_url)
        self.cursor.execute('''INSERT OR IGNORE INTO "users_info" (login, password, role, image)
                        VALUES ('{}', '{}', {}, '{}')'''.format(login, password, 1, img_url))
        self.conn.commit()
        logger.info(self.cursor.lastrowid)
        if self.cursor.lastrowid:
            return {"id": self.cursor.lastrowid, "login": login, "role": 1, "img_url": img_url}
        return False


    def get_user(self, login):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' '''.format(login))
        k = self.cursor.fetchone()
        if k:
            return {"id": k[0], "login": k[1], "role": k[3], "img_url": k[4]}
        return False

    def authentication(self, login, password):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' and password = '{}' '''.format(login, password))
        k = self.cursor.fetchone()
        logger.info(k)
        if k:
            return {"id": k[0], "login": k[1], "role": k[3], "img_url": k[4]}
        return False



    def get_channel(self, id):
        self.cursor.execute('''SELECT * FROM "channels" WHERE id = {} '''.format(id))
        k = self.cursor.fetchone()
        if k:
            return {"id": k[0], "name": k[1], "description": k[2], "img_url": k[4]}
        return False
