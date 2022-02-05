from flask import Flask
from flask_restful import Api
import config
from resources.racks import Racks
from flask_cors import CORS

server = Flask(__name__)
CORS(server)
api = Api(server)

api.add_resource(Racks, '/racks')

server.debug = config.DEBUG
print("Server started on : ", config.HOST,":",config.PORT)

if __name__ == "__main__":
    server.run(host=config.HOST, port=config.PORT)