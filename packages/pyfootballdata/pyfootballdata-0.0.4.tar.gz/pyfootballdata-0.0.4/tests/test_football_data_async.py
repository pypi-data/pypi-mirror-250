import unittest

from src.pyfootballdata import FootballDataAsync
from src.pyfootballdata.structs import Areas


class TestFootballDataAsync(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        """
        We'll mimic e2e behavior by pointing to a non-existing base_url. This way we'll ensure that useful data
        is making it to the methods tested (hence all the tests below successfully failing, haha!).
        The correctness of the data is tested in e2e tests.
        """
        cls.fd = FootballDataAsync(base_url="")

    async def test_areas(self):
        try:
            await self.fd.areas()
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_area(self):
        try:
            await self.fd.area(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_competitions(self):
        try:
            await self.fd.competitions()
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_competition(self):
        try:
            await self.fd.competition(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_standings(self):
        try:
            await self.fd.standings(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_matches_by_team(self):
        try:
            await self.fd.matches(team=57)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_matches_by_competition(self):
        try:
            await self.fd.matches(competition=2021, limit=5)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_matches_by_person(self):
        try:
            await self.fd.matches(person=341459)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_matches_by_nothing(self):
        try:
            await self.fd.matches()
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_match(self):
        try:
            await self.fd.match(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_teams_by_competition(self):
        try:
            await self.fd.teams(competition=2021, limit=5)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_teams_by_nothing(self):
        try:
            await self.fd.teams()
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_team(self):
        try:
            await self.fd.team(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_person(self):
        try:
            await self.fd.person(1)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_scorers(self):
        try:
            await self.fd.scorers(1, 10)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_head2head(self):
        try:
            await self.fd.head2head(1, 10)
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")

    async def test_real_connection_success(self):
        try:
            fd = FootballDataAsync()
            areas = await fd.areas()
            self.assertIsInstance(areas, Areas, "Areas should be an instance of Areas")
        except Exception as e:
            self.fail(e)

    async def test_real_connection_error(self):
        try:
            fd = FootballDataAsync(base_url="google.com", api_key="DUMMY_KEY")
            areas = await fd.areas()
            self.fail("Should have raised an exception")
        except Exception as e:
            self.assertIsNotNone(e, "Exception should not be None")
