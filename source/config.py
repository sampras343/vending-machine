import logging
import os

DEBUG = os.getenv("ENVIRONEMENT") == "DEV"
APPLICATION_ROOT = os.getenv("APPLICATION_ROOT", "/vending-machine")
HOST = os.getenv("APPLICATION_HOST", '0.0.0.0')
PORT = int(os.getenv("APPLICATION_PORT", "3001"))


logging.basicConfig(
    filename=os.getenv("SERVICE_LOG", "vending-machine.log"),
    level=logging.DEBUG,
    format="%(levelname)s: %(asctime)s \
        pid:%(process)s module:%(module)s %(message)s",
    datefmt="%d/%m/%y %H:%M:%S",
)
