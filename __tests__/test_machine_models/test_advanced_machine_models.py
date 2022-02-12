from os import path
import unittest
from source.util.constants import Constants
import json
from source.server import server
import os


class Test_MachineModelClass(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = server.test_client()

        