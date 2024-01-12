from .entities_base import FlaggedAndCodedEntity, Collection


class CondensedArea(FlaggedAndCodedEntity):
    pass


class Area(CondensedArea):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.parent_area_id: int = dictionary.get("parentAreaId")
        self.parent_area: int = dictionary.get("parentArea")


class Areas(Collection[Area]):
    def __init__(self, dictionary):
        super().__init__(list(map(Area, dictionary.get("areas", []))))
