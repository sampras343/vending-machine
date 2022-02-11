"""
Define the REST verbs relative to the Machine Models
"""
import logging
import json
import math
import warlock
import uuid
from datetime import datetime 
from flask_restful import Resource
from flask import request, Response
from flask_restful.reqparse import Argument

try:
    from util import fileOps, Constants, Validate, ErrorClass
    from util.schemas import machine_model_schema, error_schema
    from .machine_objects import CreateMachineModelObject
except (ModuleNotFoundError, ImportError):
    from source.util.schemas import machine_model_schema, error_schema
    from source.util import fileOps, Constants, Validate, ErrorClass
    from source.resources.machine_models.machine_objects import CreateMachineModelObject


        


class MachineModelClass(Resource, CreateMachineModelObject):
    def __init__(self):
        pass

    def get(self):
        try:
            modStatus, modelInfo = fileOps.loadJSONFile(
                Constants.MACHINE_MODEL_CONFIG_FILE)
            pageObj = warlock.model_factory(machine_model_schema.PAGINATION)
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
            outputConfig['page']['total-elements'] = len(
                modelInfo['machine-model-details'])
            outputConfig['page']['total-pages'] = 1
            queryStr = json.loads(json.dumps(request.args))
            if 'page' not in queryStr.keys() or 'size' not in queryStr.keys():
                return outputConfig
            if queryStr['page'] != None and queryStr['size'] != None:
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
            err = ErrorClass('Something went wrong', 'something.wrong.get.models')
            return Response(json.dumps({'errors': err.generateErr()}), status=502, mimetype='application/json')

    def post(self):
        try:
            requestObj = request.get_json(force=True)
            v = Validate(requestObj, machine_model_schema.POST_REQ_MODEL)
            if v.validate() == False:
                err = ErrorClass('Invalid Input', 'models.post.invalid.input')
                return Response(json.dumps({'errors': err.generateErr()}), status=422, mimetype='application/json')
            generatedObject = CreateMachineModelObject().generateNewObject(requestObj)
            modelState, modelInfo = fileOps.loadJSONFile(Constants.MACHINE_MODEL_CONFIG_FILE)
            if not modelState:
                logging.info('First Entry to be made')
                machine_model = []
                machine_model.append(generatedObject)
                fileWriteObj = {
                    'machine-model-details': machine_model
                }
                fileOps.writeJSONFile(fileWriteObj, Constants.MACHINE_MODEL_CONFIG_FILE)
                logging.info('POST Model Operation Successful')
                return Response(json.dumps(generatedObject), status=200, mimetype='application/json')

            isModelExists = [x for x in modelInfo['machine-model-details'] if x["name"] == generatedObject["name"] ]
            if len(isModelExists):
                logging.error('Cannot add duplicates')
                err = ErrorClass('Entry available. Cannot add duplicates', 'models.post.duplicates')
                return Response(json.dumps({'errors': err.generateErr()}), status=400, mimetype='application/json')
            logging.info('No duplicates. Allowed to add')
            modelInfo['machine-model-details'].append(generatedObject)
            fileOps.writeJSONFile(modelInfo, Constants.MACHINE_MODEL_CONFIG_FILE)
            logging.info('POST Model Operation Successful')
            return Response(json.dumps(generatedObject), status=200, mimetype='application/json')
        except Exception as e:
            logging.error(e)
            err = ErrorClass('Something wrong', 'models.post.exception')
            return Response(json.dumps({'errors': err.generateErr()}), status=502, mimetype='application/json')
