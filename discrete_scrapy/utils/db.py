# coding=utf8
import psycopg2
import logging

# HOST = '47.93.5.189'
# HOST = 'localhost'
HOST = '172.16.10.133'
PORT = '5432'
DATABASE = 'peiwo_bi'
USER = 'huangkaijie'
USER = 'peiwo_bi'
PASSWORD = 'raybo123'


class BaseDB(object):

    def __init__(self, database='peiwo_bi',port='5432'):
        self.conn = psycopg2.connect(database=database, password=PASSWORD, user=USER, host=HOST, port=port)
        self.cur = self.conn.cursor()

    def query(self, table=None, columns_values=None):
        # 插入操作
        if table and columns_values:
            try:
                sql = 'INSERT INTO  %s  %s  ' % (table, columns_values)
                self.cur.execute(sql)
                self.commit()
            except Exception as e:
                self.commit()
                logging.error(str(e))

    def update(self):
        # 更新操作
        pass

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
