import json
import unittest

from src.pyfootballdata.structs import Competitions, Competition


class TestCompetitions(unittest.TestCase):
    def setUp(self):
        competitions_file = open("data/competitions.json")
        competitions_dictionary = json.load(competitions_file)
        self.competitions = Competitions(competitions_dictionary)
        competitions_file.close()

        competition_file = open("data/competition_epl.json")
        competition_dictionary = json.load(competition_file)
        self.competition = Competition(competition_dictionary)
        competition_file.close()

    def test_competitions_instance(self):
        self.assertIsInstance(
            self.competitions, Competitions, "Competitions should be an instance of Competitions"
        )

    def test_competition_instance(self):
        self.assertIsInstance(
            self.competition, Competition, "Competition should be an instance of Competition"
        )
