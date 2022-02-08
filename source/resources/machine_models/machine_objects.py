import warlock
import uuid
from datetime import datetime 

try:
    from util.schemas import machine_model_schema
except (ModuleNotFoundError, ImportError):
    from source.util.schemas import machine_model_schema


class CreateMachineModelObject():
    def __init__(self):
        pass
    def generateNewObject(self, requestObj):
        self.requestObj = requestObj
        createNewModelObject = warlock.model_factory(machine_model_schema.CREATE_MODEL)
        createQuantityModelObject = warlock.model_factory(machine_model_schema.CREATE_QUANTITY_MODEL)
        outputConfig = createNewModelObject (
            name = requestObj['name'],
            racks = requestObj['racks']
        )
        outputConfig['id'] = str(uuid.uuid4())
        outputConfig['created-at'] = str(datetime.now().isoformat())
        outputConfig['last-modified-at'] = str(datetime.now().isoformat())
        outputConfig['quantity'] = createQuantityModelObject (
            total=requestObj['quantity'],
            active=0,
            inactive=requestObj['quantity'],
            damaged=0,
            archived=0,
        )
        return outputConfig