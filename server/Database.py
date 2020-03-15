import sqlite3
from Subscriber import Subscriber, generate_user, get_subs_set_from_json
import json

class Database:
    def __init__(self, db_filename="subsribers.db"):
        self.conn = sqlite3.connect(db_filename)
        self.cursor = self.conn.cursor()
        self.refresh()
    
    def create_if_not_exists(self):
        self.cursor.execute(
            """create table if not exists subscribers (
                uuid text not null unique,
                name text not null,
                balance integer not null,
                hold integer not null,
                status integer not null
            );""")
        self.conn.commit()
    
    def insert_one_subscriber(self, sub):
        status = 1 if sub.status else 0
        self.cursor.execute(
            """insert into subscribers (
                uuid, name, balance, hold, status
            )
            values (?, ?, ?, ?, ?);""", [str(sub.uuid), sub.name, sub.balance, sub.hold, status])
        self.conn.commit()
    
    def insert_multiple_subscriber(self, sub_dict):
        for sub in sub_dict:
            status = 1 if sub.status else 0
            self.cursor.execute(
                """insert into subscribers (
                    uuid, name, balance, hold, status
                )
                values (?, ?, ?, ?, ?);""", [str(sub.uuid), sub.name, sub.balance, sub.hold, status])
        self.conn.commit()

    def all_users(self):
        records = self.cursor.execute("select * from subscribers;").fetchall()
        subscribers = set()
        for u in records:
            sub = Subscriber(u[0], u[1], u[2], u[3], u[4]==1)
            subscribers.add(sub)
        return subscribers
    
    def drop_table_if_exists(self):
        self.cursor.execute("drop table if exists subscribers;")
    
    def refresh(self):
        self.drop_table_if_exists()
        self.create_if_not_exists()
    
    def load_from_json(self, filename="server/example.json"):
        subscribers = get_subs_set_from_json(filename)
        self.insert_multiple_subscriber(subscribers)
        print(self.all_users())



