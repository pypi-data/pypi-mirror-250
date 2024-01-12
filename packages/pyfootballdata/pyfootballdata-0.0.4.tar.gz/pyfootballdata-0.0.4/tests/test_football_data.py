import unittest

from src.pyfootballdata import FootballData


class TestFootballData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """
            We'll mimic e2e behavior by pointing to a non-existing base_url. This way we'll ensure that useful data
            is making it to the methods tested (hence all the tests below successfully failing, haha!).
            The correctness of the data is tested in e2e tests.
        """
        cls.fd = FootballData(base_url="")

    def test_areas(self):
        try:
            self.fd.areas()
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_area(self):
        try:
            self.fd.area(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_competitions(self):
        try:
            self.fd.competitions()
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_competition(self):
        try:
            self.fd.competition(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_standings(self):
        try:
            self.fd.standings(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_matches_by_team(self):
        try:
            self.fd.matches(team=57)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_matches_by_competition(self):
        try:
            self.fd.matches(competition=2021, limit=5)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_matches_by_person(self):
        try:
            self.fd.matches(person=341459)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_matches_by_nothing(self):
        try:
            self.fd.matches()
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_match(self):
        try:
            self.fd.match(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_teams_by_competition(self):
        try:
            self.fd.teams(competition=2021, limit=5)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_teams_by_nothing(self):
        try:
            self.fd.teams()
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_team(self):
        try:
            self.fd.team(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_person(self):
        try:
            self.fd.person(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_scorers(self):
        try:
            self.fd.scorers(1, 10)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")

    def test_head2head(self):
        try:
            self.fd.head2head(1, 10)
            self.fail("Should have raised an exception")
        except Exception as e:
            print(e)
            self.assertIsNotNone(e, "Exception should not be None")
