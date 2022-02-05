"""
Define the REST verbs relative to the Racks
"""
from flask_restful import Resource, reqparse
from util import parse_params
from flask.json import jsonify
from flask_restful.reqparse import Argument

class Racks(Resource):
    def __init__(self):
        pass
    def get(self):
        return {'hello': 'world'}

    
    @parse_params(
        Argument("name", location="json", required=True),
        Argument("id", location="json", required=True)
    )
    def post(self, **kwargs):
        print("Name", kwargs)
        return {'method': 'post'}