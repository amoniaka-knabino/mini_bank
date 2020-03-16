import json
import unittest
from Database import Database
from Subscriber import Subscriber, get_subs_set_from_json, generate_user
import os

class TestDB(unittest.TestCase):
    db_name = "test.db"
    filename = "example.json"
    def test_loading_count(self):
        db = Database(self.db_name)
        self.assertEqual(len(db.all_users()), 0)
        db.load_from_json(self.filename)
        subs_from_db = db.all_users()
        with open(self.filename) as f:
            subs_from_json = json.loads(f.read())
        self.assertTrue(len(subs_from_db), len(subs_from_json))
        os.remove(self.db_name)
    
    def test_loading_by_uuids(self):
        db = Database(self.db_name)
        self.assertEqual(len(db.all_users()), 0)
        db.load_from_json(self.filename)
        subs_from_db = db.all_users()
        subs_from_json = get_subs_set_from_json(self.filename)
        self.assertEqual(len(subs_from_db), len(subs_from_json))
        self.assertEqual(subs_from_db, subs_from_json)
        os.remove(self.db_name)
    
    def test_update(self):
        db = Database(self.db_name)
        self.assertEqual(len(db.all_users()), 0)
        u = generate_user(0,0,True)
        db.update_or_add_one_subscriber(u)
        u.add(100)
        db.update_or_add_one_subscriber(u)
        users = db.all_users()
        self.assertEqual(len(users),1)
        db_u = users.pop()
        self.assertEqual(u, db_u)
        os.remove(self.db_name)
    
    
            
        