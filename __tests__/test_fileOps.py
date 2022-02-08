import os
from unittest import mock, TestCase
from source.util.fileOps import loadJSONFile, writeJSONFile
from source.util.constants import Constants


# @mock.patch('source.util.fileOps.constants.Constants.APP_STORAGE_PATH', return_value = str('__tests__/dummyFiles/'))
class Test_FileOps(TestCase):

    def setUp(self) -> None:
        Constants.APP_STORAGE_PATH = '__tests__/dummyFiles/'

    def tearDown(self) -> None:
        Constants.APP_STORAGE_PATH = 'source/storage'
    
    def test_loadJSONFile(self) -> None:
        '''File found in the required location'''
        # GIVEN: To read from any file provided
        # WHEN: the file is present in the storage and not corrupted 
        # THEN: Read and return it's contents & True
        resultPositive = loadJSONFile('config.json')
        self.assertEqual(resultPositive[0], True)

        '''File not found in the required location'''
        # GIVEN: To read from any file provided
        # WHEN: the file is NOT present in the storage
        # THEN: Return default contents & False
        resultNegative = loadJSONFile('noFile.json')
        expected1 = (False, {})
        self.assertEqual(resultNegative, expected1)

        '''File not found in the required location'''
        # GIVEN: To read from any file provided
        # WHEN: the file is present in the storage but corrupted
        # THEN: Return default contents & False
        resultCorrupted = loadJSONFile('corrupted.json')
        expected2 = (False, {})
        self.assertEqual(resultCorrupted, expected2)

    def test_writeJSONFile(self):
        fileName = 'xyz.json'
        filePath = Constants.APP_STORAGE_PATH + fileName
        '''TEST 1: Write Successful'''
        # GIVEN: To write JSON contents onto any file 
        # WHEN: the file is/is not present in the storage
        # THEN: Write the file with desired Contents
        resultPositive = writeJSONFile({}, fileName)
        expected1 = True
        self.assertEqual(resultPositive, expected1)
        validateFileContents = loadJSONFile(fileName)
        expected1Data = (True, {})
        self.assertEqual(validateFileContents, expected1Data)
        os.remove(filePath)