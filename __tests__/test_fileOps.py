from unittest import mock, TestCase
from source.util.fileOps import loadJSONFile
from source.util.constants import Constants


# @mock.patch('source.util.fileOps.constants.Constants.APP_STORAGE_PATH', return_value = str('__tests__/dummyFiles/'))
class Test_FileOps(TestCase):

    def setUp(self) -> None:
        Constants.APP_STORAGE_PATH = '__tests__/dummyFiles/'

    def tearDown(self) -> None:
        Constants.APP_STORAGE_PATH = 'source/storage'
    
    def test_loadJSONFile(self) -> None:
        '''File found in the required location'''
        resultPositive = loadJSONFile('config.json')
        self.assertEqual(resultPositive[0], True)

        '''File not found in the required location'''
        resultNegative = loadJSONFile('noFile.json')
        expected = (False, {})
        self.assertEqual(resultNegative, expected)


