"""
Define the REST verbs relative to the Racks
"""
from re import L
from flask_restful import Resource
from util import parse_params
from flask.json import jsonify
from flask_restful.reqparse import Argument
from util.fileOps import loadJSONFile
from util.constants import Constants

class Racks(Resource):
    def __init__(self):
        pass
    def get(self):
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