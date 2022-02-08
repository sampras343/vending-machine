import logging
import jsonschema
import logging

class Validate():
    def __init__(self, instance = {}, schema = {}):
        self.instance = instance
        self.schema = schema
        pass
    def validate(self):
        try:
            jsonschema.validate(instance=self.instance, schema=self.schema)
        except jsonschema.exceptions.ValidationError as e:
            logging.error('Invalid JSON Schema ')
            return False
        return True

