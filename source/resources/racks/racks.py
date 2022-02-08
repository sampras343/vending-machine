"""
Define the REST verbs relative to the Racks
"""
import json
from flask_restful import Resource
from flask_restful.reqparse import Argument
from flask import request

try:
    from util.parse_params import parse_params
    from util.fileOps import loadJSONFile
    from util.constants import Constants
except (ModuleNotFoundError, ImportError):
    from source.util.fileOps import loadJSONFile
    from source.util.constants import Constants   
    from source.util.parse_params import parse_params 

class Racks(Resource):
    def __init__(self):
        pass
    def get(self):
        queryStr = json.dumps(request.args)
        print("GET Args Racks", queryStr)
        rackStatus, configInfo = loadJSONFile(Constants.CONFIG_FILE)
        if not rackStatus:
            return []
        return configInfo

    @parse_params(
        Argument("name", location="json", required=True),
        Argument("id", location="json", required=True)
    )
    def post(self, **kwargs):
        print("Name", kwargs)
        return {'method': 'post'}