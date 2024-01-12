import re
from typing import Literal, Optional, List

from .entities_base import CondensedTeam
from .entities_compound import GeoHistoricalEntity


def convert_results_to_points(result: str) -> int:
    if result == "W":
        return 3
    elif result == "D":
        return 1
    elif result == "L":
        return 0
    else:
        raise ValueError("Invalid result: {}".format(result))


class Form:
    def __init__(self, form: str):
        self._form = form

    def __repr__(self):
        return str(self._form)

    def __eq__(self, other):
        if isinstance(other, Form):
            return self._form == other._form
        if isinstance(other, str):
            return self._form == other
        else:
            raise TypeError("Cannot compare Form with {}".format(type(other)))

    def to_list(self) -> List[str]:
        return self._form.split(",")

    def to_points_list(self) -> List[int]:
        return [convert_results_to_points(result) for result in self.to_list()]


class TablePosition:
    def __init__(self, dictionary):
        self.position: int = dictionary.get("position")
        self.team: CondensedTeam = CondensedTeam(dictionary.get("team"))
        self.played_games: int = dictionary.get("playedGames")
        self.form: Form = Form(dictionary.get("form"))
        self.wins: int = dictionary.get("won")
        self.draws: int = dictionary.get("draw")
        self.losses: int = dictionary.get("lost")
        self.points: int = dictionary.get("points")
        self.goals_for: int = dictionary.get("goalsFor")
        self.goals_against: int = dictionary.get("goalsAgainst")
        self.goals_difference: int = dictionary.get("goalDifference")

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        if isinstance(other, TablePosition):
            return self.team.id == other.team.id
        if isinstance(other, int):
            return self.team.id == other
        if isinstance(other, str):
            return self.team.name.lower() == other.lower()
        else:
            raise TypeError("Cannot compare TablePosition with {}".format(type(other)))


SortAttr = Literal[
    "position",
    "played_games",
    "wins",
    "draws",
    "losses",
    "points",
    "goals_for",
    "goals_against",
    "goals_difference",
]
SortDirections = Literal["asc", "desc"]


class Table:
    def __init__(self, table):
        self._items = list(map(TablePosition, table))

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self):
        return str(self._items)

    @property
    def total_goals(self) -> int:
        return sum([item.goals_for for item in self._items])

    @property
    def total_matches_played(self) -> int:
        return sum([item.played_games for item in self._items])

    @property
    def average_goals(self) -> float:
        return self.total_goals / self.total_matches_played

    def position(self, position: int) -> TablePosition:
        return next((item for item in self._items if item.position == position), None)

    def team_position(
        self,
        team_name: str = None,
        team_id: int = None,
    ) -> TablePosition:
        if team_id is not None:
            return next((item for item in self._items if item.team.id == team_id), None)
        if team_name is not None:
            return next(
                (
                    item
                    for item in self._items
                    if re.search(team_name, item.team.name, re.IGNORECASE)
                    or re.search(team_name, item.team.short_name, re.IGNORECASE)
                ),
                None,
            )

    def sort_by(
        self, key: Optional[SortAttr] = None, direction: SortDirections = "asc"
    ) -> List[TablePosition]:
        reverse = direction == "desc"
        sort_key = key if key is not None else "position"
        return sorted(
            self._items, key=lambda item: getattr(item, sort_key), reverse=reverse
        )


class Group:
    def __init__(self, dictionary):
        self.stage: str = dictionary.get("stage")
        self.type: str = dictionary.get("type")
        self.name: str = dictionary.get("group")
        self.table = Table(dictionary.get("table"))

    def __repr__(self):
        return str(self.__dict__)


class Standings(GeoHistoricalEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self._standings = list(map(Group, dictionary.get("standings")))

    def group(self, group: str) -> Optional[Group]:
        group_text = "group {}".format(group) if len(group) == 1 else group
        return next(
            (
                item
                for item in self._standings
                if item.name.lower() == group_text.lower()
            ),
            None,
        )

    @property
    def groups_all(self) -> List[Group]:
        return self._standings

    @property
    def overall(self) -> Optional[Table]:
        return self._standings[0].table

    @property
    def home(self) -> Optional[Table]:
        if self.competition.type == "LEAGUE" and len(self._standings) > 1:
            return self._standings[1].table
        else:
            raise RuntimeError(
                "No home standings available. "
                "This might happen due to the competition requested being a cup or in progress."
            )

    @property
    def away(self) -> Optional[Table]:
        if self.competition.type == "LEAGUE" and len(self._standings) > 1:
            return self._standings[2].table
        else:
            raise RuntimeError(
                "No away standings available. "
                "This might happen due to the competition requested being a cup or in progress."
            )

    def __repr__(self):
        return str(self.__dict__)
