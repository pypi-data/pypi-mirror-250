from datetime import datetime

from .entities_base import AtomicEntity, CondensedTeam


class Winner(CondensedTeam):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.address = dictionary.get("address")
        self.website = dictionary.get("website")
        self.founded = dictionary.get("founded")
        self.club_colors = dictionary.get("clubColors")
        self.venue = dictionary.get("venue")
        self.last_updated = dictionary.get("lastUpdated")


class Season(AtomicEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.start_date: datetime = datetime.strptime(
            dictionary.get("startDate"), "%Y-%m-%d"
        )
        self.end_date: datetime = datetime.strptime(
            dictionary.get("endDate"), "%Y-%m-%d"
        )
        self.matchday: int = dictionary.get("currentMatchday", None)
        self.winner = (
            Winner(dictionary.get("winner")) if dictionary.get("winner") else None
        )
