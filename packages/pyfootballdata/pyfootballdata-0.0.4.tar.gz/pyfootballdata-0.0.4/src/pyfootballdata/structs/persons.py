from datetime import datetime
from typing import Literal, Optional

from .entities_base import BaseEntity, Collection

RefereeType = Literal[
    "REFEREE",
    "ASSISTANT_REFEREE_N1",
    "ASSISTANT_REFEREE_N2",
    "ASSISTANT_REFEREE_N3",
    "FOURTH_OFFICIAL",
    "VIDEO_ASSISTANT_REFEREE_N1",
    "VIDEO_ASSISTANT_REFEREE_N2",
    "VIDEO_ASSISTANT_REFEREE_N3",
]


class Nationality:
    def __init__(self, nationality: str):
        self._nationality = nationality

    @property
    def title(self):
        return self._nationality


class Person(BaseEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.first_name: str = dictionary.get("firstName")
        self.last_name: str = dictionary.get("lastName")
        self.date_of_birth: Optional[datetime] = (
            datetime.strptime(dictionary.get("dateOfBirth"), "%Y-%m-%d")
            if dictionary.get("dateOfBirth")
            else None
        )
        self.nationality: Nationality = Nationality(dictionary.get("nationality"))

        self.last_updated: Optional[datetime] = (
            datetime.fromisoformat(dictionary.get("lastUpdated").replace("Z", "+00:00"))
            if dictionary.get("lastUpdated")
            else None
        )


class Player(Person):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.section: Optional[str] = dictionary.get("section", None)
        self.position: Optional[str] = dictionary.get("position", None)
        self.shirt_number: Optional[str] = dictionary.get("shirtNumber", None)


class Referee(Person):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.type: RefereeType = dictionary.get("type")


class Coach(Person):
    def __init__(self, dictionary):
        super().__init__(dictionary)


class Referees(Collection[Referee]):
    def __init__(self, dictionary):
        super().__init__(list(map(Referee, dictionary.get("referees", []))))


class Squad(Collection[Player]):
    def __init__(self, dictionary):
        super().__init__(list(map(Player, dictionary.get("squad", []))))
