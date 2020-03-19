import psycopg2
from psycopg2 import sql
from Subscriber import Subscriber, get_subs_set_from_json
import json
import helpers.exceptions as e


class DatabaseClient:
    def __init__(self):
        pass

    def __enter__(self):
        self.conn = psycopg2.connect(dbname='postgres', user='postgres',
                                     password='postgres', host='postgres')
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.conn.close()

    def create_table(self):
        self.cursor.execute("""create table if not exists public.subscribers(
uuid varchar not null unique,
name varchar not null,
balance integer not null,
hold integer not null,
status integer not null);""")
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute("drop table if exists subscribers;")

    def add_one_subscriber(self, sub):
        status = 1 if sub.status else 0
        values = [(str(sub.uuid), sub.name, sub.balance, sub.hold, status), ]
        insert = sql.SQL('INSERT INTO subscribers (uuid, name, balance, hold, status) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, values))
        )
        self.cursor.execute(insert)
        self.conn.commit()

    def insert_multiple_subscriber(self, sub_list):
        subs_list_for_bd = [(str(sub.uuid), sub.name, sub.balance,
                             sub.hold, 1 if sub.status else 0) for sub in sub_list]
        insert = sql.SQL('INSERT INTO subscribers (uuid, name, balance, hold, status) VALUES {}').format(
            sql.SQL(',').join(map(sql.Literal, subs_list_for_bd))
        )
        self.cursor.execute(insert)
        self.conn.commit()

    def update_balance(self, sub):
        self.cursor.execute(
            'update subscribers set balance=%s where uuid=%s', ((sub.balance, str(sub.uuid))))
        self.conn.commit()

    def update_hold(self, sub):
        self.cursor.execute(
            'update subscribers set hold=%s where uuid=%s', ((sub.hold, str(sub.uuid))))
        self.conn.commit()

    def substract_hold_of_every_sub(self):
        users = self.all_users()
        for u in users:
            print(f"substract {u.uuid} hold")
            u.substract_hold()
            self.update_hold(u)
            self.update_balance(u)

    def add_money_to_sub(self, uuid, sum):
        user = self.select_user_by_uuid(uuid)
        user.add(sum)
        print(
            f"add {sum} to {user.uuid}, now balance is {user.balance}")
        self.update_balance(user)

    def substract_money_from_sub(self, uuid, sum):
        user = self.select_user_by_uuid(uuid)
        user.substract(sum)
        print(f"sub {sum} from {user.uuid}, now hold is {user.hold}")
        self.update_hold(user)

    def all_users(self):
        self.cursor.execute("select * from subscribers;")
        records = self.cursor.fetchall()
        subscribers = set()
        for u in records:
            sub = Subscriber(u[0], u[1], u[2], u[3], u[4] == 1)
            subscribers.add(sub)
        return subscribers

    def select_user_by_uuid(self, uuid):
        self.cursor.execute(
            'select * from subscribers where "uuid"= %s', (str(uuid),))
        u = self.cursor.fetchone()
        if u is None:
            raise e.UserNotFoundException
        sub = Subscriber(u[0], u[1], u[2], u[3], u[4] == 1)
        return sub

    def load_from_jsonfile(self, filename="server/example.json"):
        subscribers = get_subs_set_from_json(filename)
        for u in subscribers:
            print(f"subsriber from jsonfile: {u}")
        self.insert_multiple_subscriber(subscribers)
        return self.all_users()

    def load_from_json(self, json_with_subs_list):
        subscribers = get_subs_set_from_json(json_with_subs_list)
        for u in subscribers:
            print(f"subsriber from json: {u}")
        self.insert_multiple_subscriber(subscribers)
        return self.all_users()

    def dump_users_to_dict_for_json(self):
        subs = []
        users = self.all_users()
        for u in users:
            subs.append(u.dict_for_json())
        return subs
