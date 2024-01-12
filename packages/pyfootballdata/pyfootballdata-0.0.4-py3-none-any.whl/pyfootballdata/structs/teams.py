from .competitions import CondensedCompetitions
from .entities_base import (
    Collection,
    CondensedTeam,
)
from .persons import Coach, Squad


class Team(CondensedTeam):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.address = dictionary.get("address")
        self.website = dictionary.get("website")
        self.founded = dictionary.get("founded")
        self.club_colors = dictionary.get("clubColors")
        self.venue = dictionary.get("venue")
        self.last_updated = dictionary.get("lastUpdated")

        competitions = dictionary.get("runningCompetitions")
        if competitions is None:
            competition = dictionary.get("competition")
            competitions = [competition] if competition else None

        self.competitions: CondensedCompetitions = (
            CondensedCompetitions({"competitions": competitions})
            if competitions
            else None
        )

        self.coach: Coach = (
            Coach(dictionary.get("coach")) if dictionary.get("coach") else None
        )
        self.squad: Squad = Squad(dictionary)


class Teams(Collection[Team]):
    def __init__(self, dictionary):
        super().__init__(list(map(Team, dictionary.get("teams", []))))
