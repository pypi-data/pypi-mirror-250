import json
import unittest

from src.pyfootballdata.structs import Standings


class TestStandings(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        standings_epl_file = open("data/standings_epl_2021.json")
        standings_epl_dictionary = json.load(standings_epl_file)
        cls.standings_epl = Standings(standings_epl_dictionary)
        cls.standings_epl_copy = Standings(standings_epl_dictionary)
        standings_epl_file.close()

        standings_epl_in_progress = open("data/standings_epl_in_progress.json")
        standings_epl_in_progress_dictionary = json.load(standings_epl_in_progress)
        cls.standings_epl_in_progress = Standings(standings_epl_in_progress_dictionary)
        standings_epl_in_progress.close()

        standings_cl_in_progress = open("data/standings_cl_in_progress.json")
        standings_cl_in_progress_dictionary = json.load(standings_cl_in_progress)
        cls.standings_cl_in_progress = Standings(standings_cl_in_progress_dictionary)
        standings_cl_in_progress.close()

    def test_standings(self):
        self.assertIsInstance(
            self.standings_epl,
            Standings,
            "Standings should be an instance of Standings",
        )
        print(self.standings_epl)
        print(self.standings_epl_copy)
        self.assertEqual(
            repr(self.standings_epl),
            repr(self.standings_epl_copy),
            "Standings should be equal to Standings copy",
        )

    def test_standings_search_by_team_name(self):
        liverpool_fc = self.standings_epl.overall.team_position(team_name="Liverpool")
        self.assertEqual(
            "Liverpool FC", liverpool_fc.team.name, "Team name should be Liverpool FC"
        )
        self.assertEqual(
            2, liverpool_fc.position, "Position should be 1 for Liverpool FC"
        )

    def test_standings_average_goals_aggr(self):
        average_goals_scored = self.standings_epl.overall.average_goals
        self.assertIsNotNone(average_goals_scored, "Average goals should not be None")
        self.assertTrue(
            average_goals_scored > 1.0,
            "Average goals scored should be greater than 1.0",
        )

    def test_standings_home(self):
        least_home_goals = self.standings_epl.home.sort_by(
            key="goals_for"
        )[0]
        self.assertTrue(
            least_home_goals == "Norwich City FC",
            "Team with least home goals should be Norwich City FC",
        )
        self.assertTrue(
            least_home_goals == "norwich city fc",
            "Team with least home goals should be Norwich City FC",
        )

    def test_standings_away(self):
        most_away_wins = self.standings_epl.away.sort_by(key="wins", direction="desc")[0]
        self.assertTrue(
            most_away_wins == "Manchester City fc",
            "Team with least home goals should be Norwich City FC",
        )

    def test_standings_exceptions_for_competition_in_progress(self):
        with self.assertRaises(RuntimeError):
            print(self.standings_epl_in_progress.home)
        with self.assertRaises(RuntimeError):
            print(self.standings_epl_in_progress.away)
        with self.assertRaises(RuntimeError):
            print(len(self.standings_cl_in_progress.home))
        with self.assertRaises(RuntimeError):
            print(len(self.standings_cl_in_progress.away))
        self.assertIsNotNone(self.standings_epl_in_progress.overall)

    def test_standings_table_len(self):
        self.assertEqual(len(self.standings_epl.overall), 20)
        self.assertEqual(len(self.standings_epl.home), 20)
        self.assertEqual(len(self.standings_epl.away), 20)
        with self.assertRaises(RuntimeError):
            print(len(self.standings_cl_in_progress.home))
        with self.assertRaises(RuntimeError):
            print(len(self.standings_cl_in_progress.away))
        self.assertEqual(len(self.standings_cl_in_progress.overall), 4)

    def test_standings_table_sort_by(self):
        pass

    def test_standings_groups(self):
        all_cl_groups = self.standings_cl_in_progress.groups_all
        self.assertEqual(len(all_cl_groups), 8)
        self.assertEqual(all_cl_groups[0].name, "Group A")
        self.assertEqual(all_cl_groups[1].name, "Group B")

        group_a = self.standings_cl_in_progress.group("A")
        self.assertEqual(group_a.name, "Group A")
        self.assertEqual(group_a.type, "TOTAL")

        group_b = self.standings_cl_in_progress.group("b")
        self.assertEqual(group_b.name, "Group B")
        self.assertEqual(group_b.type, "TOTAL")

    def test_standings_position(self):
        epl_bottom_team = self.standings_epl.overall.position(position=20)
        self.assertEqual(epl_bottom_team.team.name, "Norwich City FC")

    def test_standings_team_position(self):
        team_by_name = self.standings_epl.overall.team_position(team_name="Leeds")
        team_by_id = self.standings_epl.overall.team_position(team_id=341)
        self.assertEqual(team_by_name, team_by_id)

    def test_standings_equality(self):
        team_by_name = self.standings_epl.overall.team_position(team_name="Leeds")
        team_by_id = self.standings_epl.overall.team_position(team_id=341)
        self.assertEqual(team_by_name, team_by_id)
        self.assertEqual(team_by_name, "Leeds United FC")
        self.assertEqual(team_by_name, 341)
        with self.assertRaises(TypeError):
            print(team_by_name == {})

    def test_standings_sorting(self):
        sorted_by_goals_conceded = self.standings_epl.overall.sort_by(
            key="goals_against", direction="desc"
        )
        worst_defence = sorted_by_goals_conceded[0]
        second_worst_defence = sorted_by_goals_conceded[1]
        self.assertEqual(worst_defence.team.name, "Norwich City FC")
        self.assertTrue(
            worst_defence == "Norwich City FC",
            "Team with worst defence should be Norwich City FC",
        )
        self.assertTrue(
            second_worst_defence == "Leeds United FC",
            "Team with worst defence should be Norwich City FC",
        )

        default_sort = self.standings_epl.overall.sort_by()
        default_sort_first = default_sort[0]
        reversed_sort = self.standings_epl.overall.sort_by(direction="desc")
        reversed_sort_last = reversed_sort[-1]
        self.assertEqual(default_sort_first, reversed_sort_last)

    def test_standings_loop(self):
        for team in self.standings_epl.overall:
            self.assertTrue(team == team.team.name)
        for team in self.standings_epl.home:
            self.assertTrue(team == team.team.name)
        for team in self.standings_epl.away:
            self.assertTrue(team == team.team.name)
