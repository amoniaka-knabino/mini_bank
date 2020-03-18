from sys import argv
import json, urllib.request
import unittest

host = "localhost:8000"
#host = "167.172.155.67/

class TestAPI(unittest.TestCase):
    def test_load(self):
        with open('example.json', 'rb') as f:
            req = urllib.request.Request("http://"+host+"/api/refresh")
            urllib.request.urlopen(req)

            json_to_load_bytes = f.read()
        json_to_load = json.loads(json_to_load_bytes)
        req = urllib.request.Request("http://"+host+"/api/load_db", data=json_to_load_bytes,
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
                        


