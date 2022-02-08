import logging
from datetime import datetime

class ErrorClass():
    def __init__(self, message, logref):
        self.message = message
        self.logref = logref
        
    def err(self):
        error = {
            'message': self.message,
            'timestamp': str(datetime.now().isoformat()),
            'logref': self.logref
        }
        return error