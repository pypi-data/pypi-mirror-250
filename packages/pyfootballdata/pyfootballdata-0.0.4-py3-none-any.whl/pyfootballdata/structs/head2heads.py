from datetime import datetime
from typing import Optional

from .entities_base import AtomicEntity, BaseEntity
from .matches import Matches


class TeamStats(BaseEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.wins: int = dictionary.get("wins")
        self.draws: int = dictionary.get("draws")
        self.losses: int = dictionary.get("losses")


class Head2Head:
    def __init__(self, dictionary):
        meta = dictionary.get("resultSet")
        self.date_from: datetime = datetime.strptime(meta.get("first"), "%Y-%m-%d")
        self.date_to: datetime = datetime.strptime(meta.get("last"), "%Y-%m-%d")
        self.matches: Matches = Matches(dictionary)

        aggregates = dictionary.get("aggregates")
        self.number_of_matches: Optional[int] = aggregates.get("numberOfMatches", None)
        self.total_goals: Optional[int] = aggregates.get("totalGoals", None)
        self.team_home: TeamStats = TeamStats(aggregates.get("homeTeam"))
        self.team_away: TeamStats = TeamStats(aggregates.get("awayTeam"))

    @property
    def average_goals(self) -> float:
        return (
            self.total_goals / self.number_of_matches if self.number_of_matches else 0
        )
