__author__ = 'alexsviridov'

import postgresql


#if __name__ == "__main__":
#    db = postgresql.open('pq://postgres:postgres@localhost:5432/mydb')
#else:
#    db = postgresql.open('postgres://ckfsscwlnlwzrz:f9afa49497b0ad5a2670817f677958f0ea7589701ba5a4f3c857255cd20b1bb9@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dmv0obck94pa5')



class BotDatabase:
    def __init__(self):
        self.db = postgresql.open('postgres://ckfsscwlnlwzrz:f9afa49497b0ad5a2670817f677958f0ea7589701ba5a4f3c857255cd20b1bb9@ec2-23-23-80-20.compute-1.amazonaws.com:5432/dmv0obck94pa5')
        self.db.execute("CREATE TABLE IF NOT EXISTS TVALUE (id SERIAL PRIMARY KEY, Value float")
        self.db.execute("CREATE TABLE IF NOT EXISTS TLOG (id SERIAL PRIMARY KEY, opDate timestamp, opTag char(20),  opVALUE float")

    def getValue(self):
        return self.db.query("SELECT Value FROM TVALUE")