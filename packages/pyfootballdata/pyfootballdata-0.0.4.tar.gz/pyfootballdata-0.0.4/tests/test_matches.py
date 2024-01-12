import json
import unittest

from src.pyfootballdata.structs import Matches


class TestMatches(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        matches_file = open("data/matches.json")
        matches_dictionary = json.load(matches_file)
        cls.matches = Matches(matches_dictionary)
        matches_file.close()

        matches_by_competition_file = open("data/matches_by_competition_epl_2020.json")
        matches_by_competition_dictionary = json.load(matches_by_competition_file)
        cls.matches_by_competition = Matches(matches_by_competition_dictionary)
        matches_by_competition_file.close()

        matches_by_team_file = open("data/matches_by_team.json")
        matches_by_team_dictionary = json.load(matches_by_team_file)
        cls.matches_by_team = Matches(matches_by_team_dictionary)
        matches_by_team_file.close()

        matches_by_person_file = open("data/matches_by_person.json")
        matches_by_person_dictionary = json.load(matches_by_person_file)
        cls.matches_by_person = Matches(matches_by_person_dictionary)
        matches_by_person_file.close()

    def test_matches_instance(self):
        self.assertIsInstance(
            self.matches, Matches, "Matches should be an instance of Matches"
        )

    def test_matches_by_competition_instance(self):
        self.assertIsInstance(
            self.matches_by_competition, Matches, "Matches should be an instance of Matches"
        )

    def test_matches_by_team_instance(self):
        self.assertIsInstance(
            self.matches_by_team, Matches, "Matches should be an instance of Matches"
        )

    def test_matches_by_person_instance(self):
        self.assertIsInstance(
            self.matches_by_person, Matches, "Matches should be an instance of Matches"
        )

    def test_some_matches_props(self):
        some_match = self.matches[0]
        self.assertEqual(
            some_match.competition.name, "Serie A", "Match competition name should be Serie A"
        )
        self.assertEqual(
            some_match.area.name, "Italy", "Match area name should be Italy"
        )
        self.assertEqual(
            some_match.season.matchday, 16, "Match season name should be 2020/2021"
        )


