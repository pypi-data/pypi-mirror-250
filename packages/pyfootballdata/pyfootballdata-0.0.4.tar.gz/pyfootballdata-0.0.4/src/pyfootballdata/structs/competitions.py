from datetime import datetime
from typing import Literal, Optional, List

from .entities_base import FlaggedAndCodedEntity, Collection
from .seasons import Season
from .areas import CondensedArea


CompetitionType = Literal[
    "LEAGUE",
    "CUP",
    "LEAGUE_CUP",
    "PLAYOFFS",
]

CompetitionStage = Literal[
    "FINAL",
    "THIRD_PLACE",
    "SEMI_FINALS",
    "QUARTER_FINALS",
    "LAST_16",
    "LAST_32",
    "LAST_64",
    "ROUND_4",
    "ROUND_3",
    "ROUND_2",
    "ROUND_1",
    "GROUP_STAGE",
    "PRELIMINARY_ROUND",
    "QUALIFICATION",
    "QUALIFICATION_ROUND_1",
    "QUALIFICATION_ROUND_2",
    "QUALIFICATION_ROUND_3",
    "PLAYOFF_ROUND_1",
    "PLAYOFF_ROUND_2",
    "PLAYOFFS",
    "REGULAR_SEASON",
    "CLAUSURA",
    "APERTURA",
    "CHAMPIONSHIP",
    "RELEGATION",
    "RELEGATION_ROUND",
]


class CondensedCompetition(FlaggedAndCodedEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.type: Optional[CompetitionType] = dictionary.get("type", None)


class Competition(CondensedCompetition):
    available_seasons_count: Optional[int]
    seasons: Optional[List[Season]]

    def __init__(self, dictionary):
        super().__init__(dictionary)
        area = dictionary.get("area", None)
        self.area: Optional[CondensedArea] = CondensedArea(area) if area else None

        current_season = dictionary.get("currentSeason", None)
        self.current_season: Optional[Season] = (
            Season(current_season) if current_season else None
        )
        self.available_seasons_count: Optional[int] = dictionary.get(
            "numberOfAvailableSeasons", None
        )
        self.seasons: Optional[List[Season]] = list(
            map(Season, dictionary.get("seasons", []))
        )
        last_updated = dictionary.get("lastUpdated", None)
        self.last_updated: Optional[datetime] = (
            datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
            if last_updated
            else None
        )


class Competitions(Collection[Competition]):
    def __init__(self, dictionary):
        super().__init__(list(map(Competition, dictionary.get("competitions", []))))


class CondensedCompetitions(Collection[CondensedCompetition]):
    def __init__(self, dictionary):
        super().__init__(
            list(map(CondensedCompetition, dictionary.get("competitions", [])))
        )
