import json
import unittest

from src.pyfootballdata.structs import Scorers


class TestScorers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scorers_file = open("data/scorers_epl_top_20_2020.json")
        scorers_dictionary = json.load(scorers_file)
        cls.scorers = Scorers(scorers_dictionary)
        scorers_file.close()

    def test_scorers_instance(self):
        self.assertIsInstance(
            self.scorers, Scorers, "Scorers should be an instance of Scorers"
        )
        scorer = self.scorers[0]
        self.assertEqual(scorer.name, "Harry Kane", "Top scorer should be Harry Kane")
        self.assertEqual(
            scorer.nationality.title, "England", "Top scorer should be from English"
        )
        self.assertEqual(
            scorer.team.name,
            "Tottenham Hotspur FC",
            "Top scorer should be from Tottenham Hotspur FC",
        )
