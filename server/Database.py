import sqlite3
from Subscriber import Subscriber, generate_user

class Database:
    def __init__(self, db_filename="subsribers.db"):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self.create_if_not_exist()
    
    def create_if_not_exist(self):
        self.cursor.execute(
            """create table if not exists subscribers (
                uuid text not null unique,
                name text not null,
                balance integer not null,
                hold integer not null,
                status integer not null
            );""")
    
    def insert_subscriber(self, sub):
        status = 1 if sub.status else 0
        self.cursor.execute(
            """insert into subscribers (
                uuid, name, balance, hold, status
            )
            values (?, ?, ?, ?, ?);""", [str(sub.uuid), sub.name, sub.balance, sub.hold, status])
        self.conn.commit()

    def _all_subs(self):
        return self.cursor.execute("select * from subscribers;").fetchall()