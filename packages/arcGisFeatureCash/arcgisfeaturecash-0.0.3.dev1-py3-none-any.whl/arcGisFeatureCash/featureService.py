import asyncio
import numpy as np

from typing import Optional, List

from numpy.typing import NDArray
from shapely import STRtree, box

from arcGisFeatureCash.models.feature import Feature
from arcGisFeatureCash.featureLayer import ArcGisFeatureServiceLayer
from arcGisFeatureCash.arcGisScraper import ArcGisScraper


class ArcGisFeatureService:
    def __init__(self, feature_service_url: str):
        self._base_url: str = feature_service_url
        self.name: str = feature_service_url.split(r"/")[-2]
        self.feature_service_layers: List[ArcGisFeatureServiceLayer] = []
        self._tree: STRtree = STRtree([])
        self._tree_keys: NDArray = np.array([])

    @classmethod
    async def factory(cls, url) -> "ArcGisFeatureService":
        self = ArcGisFeatureService(url)
        arc_gis_scraper = await ArcGisScraper.factory(url)
        layer_legenda = {
            f"{item['id']}": item["name"]
            for item in arc_gis_scraper.feature_service_info["layers"]
        }

        # todo: get layer name here so we allso can use it when no feature returns (returns count=0)

        tasks = [
            ArcGisFeatureServiceLayer.factory(item, layer_legenda)
            for item in arc_gis_scraper.feature_layers
        ]
        self.feature_service_layers = await asyncio.gather(*tasks)
        records = [
            {"geometry": item.geometry, "key": item.uuid}
            for layer in self.feature_service_layers
            for item in layer.features
        ]

        self._tree = STRtree([record["geometry"] for record in records])
        self._tree_keys = np.array([record["key"] for record in records])

        return self

    def get_all_features(
        self, feature_layer: Optional[List[str]] = None
    ) -> List[Feature]:
        out_list = []
        for item in self.feature_service_layers:
            if feature_layer:
                out_list.extend(
                    [item2 for item2 in item.features if item2.dataset in feature_layer]
                )
            else:
                out_list.extend([item2 for item2 in item.features])
        return out_list

    def get_features_by_key(self, uuids: List[str]) -> List[Feature]:
        out_list = []
        for item in self.feature_service_layers:
            out_list.extend([_ for _ in item.features if _.uuid in uuids])
        return out_list

    def get_features_in_box(self, bbox: box) -> List[Feature]:
        query = self._tree.query(bbox)
        keys = self._tree_keys.take(query).tolist()
        return self.get_features_by_key(keys)

    # def get_features_matching_field_value(
    #     self,
    #     field: FeatureAttribute,
    #     value: Any,
    #     feature_layer: Optional[List[str]] = None,
    # ):
    #     # todo: attribute query on layer
    #     out_list = []
    #     for item in self.feature_service_layers:
    #         pass
    #     return out_list


if __name__ == "__main__":
    pass
