"""
Define the REST APIs relative to the Advanced Machine Models
Routes: GET,PUT,PATCH /models/{id}
"""

import logging
import json
from flask_restful import Resource
from flask import request, Response

try:
    from util import fileOps, Constants, Validate, ErrorClass
    from util.schemas import machine_model_schema
    from .machine_objects import CreateMachineModelObject
except (ModuleNotFoundError, ImportError):
    from source.util.schemas import machine_model_schema
    from source.util import fileOps, Constants, Validate, ErrorClass
    from source.resources.machine_models.machine_objects import CreateMachineModelObject



class Advanced_MachineModel_Class(Resource):
    def __init__(self):
        pass

    def get(self, modelId):
        try:
            notfoundErr = ErrorClass('Model Not found', 'notFound.get.models.id')
            modStatus, modelInfo = fileOps.loadJSONFile(Constants.MACHINE_MODEL_CONFIG_FILE)
            if not modStatus:
                logging.error('File not found. Hence ID cannot be retrieved')
                return Response(json.dumps({'errors': notfoundErr.generateErr()}), status=404, mimetype='application/json')
            isModelExists = [x for x in modelInfo['machine-model-details'] if x["id"] == modelId ]
            if len(isModelExists):
                logging.info('Found Object')
                return Response(json.dumps(isModelExists[0]), status=200, mimetype='application/json')                
            logging.error('Model ID not found')
            return Response(json.dumps({'errors': notfoundErr.generateErr()}), status=404, mimetype='application/json')
        except Exception as e:
            logging.error(e)
            err = ErrorClass('Something went wrong', 'something.wrong.get.models')
            return Response(json.dumps({'errors': err.generateErr()}), status=502, mimetype='application/json')
           