from typing import List

from .competitions import CompetitionStage
from .matches import MatchStatus


def collect_unique_items(single: any = None, multiple: List[any] = None):
    unique_items = set()
    if single:
        unique_items.add(single)
    if multiple:
        unique_items.update(multiple)
    return None if len(unique_items) == 0 else list(unique_items)


class Filters:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if value:
                self.__dict__[key] = value


class CompetitionsFilters(Filters):
    def __init__(self, area: int = None, areas: List[int] = None):
        areas_filters = collect_unique_items(single=area, multiple=areas)
        super().__init__(areas=areas_filters)


class StandingsFilters(Filters):
    def __init__(self, matchday: int = None, season: int = None, date: str = None):
        super().__init__(matchday=matchday, season=season, date=date)


class DefaultMatchesFilters(Filters):
    def __init__(
        self,
        date_from: str = None,
        date_to: str = None,
        status: MatchStatus = None,
        competitions: List[int] = None,
        ids: List[int] = None,
        **kwargs,
    ):
        super().__init__(
            dateFrom=date_from,
            dateTo=date_to,
            status=status,
            competitions=competitions,
            ids=ids,
        )


class CompetitionMatchesFilters(Filters):
    def __init__(
        self,
        date_from: str = None,
        date_to: str = None,
        stage: CompetitionStage = None,
        status: MatchStatus = None,
        matchday: int = None,
        group: str = None,
        season: int = None,
        **kwargs,
    ):
        super().__init__(
            dateFrom=date_from,
            dateTo=date_to,
            stage=stage,
            status=status,
            matchday=matchday,
            group=group,
            season=season,
        )


class PersonMatchesFilters(Filters):
    def __init__(
        self,
        date_from: str = None,
        date_to: str = None,
        status: MatchStatus = None,
        competitions: List[int] = None,
        limit: int = None,
        offset: int = None,
        **kwargs,
    ):
        super().__init__(
            dateFrom=date_from,
            dateTo=date_to,
            status=status,
            competitions=competitions,
            limit=limit,
            offset=offset,
        )


class ScorersFilters(Filters):
    def __init__(self, limit: int = None, season: int = None):
        super().__init__(limit=limit, season=season)


class TeamMatchesFilters(Filters):
    def __init__(
        self,
        date_from: str = None,
        date_to: str = None,
        season: int = None,
        competitions: List[int] = None,
        status: MatchStatus = None,
        venue: str = None,
        limit: int = None,
        **kwargs,
    ):
        super().__init__(
            dateFrom=date_from,
            dateTo=date_to,
            season=season,
            competitions=competitions,
            status=status,
            venue=venue,
            limit=limit,
        )


class CompetitionTeamsFilters(Filters):
    def __init__(self, season: int = None, **kwargs):
        super().__init__(season=season)


class TeamFilters(Filters):
    def __init__(self, limit: int = None, offset: int = None, **kwargs):
        super().__init__(limit=limit, offset=offset)


class Head2HeadFilters(Filters):
    def __init__(
        self,
        limit: int = None,
        date_from: str = None,
        date_to: str = None,
        competitions: List[int] = None,
        **kwargs,
    ):
        super().__init__(
            limit=limit, dateFrom=date_from, dateTo=date_to, competitions=competitions
        )
