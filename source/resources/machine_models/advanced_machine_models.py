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
        modStatus, modelInfo = fileOps.loadJSONFile(Constants.MACHINE_MODEL_CONFIG_FILE)
        self.modStatus = modStatus
        self.modelInfo = modelInfo
        notfoundErr = ErrorClass('Model Not found', 'notFound.models.id')
        self.notfoundErr = json.dumps({'errors': notfoundErr.generateErr()})
        somethingWrong = ErrorClass('Something went wrong', 'something.wrong.get.models')
        self.somethingWrong = json.dumps({'errors': somethingWrong.generateErr()})
        pass

    def get(self, modelId):
        try:
            if not self.modStatus:
                logging.error('File not found. Hence ID cannot be retrieved')
                return Response(self.notfoundErr, status=404, mimetype='application/json')
            isModelExists = [x for x in self.modelInfo['machine-model-details'] if x["id"] == modelId]
            if len(isModelExists):
                logging.info('Found Object')
                return Response(json.dumps(isModelExists[0]), status=200, mimetype='application/json')
            logging.error('Model ID not found')
            return Response(self.notfoundErr, status=404, mimetype='application/json')
        except Exception as e:
            logging.error(e)
            return Response(self.somethingWrong, status=502, mimetype='application/json')

    def patch(self, modelId):
        try:
            if not self.modStatus:
                logging.error('File not found. Cannot edit')
                return Response(self.notfoundErr, status=404, mimetype='application/json')
            isModelExists = [x for x in self.modelInfo['machine-model-details'] if x["id"] == modelId]
            if not len(isModelExists):
                logging.error('Model ID not found')
                return Response(self.notfoundErr, status=404, mimetype='application/json')
            logging.info('Found Model Object')
            requestObj = request.get_json(force=True)
            if 'name' in requestObj and requestObj['name'] is not None:
                isModelExists[0]['name'] = requestObj['name']
            if 'racks' in requestObj and requestObj['racks'] is not None:
                if 'max-racks' in requestObj['racks'] and requestObj['racks']['max-racks'] is not None:
                    isModelExists[0]['racks']['max-racks'] = requestObj['racks']['max-racks']
                if 'max-products-per-rack' in requestObj['racks'] and requestObj['racks']['max-products-per-rack'] is not None:
                    isModelExists[0]['racks']['max-products-per-rack'] = requestObj['racks']['max-products-per-rack'] 
            fileOps.writeJSONFile(self.modelInfo, Constants.MACHINE_MODEL_CONFIG_FILE)
            return Response(json.dumps(isModelExists[0]), status=200, mimetype='application/json')
        except Exception as e:
            logging.error(e)
            err = ErrorClass('Something went wrong', 'something.wrong.get.models')
            return Response(json.dumps({'errors': err.generateErr()}), status=502, mimetype='application/json')
