import sqlite3
from Subscriber import Subscriber, generate_user
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

    def _all_subs(self):
        return self.cursor.execute("select * from subscribers;").fetchall()
    
    def drop_table_if_exists(self):
        self.cursor.execute("drop table if exists subscribers;")
    
    def refresh(self):
        self.drop_table_if_exists()
        self.create_if_not_exists()
    
    def load_from_json(self, filename="server/example.json"):
        with open(filename) as f:
            subs_from_json = json.loads(f.read())
        subscribers = []
        for u in subs_from_json:
            sub = Subscriber(u["uuid"], u["name"], u["balance"], u["hold"], u["status"])
            subscribers.append(sub)
        self.insert_multiple_subscriber(subscribers)
        print(self._all_subs())



