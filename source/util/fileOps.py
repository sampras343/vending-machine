import json
from os.path import exists
from . import constants
import logging

def loadJSONFile(fileName):
    try:
        path_to_file = constants.Constants.APP_STORAGE_PATH + fileName
        if exists(path_to_file):
            logging.info('File Exists : '+ str(path_to_file))
            f = open(path_to_file)
            data = json.load(f)
            print(data)
            logging.info('File Read : '+ str(data))
            f.close()
            logging.info('File Closed : '+ str(path_to_file))
            return True, data
        else:
            logging.warning('File Does not Exists  : '+ str(path_to_file))
            return False, {}
    except Exception:
        logging.error('File Corrupted')
        return False, {}

def writeJSONFile(data, fileName):
    path_to_file = constants.Constants.APP_STORAGE_PATH + fileName
    with open(path_to_file, "w") as outfile:
        json.dump(data, outfile, indent=4)
    return True
