from .areas import CondensedArea
from .competitions import CondensedCompetition
from .seasons import Season


class GeoHistoricalEntity:
    def __init__(self, dictionary):
        self._area = CondensedArea(dictionary.get("area"))
        self._competition = CondensedCompetition(dictionary.get("competition"))
        self._season = Season(dictionary.get("season"))

    @property
    def area(self) -> CondensedArea:
        return self._area

    @property
    def competition(self) -> CondensedCompetition:
        return self._competition

    @property
    def season(self) -> Season:
        return self._season
