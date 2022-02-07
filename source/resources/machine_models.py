"""
Define the REST verbs relative to the Machine Models
"""
try:
    import logging
    from flask_restful import Resource
    from flask import request
    import json
    import math
    import warlock
    from util import fileOps, Constants, ErrorClass, PAGINATION
except (ModuleNotFoundError, ImportError):
    from source.util import fileOps, Constants, ErrorClass, PAGINATION



class MachineModelClass(Resource):
    def __init__(self):
        pass

    def get(self):
        try:
            modStatus, modelInfo = fileOps.loadJSONFile(Constants.MACHINE_MODEL_CONFIG_FILE)
            pageObj = warlock.model_factory(PAGINATION)
            if not modStatus:
                logging.warning('File not found')
                output = {
                    'models': [],
                    'page': pageObj(number=1, size=0)
                }
                output['page']['total-elements'] = 0
                output['page']['total-pages'] = 1
                return output
            for x in modelInfo['machine-model-details']:
                del x['quantity']
            outputConfig = {
                'models': modelInfo['machine-model-details'],
                'page': pageObj(number=1, size=len(modelInfo['machine-model-details']))
            }
            outputConfig['page']['total-elements'] = len(modelInfo['machine-model-details'])
            outputConfig['page']['total-pages'] = 1
            queryStr = json.loads(json.dumps(request.args))
            print("queryStr :::::::::::::::::::::: queryStr", queryStr)
            if 'page' not in queryStr.keys() or 'size' not in queryStr.keys():
                print("queryStr :::::::::::::::::::::: KEYS", queryStr)
                return outputConfig
            if queryStr['page'] != None and queryStr['size'] != None:
                print("queryStr :::::::::::::::::::::: IF", queryStr)
                outputConfig['page']['number'] = int(queryStr['page'])
                outputConfig['page']['size'] = int(queryStr['size'])
                outputConfig['page']['total-pages'] = math.ceil(
                    len(modelInfo['machine-model-details']) / int(queryStr['size']))
                outputConfig['models'] = outputConfig['models'][(int(
                    queryStr['page']) - 1) * int(queryStr['size']):int(queryStr['page']) * int(queryStr['size'])]
                logging.info('Obtained Paginated Output')
                return outputConfig
            logging.info('Obtained Non-Paginated Output')
            return outputConfig
        except Exception as e:
            logging.error(e)
            error = ErrorClass(e)
            return error.err()
