from .entities_base import Collection
from .persons import Player
from .teams import Team


class Scorer(Player):
    def __init__(self, dictionary):
        super().__init__(dictionary.get("player"))
        self.team: Team = Team(dictionary.get("team"))
        self.matches: int = dictionary.get("playedMatches")
        self.goals: int = dictionary.get("goals")
        self.assists: int = dictionary.get("assists")
        self.penalties: int = dictionary.get("penalties")


class Scorers(Collection[Scorer]):
    def __init__(self, dictionary):
        super().__init__(list(map(Scorer, dictionary.get("scorers", []))))
