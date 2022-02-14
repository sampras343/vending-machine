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
        Constants.APP_STORAGE_PATH = 'source/storage/'

    def test_get(self):
        ''' TEST 1 :: Model found and retrieved '''
        # GIVEN: the user wants to obtain a specific model
        # WHEN: GET method is called along with the model id
        # AND: the model is available
        # THEN: Model info should be returned
        response1 = self.client.get("/machine-models/modelA_id1")
        self.assertEqual(response1.status_code, 200)
        response_json1 = json.loads(response1.data.decode("utf-8"))
        expectedResp = {
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
        self.assertEqual(response_json1, expectedResp)

        ''' TEST 2 :: Model not found '''
        # GIVEN: the user wants to obtain a specific model 
        # WHEN: GET method is called along with the model id
        # AND: the model is not registered
        # THEN: Model ID not found should be returned

        response2 = self.client.get("/machine-models/id-123")
        self.assertEqual(response2.status_code, 404)
        response_json2 = json.loads(response2.data.decode("utf-8"))
        expectedErr = 'Model Not found'
        self.assertEqual(response_json2['errors']['message'], expectedErr)

        ''' TEST 3 :: Something went wrong '''
        # GIVEN: the user wants to obtain a specific model
        # WHEN: GET method is called along with the model id
        # AND: the underlying file is corrupted
        # THEN: Something wrong should be returned from catch block
        corruptedData = {}
        path_to_file = Constants.APP_STORAGE_PATH + Constants.MACHINE_MODEL_CONFIG_FILE
        with open(path_to_file, "w") as outfile:
            json.dump(corruptedData, outfile, indent=4)
        response4 = self.client.get("/machine-models/id-123")
        self.assertEqual(response4.status_code, 502)
        response_json4 = json.loads(response4.data.decode("utf-8"))
        expectedErr = 'Something went wrong'
        self.assertEqual(response_json4['errors']['message'], expectedErr)

        ''' TEST 4 :: File not found '''
        # GIVEN: the user wants to obtain a specific model
        # WHEN: GET method is called along with the model id
        # AND: the app is not initialized
        # THEN: Model ID not found should be returned
        Constants.APP_STORAGE_PATH = 'a/b/c/'
        response3 = self.client.get("/machine-models/id-123")
        self.assertEqual(response3.status_code, 404)
        response_json3 = json.loads(response3.data.decode("utf-8"))
        expectedErr = 'Model Not found'
        self.assertEqual(response_json3['errors']['message'], expectedErr)