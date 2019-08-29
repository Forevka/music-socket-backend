import sqlite3
from loguru import logger
from ..utils import settings

class SingletonMeta(type):
    """
    В Python класс Одиночка можно реализовать по-разному. Возможные способы
    включают себя базовый класс, декоратор, метакласс. Мы воспользуемся
    метаклассом, поскольку он лучше всего подходит для этой цели.
    """

    _instance = None

    def __call__(self):
        if self._instance is None:
            self._instance = super().__call__()
        return self._instance

class DBWorker(metaclass=SingletonMeta):
    def __init__(self):
        self.connect_db()
        logger.info(self.cursor)


    def connect_db(self):
        self.conn = sqlite3.connect("DB.db")
        self.cursor = self.conn.cursor()


    def add_new_user(self, login, password, email):
        img_url = settings.image_url.format(login)
        logger.info(img_url)
        self.cursor.execute('''INSERT OR IGNORE INTO "users_info" (login, password, role, image, email)
                        VALUES ('{}', '{}', {}, '{}', '{}')'''.format(login, password, 1, img_url, email))
        self.conn.commit()
        logger.info(self.cursor.lastrowid)
        if self.cursor.lastrowid:
            return {"id": self.cursor.lastrowid, "login": login, "role": 1, "img_url": img_url, "email": email}
        return False


    def get_user(self, login):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' '''.format(login))
        k = self.cursor.fetchone()
        if k:
            return {"id": k[0], "login": k[1], "role": k[3], "img_url": k[4], "email": k[5]}
        return False


    def authentication(self, login, password):
        self.cursor.execute('''SELECT * FROM "users_info" WHERE login = '{}' and password = '{}' '''.format(login, password))
        k = self.cursor.fetchone()
        logger.info(k)
        if k:
            return {"id": k[0], "login": k[1], "role": k[3], "img_url": k[4], "email": k[5]}
        return False

    def update_password(self, new_pass, email):
        logger.info(new_pass)
        self.cursor.execute('''UPDATE users_info SET password = '{}' WHERE email = '{}' '''.format(new_pass, email))
        self.conn.commit()


    def get_channel_list(self, page = 0, amount = 10):
        self.cursor.execute(f'SELECT * FROM "channels" LIMIT {amount} OFFSET {page * amount}')
        k = self.cursor.fetchall()
        print("k", len(k))
        d = {"page": page, 'amount': amount, "channels": []}
        logger.info(k)
        for i in k:
            d['channels'].append({"id": i[0], "name": i[1], "description": i[2], "img_url": i[3]})
        #logger.info(d["channels"])
        return d


    def get_channels_number(self):
        self.cursor.execute(f'SELECT COUNT(id) FROM "channels"')
        k = self.cursor.fetchone()
        logger.debug(k)
        return {"number": k[0]}



    def check_email(self, email):
        logger.info(email)
        self.cursor.execute('''SELECT * FROM "users_info" WHERE email = '{}' '''.format(email))
        k = self.cursor.fetchone()
        if k:
            return {"id": k[0], "login": k[1], "role": k[3], "img_url": k[4], "email": k[5]}
        return False



    def delete_user(self, login):
        self.cursor.execute('''DELETE FROM "users_info" WHERE login = '{}' '''.format(login))
        self.conn.commit()



    def get_channel(self, id):
        self.cursor.execute('''SELECT * FROM "channels" WHERE id = {} '''.format(id))
        k = self.cursor.fetchone()
        if k:
            return {"id": k[0], "name": k[1], "description": k[2], "img_url": k[3]}
        return False
