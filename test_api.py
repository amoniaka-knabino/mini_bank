from sys import argv
import json, urllib.request
import unittest
import server.helpers.exceptions as e

host = "localhost:8000"
#host = "167.172.155.67/"
def reload_db():
    with open('example.json', 'rb') as f:
        req = urllib.request.Request("http://"+host+"/api/refresh")
        urllib.request.urlopen(req)

        json_to_load_bytes = f.read()
    req = urllib.request.Request("http://"+host+"/api/load_db", data=json_to_load_bytes,
                                headers={'content-type': 'application/json'})
    _ = urllib.request.urlopen(req)

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
    
    def test_add(self):
        pass
    
    def test_substract(self):
        pass

    def test_negative_sum(self):
        reload_db()
        with self.assertRaises(urllib.error.HTTPError):
            newConditions = {"addition":{"uuid":"26c940a1-7228-4ea2-a3bc-e6460b172040", "sum":-10}}  
            req = urllib.request.Request("http://"+host+"/api/add", data=json.dumps(newConditions).encode('utf-8'),
                                    headers={'content-type': 'application/json'})
            _ = urllib.request.urlopen(req)
        

    def test_closed_acc(self):
        reload_db()
        with self.assertRaises(urllib.error.HTTPError):
            newConditions = {"addition":{"uuid":"867f0924-a917-4711-939b-90b179a96392", "sum":10}}  
            req = urllib.request.Request("http://"+host+"/api/add", data=json.dumps(newConditions).encode('utf-8'),
                                    headers={'content-type': 'application/json'})
            _ = urllib.request.urlopen(req)
                        


