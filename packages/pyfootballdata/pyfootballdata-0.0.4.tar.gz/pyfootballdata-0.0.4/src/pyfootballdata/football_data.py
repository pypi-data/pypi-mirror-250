import asyncio
import concurrent.futures
import http.client
import json
from typing import Optional, Union, List
from urllib.parse import urlencode

from .structs import *


def encode_params(params):
    if params:
        return urlencode(params, doseq=True)
    return ""


async def async_wrapper(synchronous_method, *args, **kwargs):
    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(
            executor, lambda: synchronous_method(*args, **kwargs)
        )


class Endpoints:
    areas = "/v4/areas"
    area = "/v4/areas/{area_id}"
    competitions = "/v4/competitions"
    competition = "/v4/competitions/{competition_id}"
    standings = "/v4/competitions/{competition_id}/standings"
    competition_matches = "/v4/competitions/{competition_id}/matches"
    competition_teams = "/v4/competitions/{competition_id}/teams"
    competition_scorers = "/v4/competitions/{competition_id}/scorers"
    teams = "/v4/teams"
    team = "/v4/teams/{team_id}"
    team_matches = "/v4/teams/{team_id}/matches"
    person = "/v4/persons/{person_id}"
    person_matches = "/v4/persons/{person_id}/matches"
    matches = "/v4/matches"
    match = "/v4/matches/{match_id}"
    match_head2head = "/v4/matches/{match_id}/head2head"


class FootballData:
    _endpoints = Endpoints()

    def __init__(self, api_key=None, base_url="api.football-data.org"):
        self._base_url = base_url
        self._api_key = api_key

    def areas(self) -> Areas:
        return self._fetch(Areas, self._endpoints.areas)

    def area(self, area_id: int) -> Area:
        return self._fetch(Area, self._endpoints.area.format(area_id=area_id))

    def competitions(
        self,
        area: Optional[Union[Area, int]] = None,
        areas: Optional[Union[List[Area], List[int]]] = None,
    ) -> Competitions:
        area_id = area.id if isinstance(area, Area) else area
        area_ids = (
            [area.id if isinstance(area, Area) else area for area in areas]
            if areas is not None
            else None
        )
        return self._fetch(
            Competitions,
            self._endpoints.competitions,
            filters=CompetitionsFilters(area=area_id, areas=area_ids),
        )

    def competition(self, competition_id) -> Competition:
        return self._fetch(
            Competition,
            self._endpoints.competition.format(competition_id=competition_id),
        )

    def standings(
        self,
        competition: Union[Competition, int, str],
        matchday: Optional[int] = None,
        season: Optional[int] = None,
        date: Optional[str] = None,
    ) -> Standings:
        competition_id = (
            competition.id if isinstance(competition, Competition) else competition
        )
        return self._fetch(
            Standings,
            self._endpoints.standings.format(competition_id=competition_id),
            filters=StandingsFilters(matchday=matchday, season=season, date=date),
        )

    def matches(
        self,
        team: Optional[Union[Team, int]] = None,
        person: Optional[Union[Person, int]] = None,
        competition: Optional[Union[Competition, int]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        status: Optional[MatchStatus] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        competitions: Optional[Union[Competitions, List[int]]] = None,
        ids: Optional[Union[Matches, List[int]]] = None,
        stage: Optional[CompetitionStage] = None,
        matchday: Optional[int] = None,
        group: Optional[str] = None,
        season: Optional[int] = None,
        venue: Optional[str] = None,
    ) -> Matches:
        return self._get_matches(
            team=team,
            person=person,
            competition=competition,
            date_from=date_from,
            date_to=date_to,
            status=status,
            limit=limit,
            offset=offset,
            сompetitions=competitions.to_ids()
            if isinstance(competitions, Competitions)
            else competitions,
            ids=ids.to_ids() if isinstance(ids, Matches) else ids,
            stage=stage,
            matchday=matchday,
            group=group,
            season=season,
            venue=venue,
        )

    def _get_matches(
        self,
        team: Optional[Union[Team, int]] = None,
        person: Optional[Union[Person, int]] = None,
        competition: Optional[Union[Competition, int]] = None,
        **kwargs,
    ) -> Matches:
        if team is None and person is None and competition is None:
            endpoint = self._endpoints.matches
            matches_filters = DefaultMatchesFilters(**kwargs)
            return self._fetch(Matches, endpoint, filters=matches_filters)

        if team is not None:
            team = team if isinstance(team, Team) else Team({"id": team})
            endpoint = self._endpoints.team_matches.format(team_id=team.id)
            matches_filters = TeamMatchesFilters(**kwargs)
            return self._fetch(Matches, endpoint, filters=matches_filters)

        if person is not None:
            person = person if isinstance(person, Person) else Person({"id": person})
            endpoint = self._endpoints.person_matches.format(person_id=person.id)
            matches_filters = PersonMatchesFilters(**kwargs)
            return self._fetch(Matches, endpoint, filters=matches_filters)

        if competition is not None:
            competition = (
                competition
                if isinstance(competition, Competition)
                else Competition({"id": competition})
            )
            endpoint = self._endpoints.competition_matches.format(
                competition_id=competition.id
            )
            matches_filters = CompetitionMatchesFilters(**kwargs)
            return self._fetch(Matches, endpoint, filters=matches_filters)

    def match(self, match: Union[Match, int]) -> Match:
        match_id = match.id if isinstance(match, Match) else match
        return self._fetch(Match, self._endpoints.match.format(match_id=match_id))

    def teams(
        self,
        competition: Union[Competition, int, str] = None,
        season: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Teams:
        competition_id = (
            competition.id if isinstance(competition, Competition) else competition
        )
        if competition_id is None:
            return self._fetch(
                Teams,
                self._endpoints.teams,
                filters=TeamFilters(limit=limit, offset=offset),
            )
        else:
            return self._fetch(
                Teams,
                self._endpoints.competition_teams.format(competition_id=competition_id),
                filters=CompetitionTeamsFilters(season=season),
            )

    def team(self, team: Union[Team, CondensedTeam, int]) -> Team:
        team_id = team.id if isinstance(team, (Team, CondensedTeam)) else team
        return self._fetch(Team, self._endpoints.team.format(team_id=team_id))

    def person(self, person: Union[Person, int]) -> Person:
        person_id = person.id if isinstance(person, Person) else person
        return self._fetch(Person, self._endpoints.person.format(person_id=person_id))

    def scorers(
        self,
        competition: Union[Competition, int, str],
        limit: Optional[int] = None,
        season: Optional[int] = None,
    ) -> Scorers:
        competition_id = (
            competition.id if isinstance(competition, Competition) else competition
        )
        return self._fetch(
            Scorers,
            self._endpoints.competition_scorers.format(competition_id=competition_id),
            ScorersFilters(limit=limit, season=season),
        )

    def head2head(
        self,
        match: Union[Match, int],
        limit: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        competitions: Optional[Union[Competitions, List[int]]] = None,
    ) -> Head2Head:
        match_id = match.id if isinstance(match, Match) else match
        comps = (
            competitions.to_ids()
            if isinstance(competitions, Competitions)
            else competitions
        )
        return self._fetch(
            Head2Head,
            self._endpoints.match_head2head.format(match_id=match_id),
            Head2HeadFilters(
                limit=limit,
                date_from=date_from,
                date_to=date_to,
                competitions=comps,
            ),
        )

    def _fetch(self, mapping, endpoint, filters=None):
        conn = None
        try:
            method = "GET"
            conn = http.client.HTTPSConnection(self._base_url, timeout=10)
            request_url = (
                f"{endpoint}/?{encode_params(vars(filters))}" if filters else endpoint
            )

            headers = {}
            if self._api_key:
                headers["X-Auth-Token"] = self._api_key

            conn.request(method, request_url, headers=headers)
            response = conn.getresponse()
            if response.status == 200:
                data = response.read()
                return mapping(json.loads(data.decode("utf-8")))
            else:
                raise Exception(f"HTTP error {response.status}: {response.reason}")
        finally:
            conn.close() if conn is not None else None


class FootballDataAsync(FootballData):
    def __init__(self, api_key: str = None, base_url: str = "api.football-data.org"):
        super().__init__(api_key=api_key, base_url=base_url)

    async def areas(self) -> Areas:
        return await async_wrapper(super().areas)

    async def area(self, area_id: int) -> Area:
        return await async_wrapper(super().area, area_id=area_id)

    async def competitions(
        self,
        area: Optional[Union[Area, int]] = None,
        areas: Optional[Union[List[Area], List[int]]] = None,
    ) -> Competitions:
        return await async_wrapper(super().competitions, area=area, areas=areas)

    async def competition(self, competition_id) -> Competition:
        return await async_wrapper(super().competition, competition_id=competition_id)

    async def standings(
        self,
        competition: Union[Competition, int, str],
        matchday: Optional[int] = None,
        season: Optional[int] = None,
        date: Optional[str] = None,
    ) -> Standings:
        return await async_wrapper(
            super().standings,
            competition=competition,
            matchday=matchday,
            season=season,
            date=date,
        )

    async def matches(
        self,
        team: Optional[Union[Team, int]] = None,
        person: Optional[Union[Person, int]] = None,
        competition: Optional[Union[Competition, int]] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        status: Optional[MatchStatus] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        competitions: Optional[Union[Competitions, List[int]]] = None,
        ids: Optional[Union[Matches, List[int]]] = None,
        stage: Optional[CompetitionStage] = None,
        matchday: Optional[int] = None,
        group: Optional[str] = None,
        season: Optional[int] = None,
        venue: Optional[str] = None,
    ) -> Matches:
        return await async_wrapper(
            super().matches,
            team=team,
            person=person,
            competition=competition,
            date_from=date_from,
            date_to=date_to,
            status=status,
            limit=limit,
            offset=offset,
            competitions=competitions,
            ids=ids,
            stage=stage,
            matchday=matchday,
            group=group,
            season=season,
            venue=venue,
        )

    async def match(self, match: Union[Match, int]) -> Match:
        return await async_wrapper(super().match, match=match)

    async def teams(
        self,
        competition: Union[Competition, int, str] = None,
        season: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> Teams:
        return await async_wrapper(
            super().teams,
            competition=competition,
            season=season,
            limit=limit,
            offset=offset,
        )

    async def team(self, team: Union[Team, CondensedTeam, int]) -> Team:
        return await async_wrapper(super().team, team=team)

    async def person(self, person: Union[Person, int]) -> Person:
        return await async_wrapper(super().person, person=person)

    async def scorers(
        self,
        competition: Union[Competition, int, str],
        limit: Optional[int] = None,
        season: Optional[int] = None,
    ) -> Scorers:
        return await async_wrapper(
            super().scorers, competition=competition, limit=limit, season=season
        )

    async def head2head(
        self,
        match: Union[Match, int],
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: Optional[int] = None,
        competitions: Optional[Union[Competitions, List[int]]] = None,
    ) -> Head2Head:
        return await async_wrapper(
            super().head2head,
            match=match,
            limit=limit,
            date_from=date_from,
            date_to=date_to,
            competitions=competitions,
        )
