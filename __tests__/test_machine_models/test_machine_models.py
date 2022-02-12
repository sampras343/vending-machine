from os import path
import unittest
from source.util.constants import Constants
import json
from source.server import server
import os


class Test_MachineModelClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

    def setUp(self) -> None:
        Constants.APP_STORAGE_PATH = '__tests__/dummyFiles/'
        defaultTestData = {
            "machine-model-details": [
                {
                    "created-at": "time",
                    "last-modified-at": "time",
                    "name": "model A",
                    "id": "modelA_id1",
                    "racks": {
                        "max-racks": 10,
                        "max-products-per-rack": 10
                    },
                    "quantity": {
                        "total": 5,
                        "active": 2,
                        "inactive": 2,
                        "damaged": 1,
                        "archived": 1
                    }
                }
            ]
        }
        path_to_file = Constants.APP_STORAGE_PATH + Constants.MACHINE_MODEL_CONFIG_FILE
        with open(path_to_file, "w") as outfile:
            json.dump(defaultTestData, outfile, indent=4)

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
        self.assertEqual(response3.status_code, 200)
        self.assertEqual(expectedData, response_json3)

        ''' TEST 4 :: File Schema corrupted '''
        # GIVEN: the user wants to obtain the list of models
        # WHEN: GET method is called 
        # AND: the file data is corrupted
        # THEN: the catch block should be triggered
        corruptedData = {}
        path_to_file = Constants.APP_STORAGE_PATH + Constants.MACHINE_MODEL_CONFIG_FILE
        with open(path_to_file, "w") as outfile:
            json.dump(corruptedData, outfile, indent=4)
        url = 'http://example.com/machine-models?page=1&size=10'
        response4 = self.client.get(url)
        response_json4 = json.loads(response4.data.decode("utf-8"))
        expectedMessage4 = 'Something went wrong'
        self.assertEqual(response4.status_code, 502)
        self.assertEqual(response_json4['errors']['message'], expectedMessage4)

    def test_post(self):
        ''' TEST 1 :: Invalid Input provided '''
        # GIVEN: Invalid schema is provided
        # WHEN: POST method is called
        # THEN: Error stating with 422 Response code should be returned
        response = self.client.post(
            "/machine-models", content_type="application/json", data=json.dumps({}))
        self.assertEqual(response.status_code, 422)
        response_json = json.loads(response.data.decode("utf-8"))
        expectedMessage = 'Invalid Input'
        self.assertEqual(response_json['errors']['message'], expectedMessage)

        ''' TEST 2 :: Cannot add Duplicates  '''
        # GIVEN: A valid input is provided
        # WHEN: POST method is called
        # AND: the model is already registered
        # THEN: Error stating that the model cannot be registerd as it is already available
        inputData1 = {
            "name": "model A",
            "quantity": 10,
            "racks": {
                "max-racks": 10,
                "max-products-per-rack": 10
            }
        }
        response1 = self.client.post(
            "/machine-models", content_type="application/json", data=json.dumps(inputData1))
        self.assertEqual(response1.status_code, 400)
        response_json1 = json.loads(response1.data.decode("utf-8"))
        expectedMessage1 = 'Entry available. Cannot add duplicates'
        self.assertEqual(response_json1['errors']['message'], expectedMessage1)

        ''' TEST 3 :: Successfully registered model  '''
        # GIVEN: A valid input is provided
        # WHEN: POST method is called
        # AND: the model is not available already
        # THEN: the model should be successfully registered
        inputData2 = {
            "name": 'Test_ModelA',
            "quantity": 10,
            "racks": {
                "max-racks": 10,
                "max-products-per-rack": 10
            }
        }
        response2 = self.client.post(
            "/machine-models", content_type="application/json", data=json.dumps(inputData2))
        self.assertEqual(response2.status_code, 200)
        response_json2 = json.loads(response2.data.decode("utf-8"))
        expectedMessage2 = inputData2['name']
        self.assertEqual(response_json2['name'], expectedMessage2)

        ''' TEST 4 :: Something went wrong  '''
        # GIVEN: A valid input is provided
        # WHEN: POST method is called
        # AND: the model is not available already
        # AND: the json schema is corrupted
        # THEN: the catch block should be called
        inputData3 = {
            "name": 'Test_ModelAB',
            "quantity": 10,
            "racks": {
                "max-racks": 10,
                "max-products-per-rack": 10
            }
        }
        corruptedData = {}
        path_to_file = Constants.APP_STORAGE_PATH + Constants.MACHINE_MODEL_CONFIG_FILE
        with open(path_to_file, "w") as outfile:
            json.dump(corruptedData, outfile, indent=4)
        response3 = self.client.post("/machine-models", content_type="application/json", data=json.dumps(inputData3))
        self.assertEqual(response3.status_code, 502)
        response_json3 = json.loads(response3.data.decode("utf-8"))
        expectedMessage3 = 'Something wrong'
        self.assertEqual(response_json3['errors']['message'], expectedMessage3)

        ''' TEST 5 :: First Entry to be made  '''
        # GIVEN: A valid input is provided
        # WHEN: POST method is called
        # AND: the model is not available already
        # AND: the json schema is corrupted
        # THEN: the catch block should be called
        inputData4 = {
            "name": 'Test_ModelABCS',
            "quantity": 10,
            "racks": {
                "max-racks": 10,
                "max-products-per-rack": 10
            }
        }
        os.remove(Constants.APP_STORAGE_PATH + Constants.MACHINE_MODEL_CONFIG_FILE)
        response4 = self.client.post("/machine-models", content_type="application/json", data=json.dumps(inputData4))
        self.assertEqual(response4.status_code, 200)
        response_json4 = json.loads(response4.data.decode("utf-8"))
        self.assertEqual(response_json4['name'], inputData4['name'])
        # fileName = 'xyz.json'
        # path_to_file = Constants.APP_STORAGE_PATH + fileName
        # os.remove(path_to_file)