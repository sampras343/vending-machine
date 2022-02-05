from source.resources.racks import Racks
import unittest

class test_Racks(unittest.TestCase):
    def test_get(self):
        result = Racks.get(self)
        expected = {'hello': 'world'}
        assert result == expected