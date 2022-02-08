from os import path
import unittest
from source.util.constants import Constants
import json
from source.server import server


class Test_MachineModelClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self) -> None:
        Constants.APP_STORAGE_PATH = '__tests__/dummyFiles/'

    def tearDown(self) -> None:
        Constants.APP_STORAGE_PATH = 'source/storage'

    def test_get(self):
        ''' TEST 1 :: File not found '''
        # GIVEN: the user wants to obtain the list of models
        # WHEN: GET method is called & the app is not initialized
        # THEN: Empty array should be returned
        Constants.APP_STORAGE_PATH = 'a/b/'
        
        response = self.client.get("/machine-models")
        self.assertEqual(response.status_code, 200)
        response_json = json.loads(response.data.decode("utf-8"))
        
        expectedEmpty = {
            'models': [],
            'page': {
                'number': 1,
                'size': 0,
                'total-elements': 0,
                'total-pages': 1
            }
        }
        self.assertEqual(response_json, expectedEmpty)

        ''' TEST 2 :: File found, no pagination '''
        # GIVEN: the user wants to obtain the list of models
        # WHEN: GET method is called without query params
        # THEN: Data should be returned with default pagination
        Constants.APP_STORAGE_PATH = '__tests__/dummyFiles/'
        expectedFile = {
            'models': [
                {
                    "created-at": "time",
                    "last-modified-at": "time",
                    "name": "model A",
                    "id": "modelA_id1",
                    "racks": {
                            "max-racks": 10,
                            "max-products-per-rack": 10
                    }
                }
            ],
            'page': {
                'number': 1,
                'size': 1,
                'total-elements': 1,
                'total-pages': 1
            }
        }
        
        response2 = self.client.get("/machine-models")
        response_json2 = json.loads(response2.data.decode("utf-8"))
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(expectedFile, response_json2)

        ''' TEST 3 :: File found, pagination provided'''
        # GIVEN: the user wants to obtain the list of models
        # WHEN: GET method is called with custom query params of pagination
        # THEN: Data should be returned with requested pagination
        Constants.APP_STORAGE_PATH = '__tests__/dummyFiles/'
        expectedData = {
            'models': [
                {
                    "created-at": "time",
                    "last-modified-at": "time",
                    "name": "model A",
                    "id": "modelA_id1",
                    "racks": {
                            "max-racks": 10,
                            "max-products-per-rack": 10
                    }
                }
            ],
            'page': {
                'number': 1,
                'size': 10,
                'total-elements': 1,
                'total-pages': 1
            }
        }
        
        url = 'http://example.com/machine-models?page=1&size=10'
        response3 = self.client.get(url)
        response_json3 = json.loads(response3.data.decode("utf-8"))
        print("response_json3", response_json3)
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(expectedData, response_json3)

    def test_post(self):
        ''' TEST 1 :: Invalid Input provided '''
        # GIVEN: Invalid schema is provided
        # WHEN: POST method is called
        # THEN: Error stating with 422 Response code should be returned
        response = self.client.post("/machine-models", content_type="application/json", data=json.dumps({}))
        self.assertEqual(response.status_code, 422)
        response_json = json.loads(response.data.decode("utf-8"))
        expectedMessage = 'Invalid Input'
        self.assertEqual(response_json['errors']['message'], expectedMessage)