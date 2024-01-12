import json
import unittest
from src.pyfootballdata.structs import Areas, Area


class TestAreas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        areas_file = open("data/areas.json")
        areas_dictionary = json.load(areas_file)
        cls.areas = Areas(areas_dictionary)
        areas_file.close()

        area_file = open("data/area.json")
        area_dictionary = json.load(area_file)
        cls.area = Area(area_dictionary)
        area_file.close()

    def test_areas_instance(self):
        self.assertIsInstance(self.areas, Areas, "Areas should be an instance of Areas")

    def test_area_instance(self):
        self.assertIsInstance(self.area, Area, "Area should be an instance of Area")
