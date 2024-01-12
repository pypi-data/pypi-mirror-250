from datetime import datetime
from typing import List, Literal, Optional

from .competitions import CompetitionStage
from .entities_base import AtomicEntity, Collection
from .entities_compound import GeoHistoricalEntity
from .persons import Referee, Referees
from .teams import CondensedTeam

MatchStatus = Literal[
    "SCHEDULED",
    "LIVE",
    "IN_PLAY",
    "PAUSED",
    "FINISHED",
    "POSTPONED",
    "SUSPENDED",
    "CANCELLED",
]


WinnerLiteral = Literal["HOME_TEAM", "AWAY_TEAM", "DRAW"]
DurationLiteral = Literal["REGULAR", "EXTRA_TIME", "PENALTY_SHOOTOUT"]


class Result:
    def __init__(self, dictionary):
        self.home: int = dictionary.get("home")
        self.away: int = dictionary.get("away")


class FullTime(Result):
    pass


class HalfTime(Result):
    pass


class Score:
    def __init__(self, dictionary):
        self.winner: WinnerLiteral = dictionary.get("winner")
        self.duration: DurationLiteral = dictionary.get("duration")
        self.full_time: Result = FullTime(dictionary.get("fullTime"))
        self.half_time: Result = HalfTime(dictionary.get("halfTime"))


class Match(GeoHistoricalEntity, AtomicEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.status: MatchStatus = dictionary.get("status")
        self.matchday: int = dictionary.get("matchday")
        self.stage: CompetitionStage = dictionary.get("stage")
        self.group: Optional[str] = dictionary.get("group")
        self.utc_date: datetime = datetime.fromisoformat(
            dictionary.get("utcDate").replace("Z", "+00:00")
        )
        self.home_team: CondensedTeam = CondensedTeam(dictionary.get("homeTeam"))
        self.away_team: CondensedTeam = CondensedTeam(dictionary.get("awayTeam"))
        self.last_updated: datetime = datetime.fromisoformat(
            dictionary.get("lastUpdated").replace("Z", "+00:00")
        )
        self.score = Score(dictionary.get("score"))
        # TODO: Deserialize odds
        # self.odds = dictionary.get("odds")
        self.referees = Referees(dictionary)


class Matches(Collection[Match]):
    def __init__(self, dictionary):
        super().__init__(list(map(Match, dictionary.get("matches", []))))
