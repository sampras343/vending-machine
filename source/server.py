try:
    from flask import Flask, Blueprint
    from flask_restful import Api
    from flask_cors import CORS
    from config import HOST, DEBUG, PORT
    from resources.racks import Racks
    from resources.machine_models import MachineModelClass, Advanced_MachineModel_Class
except (ModuleNotFoundError, ImportError):
    from .config import HOST, DEBUG, PORT
    from .resources.racks import Racks
    from .resources.machine_models import MachineModelClass, Advanced_MachineModel_Class


server = Flask(__name__)
CORS(server)

api = Api(server)

blueprint = Blueprint('api', __name__, url_prefix='/vending-machine/api/v1')
server.register_blueprint(blueprint)

api.add_resource(Racks, '/racks', endpoint='racks')
api.add_resource(MachineModelClass, '/machine-models', endpoint='machine-models')
api.add_resource(Advanced_MachineModel_Class, '/machine-models/<string:modelId>', endpoint='adv-machine-models')


server.debug = DEBUG
print("Server started on : ", HOST, ":", PORT)

if __name__ == "__main__":
    server.run(host=HOST, port=PORT)
