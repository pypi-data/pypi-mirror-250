from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from shapely import Point, LineString, Polygon
from shapely.geometry.base import BaseGeometry

from arcGisFeatureCash.utils.helpers import clear_temp_data


class EsriGeometryTypeEnum(Enum):
    esriGeometryPoint = "esriGeometryPoint"
    esriGeometryMultipoint = "esriGeometryMultipoint"
    esriGeometryPolyline = "esriGeometryPolyline"
    esriGeometryPolygon = "esriGeometryPolygon"
    esriGeometryEnvelope = "esriGeometryEnvelope"


@dataclass
class FeatureSpatialReference:
    _data: Optional[Dict]
    wkid: str = field(init=False)
    latest_wkid: str = field(init=False)

    def __post_init__(self):
        self.wkid = self._data["wkid"]
        self.latest_wkid = self._data["latestWkid"]
        clear_temp_data(self)


@dataclass
class FeatureGeometry:
    _data: Optional[Dict]

    geometry: BaseGeometry = field(init=False)


async def parse_point(geometry_value: Dict) -> Point:
    # todo: implement 3d
    if geometry_value == "":
        return Point()
    return Point(geometry_value["x"], geometry_value["y"])


async def parse_line(geometry_value: Dict) -> LineString:
    if geometry_value == "" or (
        "paths" in geometry_value and len(geometry_value["paths"]) == 0
    ):
        return LineString()
    elif "hasZ" in geometry_value.keys() and geometry_value["hasZ"]:
        return LineString(
            [[item[0], item[1], item[2]] for item in geometry_value["paths"][0]]
        )
    else:
        return LineString(geometry_value["paths"][0])


async def parse_polygon(geometry_value: Dict) -> Polygon:
    # todo: implement 3d and inner outer stuff
    if geometry_value == "":
        return Polygon()
    return Polygon(geometry_value["rings"][0])


if __name__ == "__main__":
    pass
