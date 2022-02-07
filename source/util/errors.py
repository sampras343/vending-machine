import logging
from datetime import datetime

class ErrorClass():
    def __init__(self, message):
        self.message = message
        
    def err(self):
        error = {
            'message': self.message,
            'timestamp': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        return error