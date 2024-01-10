from dataclasses import dataclass, field
from typing import Dict

from arcGisFeatureCash.models.attributes import FeatureFields, parse_date
from arcGisFeatureCash.models.feature import Features
from arcGisFeatureCash.models.geometry import (
    FeatureSpatialReference,
    EsriGeometryTypeEnum,
)
from arcGisFeatureCash.utils.helpers import clear_temp_data
from arcGisFeatureCash.utils.log import logger


@dataclass
class ArcGisFeatureServiceLayer:
    _data: Dict

    object_id_field_name: str = field(init=False, default="")
    global_id_field_name: str = field(init=False, default="")
    geometry_type: EsriGeometryTypeEnum = field(init=False)
    spatial_reference: FeatureSpatialReference = field(init=False)
    fields: FeatureFields = field(init=False)
    features: Features = field(init=False)
    dataset: str = field(init=False, default="")
    has_m: bool = False

    def __post_init__(self):
        self.object_id_field_name = self._data["objectIdFieldName"]
        self.global_id_field_name = self._data["globalIdFieldName"]
        self.geometry_type = EsriGeometryTypeEnum[self._data["geometryType"]]
        self.spatial_reference = FeatureSpatialReference(self._data["spatialReference"])
        self.fields = FeatureFields(self._data["fields"])
        self.features = Features(self._data["features"])
        self.dataset = self._data["dataset"].split(r"/")[-1]

        clear_temp_data(self)

    async def _set_layer_name(self, layer_legenda: Dict) -> None:
        self.dataset = layer_legenda[self.dataset]
        for item in self.features:
            item.dataset = self.dataset

    async def _process_dates(self) -> None:
        self.features._set_value(self.fields.get_date_fields(), parse_date)

    async def _process_geometry(self) -> None:
        await self.features.set_geometry(self.geometry_type)
        await self.features.set_measure()
        await self.features.clean_data()

    @classmethod
    async def factory(
        cls, _data: Dict, layer_legenda: Dict
    ) -> "ArcGisFeatureServiceLayer":
        self = ArcGisFeatureServiceLayer(_data)
        layer_name = layer_legenda[_data["dataset"].split("/")[-1]]

        logger.debug(f"Processing new Feature Layer: {layer_name}")
        await self._set_layer_name(layer_legenda)
        await self._process_dates()
        await self._process_geometry()
        if len(self.features) != 0:
            self.has_m = False
        else:
            self.has_m = (
                True if self.features[0].measure_geometry is not None else False
            )

        logger.debug(f"Done, created Feature Layer: {layer_name}")

        return self

    def get_all_features(self) -> Features:
        return self.features


if __name__ == "__main__":
    pass
