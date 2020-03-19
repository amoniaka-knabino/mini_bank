from sys import argv
import json
import urllib.request
import unittest
import server.helpers.exceptions as e

#host = "localhost"
#host = "localhost:8000"
host = "167.172.155.67/"


def reload_db():
    with open('example.json', 'rb') as f:
        req = urllib.request.Request("http://"+host+"/api/refresh")
        urllib.request.urlopen(req)

        json_to_load_bytes = f.read()
    req = urllib.request.Request("http://"+host+"/api/load_db", data=json_to_load_bytes,
                                 headers={'content-type': 'application/json'})
    _ = urllib.request.urlopen(req)


def get_status_dict(uuid_str):
    newConditions = {"addition": {"uuid": uuid_str}}
    req = urllib.request.Request("http://"+host+"/api/status", data=json.dumps(newConditions).encode('utf-8'),
                                 headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    return json.loads(response.read().decode('utf8'))["addition"]


def get_subs_json_bytes():
    response = urllib.request.urlopen("http://"+host+"/api/subs")
    return response.read()


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_backup = get_subs_json_bytes()

    @classmethod
    def tearDownClass(cls):
        req = urllib.request.Request("http://"+host+"/api/refresh")
        urllib.request.urlopen(req)
        req = urllib.request.Request("http://"+host+"/api/load_db", data=cls.db_backup,
                                     headers={'content-type': 'application/json'})
        _ = urllib.request.urlopen(req)

    def test_load(self):
        with open('example.json', 'rb') as f:
            req = urllib.request.Request("http://"+host+"/api/refresh")
            urllib.request.urlopen(req)

            json_to_load_bytes = f.read()
        json_to_load = json.loads(json_to_load_bytes)
        req = urllib.request.Request("http://"+host+"/api/load_db",
                                     data=json_to_load_bytes,
                                     headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        json_from_api = json.loads(response.read().decode('utf8'))

        equals = 0
        for d1 in json_to_load["addition"]:
            for d2 in json_from_api["addition"]:
                if (d1["uuid"] == d2["uuid"]):
                    if (d1 == d2):
                        equals += 1
        self.assertEqual(len(json_to_load["addition"]), equals)

    def test_add(self):
        reload_db()
        delta = 10
        uuid = "26c940a1-7228-4ea2-a3bc-e6460b172040"

        user_dict = get_status_dict(uuid)
        old_balance = user_dict["balance"]

        newConditions = {"addition": {"uuid": uuid, "sum": delta}}
        req = urllib.request.Request("http://"+host+"/api/add",
                                     data=json.dumps(newConditions).encode('utf-8'),
                                     headers={'content-type': 'application/json'})
        _ = urllib.request.urlopen(req)

        user_dict = get_status_dict(uuid)
        new_balance = user_dict["balance"]
        self.assertEqual(old_balance+delta, new_balance)

    def test_substract(self):
        reload_db()
        delta = 10
        uuid = "26c940a1-7228-4ea2-a3bc-e6460b172040"

        user_dict = get_status_dict(uuid)
        old_hold = user_dict["hold"]
        newConditions = {"addition": {"uuid": uuid, "sum": delta}}
        req = urllib.request.Request("http://"+host+"/api/substract",
                                     data=json.dumps(newConditions).encode('utf-8'),
                                     headers={'content-type': 'application/json'})
        _ = urllib.request.urlopen(req)

        user_dict = get_status_dict(uuid)
        new_hold = user_dict["hold"]
        self.assertEqual(old_hold+delta, new_hold)

    def test_negative_sum(self):
        reload_db()
        code = 200
        try:
            newConditions = {"addition": {
                "uuid": "26c940a1-7228-4ea2-a3bc-e6460b172040", "sum": -10}}
            req = urllib.request.Request("http://"+host+"/api/add",
                                         data=json.dumps(newConditions).encode('utf-8'),
                                         headers={'content-type': 'application/json'})
            _ = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            code = e.code
        self.assertEqual(code, 400)

    def test_closed_acc(self):
        reload_db()
        code = 200
        uuid = "867f0924-a917-4711-939b-90b179a96392"
        try:
            newConditions = {"addition": {
                "uuid": uuid, "sum": 10}}
            req = urllib.request.Request("http://"+host+"/api/add",
                                         data=json.dumps(newConditions).encode('utf-8'),
                                         headers={'content-type': 'application/json'})
            _ = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            code = e.code
        self.assertEqual(code, 403)
