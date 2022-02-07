import json
from os.path import exists
from . import constants
import logging

def loadJSONFile(fileName):
    path_to_file = constants.Constants.APP_STORAGE_PATH + fileName
    if exists(path_to_file):
        logging.info('File Exists : '+ str(path_to_file))
        f = open(path_to_file)
        data = json.load(f)
        logging.info('File Read : '+ str(data))
        f.close()
        logging.info('File Closed : '+ str(path_to_file))
        return True, data
    else:
        logging.warning('File Does not Exists  : '+ str(path_to_file))
        return False, {}