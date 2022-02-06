import json
from os.path import exists
from . import constants

def loadJSONFile(fileName):
    path_to_file = constants.Constants.APP_STORAGE_PATH + fileName
    if exists(path_to_file):
        print('File Exists : ', path_to_file)
        f = open(path_to_file)
        data = json.load(f)
        print('File Read : ', data)
        f.close()
        print('File Closed : ', path_to_file)
        return True, data
    else:
        print('File Does not Exists : ', path_to_file)
        return False, {}