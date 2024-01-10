from dataclasses import dataclass, field
from typing import (
    Dict,
    Optional,
    List,
    Any,
    Callable,
    Iterator,
    overload,
    SupportsIndex,
    Union,
)
from datetime import datetime

from enum import Enum

from arcGisFeatureCash.utils.helpers import clear_temp_data
from arcGisFeatureCash.utils.immutableList import ImmutableList


class EsriFieldTypeEnum(Enum):
    esriFieldTypeOID = "esriFieldTypeOID"
    esriFieldTypeString = "esriFieldTypeString"
    esriFieldTypeInteger = "esriFieldTypeInteger"
    esriFieldTypeSmallInteger = "esriFieldTypeSmallInteger"
    esriFieldTypeDouble = "esriFieldTypeDouble"
    esriFieldTypeDate = "esriFieldTypeDate"
    esriFieldTypeGeometry = "esriFieldTypeGeometry"
    esriFieldTypeBlob = "esriFieldTypeBlob"


@dataclass
class FeatureField:
    _data: Optional[Dict]

    name: str = field(init=False)
    alias: str = field(init=False)
    type: EsriFieldTypeEnum = field(init=False)
    length: Optional[int] = field(init=False)

    def __post_init__(self):
        self.name = self._data["name"]
        self.alias = self._data["alias"]
        self.type = EsriFieldTypeEnum[self._data["type"]]
        if "length" in self._data.keys():
            self.length = self._data["length"]
        else:
            self.length = None

        clear_temp_data(self)


@dataclass
class FeatureFields(ImmutableList):
    _data: Optional[Dict]
    _items: List[FeatureField] = field(init=False)

    def __post_init__(self):
        self._items = [FeatureField(item) for item in self._data]
        clear_temp_data(self)

    def __iter__(self) -> Iterator[FeatureField]:
        yield from self._items

    @overload
    def __getitem__(self, idx: SupportsIndex) -> FeatureField:
        ...

    @overload
    def __getitem__(self, idx: slice) -> list[FeatureField]:
        ...

    def __getitem__(
        self, idx: Union[SupportsIndex, slice]
    ) -> Union[FeatureField, list[FeatureField]]:
        return self._items[idx]

    def get_date_fields(self) -> List[FeatureField]:
        return [
            item
            for item in self._items
            if item.type == EsriFieldTypeEnum.esriFieldTypeDate
        ]


@dataclass
class FeatureAttribute:
    key: str
    value: Any

    def __repr__(self) -> str:
        return f"{self.key}={self.value}"


@dataclass
class FeatureAttributes(list[FeatureAttribute]):
    _data: Optional[Dict]
    _items: List[FeatureAttribute] = field(init=False)

    def __post_init__(self):
        self._items = [
            FeatureAttribute(key, value) for key, value in self._data.items()
        ]
        clear_temp_data(self)

    def __iter__(self) -> Iterator[FeatureAttribute]:
        yield from self._items

    @overload
    def __getitem__(self, idx: SupportsIndex) -> FeatureAttribute:
        ...

    @overload
    def __getitem__(self, idx: slice) -> list[FeatureAttribute]:
        ...

    def __getitem__(
        self, idx: Union[SupportsIndex, slice]
    ) -> Union[FeatureAttribute, list[FeatureAttribute]]:
        return self._items[idx]

    def __len__(self) -> int:
        return len(self._items)

    def __delitem__(self, idx):
        raise NotImplementedError("This method is not allowed in FeatureAttributes")

    def __setitem__(self, idx, value):
        raise NotImplementedError("This method is not allowed in FeatureAttributes")

    def __repr__(self) -> str:
        return repr(self._items)

    def set_attribute(self, field_: FeatureField, function: Callable) -> None:
        for item in self._items:
            if item.key == field_.name:
                item.value = function(item.value)
                break
        else:
            raise KeyError(f"Key '{field_.name}' not found in FeatureAttributes")

    def get_all_fields(self) -> List[str]:
        return [item.key for item in self._items]

    def get_value(self, key: str) -> Optional[FeatureAttribute]:
        response = [item.value for item in self._items if item.key == key]
        if len(response) == 0:
            return None
        elif len(response) > 1:
            raise Exception(f"Duplicated key: {key}")
        return response[0]


def parse_date(date_value: int) -> Optional[datetime]:
    if date_value:
        return datetime.fromtimestamp(date_value / 1000)
    else:
        return None


if __name__ == "__main__":
    pass
