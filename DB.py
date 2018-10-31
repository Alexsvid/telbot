__author__ = 'alexsviridov'

import psycopg2
import os
import logging
import datetime


#if __name__ == "__main__":
#    db = postgresql.open('pq://postgres:postgres@localhost:5432/mydb')
#else:
#    db = postgresql.open('postgres://ckfsscwlnlwzrz:f9afa49497b0ad5a2670817f677958f0ea7589701ba5a4f3c857255cd20b1bb9@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dmv0obck94pa5')

DATABASE_URL = os.environ['DATABASE_URL']


class BotDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS TVALUE (id SERIAL PRIMARY KEY, Value float)")

        self.cur.execute("SELECT Value FROM TVALUE")
        v = self.cur.fetchone()
        if v is None:
            self.cur.execute("INSERT INTO TVALUE (Value) VALUES (0) ")
            self.conn.commit()

        self.cur.execute("CREATE TABLE IF NOT EXISTS TLOG (id SERIAL PRIMARY KEY, opDate timestamp, opTag char(20),  opVALUE float)")

    def getValue(self):
        self.cur.execute("SELECT Value FROM TVALUE")
        v = self.cur.fetchone()
        logging.log(logging.DEBUG, "-- value from DB %s" % ''.join(map(str, v)))
        try:
            return float(v[0])
        except:
            return 0.0

    def setValue(self, value):
        self.cur.execute("UPDATE TVALUE SET Value = %s ", (value,))
        self.conn.commit()

    def setLog(self, value, text):
        self.cur.execute("INSERT INTO TLOG  (opDate, opTag, opVALUEs) VALUES (%s, %s, %s) ",
                         (datetime.datetime.now(), text, value))
        self.conn.commit()