import json
import unittest

from src.pyfootballdata.structs import Teams, Team


class TestTeams(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        teams_file = open("data/teams_epl.json")
        teams_dictionary = json.load(teams_file)
        cls.teams = Teams(teams_dictionary)
        teams_file.close()

        teams_slice_file = open("data/teams_slice.json")
        teams_slice_dictionary = json.load(teams_slice_file)
        cls.teams_slice = Teams(teams_slice_dictionary)
        teams_slice_file.close()

        team_file = open("data/team_arsenal.json")
        team_dictionary = json.load(team_file)
        cls.team = Team(team_dictionary)
        team_file.close()

    def test_teams_instance(self):
        self.assertIsInstance(self.teams, Teams, "Teams should be an instance of Teams")
        self.assertTrue(len(self.teams) > 0, "Teams should not be empty")
        self.assertIsNotNone(self.teams[0], "First item in teams should not be None")
        self.assertIsInstance(
            self.teams_slice, Teams, "Teams should be an instance of Teams"
        )
        self.assertTrue(len(self.teams.to_ids()) > 0, "Teams ids should not be empty")
        for team in self.teams:
            self.assertIsInstance(
                team, Team, "Team should be an instance of Team in Teams"
            )

    def test_team_instance(self):
        self.assertIsInstance(self.team, Team, "Team should be an instance of Team")
        self.assertTrue(
            self.team.crest == self.team.flag,
            "Team crest should be equal to team flag",
        )
        self.assertTrue(
            self.team.emblem == self.team.flag,
            "Team emblem should be equal to team flag",
        )
        self.assertTrue(
            self.team.tla == self.team.code,
            "Team tla should be equal to team code",
        )
