import json
import unittest

from src.pyfootballdata.structs import Head2Head


class TestHead2Heads(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        head2heads_file = open("data/h2h.json")
        head2heads_dictionary = json.load(head2heads_file)
        cls.head2heads = Head2Head(head2heads_dictionary)
        head2heads_file.close()

    def test_head2heads_instance(self):
        self.assertIsInstance(
            self.head2heads, Head2Head, "Head2Head should be an instance of Head2Head"
        )

    def test_head2heads_average_goals(self):
        average_goals = self.head2heads.average_goals
        self.assertIsNotNone(average_goals, "Average goals should not be None")
        self.assertTrue(average_goals > 1.0, "Average goals should be greater than 1.0")
