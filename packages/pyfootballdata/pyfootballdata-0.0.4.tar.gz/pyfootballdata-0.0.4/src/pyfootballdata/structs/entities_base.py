from typing import TypeVar, Generic, List, Optional


class AtomicEntity:
    def __init__(self, dictionary):
        self.id = dictionary.get("id")

    def __repr__(self):
        return str(self.__dict__)


class BaseEntity(AtomicEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.name: Optional[str] = dictionary.get("name", None)


class FlaggedAndCodedEntity(BaseEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)

        # if any of the keys in flag_keys is not None, then flag is set to that value
        flag_keys = ["flag", "crest", "emblem"]
        self.flag: Optional[str] = next(
            (item for item in map(dictionary.get, flag_keys) if item is not None), None
        )

        # if any of the keys in code_keys is not None, then code is set to that value
        code_keys = ["countryCode", "code", "tla"]
        self.code: Optional[str] = next(
            (item for item in map(dictionary.get, code_keys) if item is not None), None
        )

    @property
    def tla(self):
        return self.code

    @property
    def crest(self):
        return self.flag

    @property
    def emblem(self):
        return self.flag


class CondensedTeam(FlaggedAndCodedEntity):
    def __init__(self, dictionary):
        super().__init__(dictionary)
        self.short_name: Optional[str] = dictionary.get("shortName", None)


T = TypeVar("T")


class Collection(Generic[T]):
    def __init__(self, items: List[T]):
        self.items = items

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __iter__(self):
        return iter(self.items)

    def to_ids(self) -> List[int]:
        return [item.id for item in self.items]
