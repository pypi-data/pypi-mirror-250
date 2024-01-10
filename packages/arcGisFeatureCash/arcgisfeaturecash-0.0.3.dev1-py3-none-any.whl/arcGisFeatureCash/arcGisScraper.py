import json
import math
import asyncio
import ssl

import httpx

from typing import Optional, Dict, List
from httpx import Limits

from arcGisFeatureCash.utils.log import logger

import pickle
from pathlib import Path


DEV = False

# seems arcgis feature service usages LEGACY_RENEGOTIATION, its a thing on 3.11 and above
CUSTOM_SSL_CONTEXT = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
CUSTOM_SSL_CONTEXT.options |= (
    0x00040000  # OP flag SSL_OP_ALLOW_UNSAFE_LEGACY_RENEGOTIATION
)
CUSTOM_SSL_CONTEXT.check_hostname = False
CUSTOM_SSL_CONTEXT.verify_mode = ssl.CERT_NONE


class ArcGisScraper:
    def __init__(self, feature_service_url: str):
        self._pickle_file: Path = Path("./cashed_scraper.temp")
        self._base_url = feature_service_url
        self.feature_service_info: Optional[Dict] = None
        self.feature_layers: Optional[List[Dict]] = None
        self._limits = Limits(max_connections=5, max_keepalive_connections=5)
        self._transport = httpx.HTTPTransport(retries=1)
        self.layer_info: dict = {}

    @classmethod
    async def factory(cls, url):
        self = ArcGisScraper(url)
        if DEV:
            if input("enter 1 to load pickle else get from internet.") == "1":
                if self._pickle_file.is_file():
                    logger.debug("found cash... load scraper for development")
                    return self._get_pickle()

        await self._process_all_layers()

        if DEV:
            self._pickle_save()

        return self

    async def _fetch(self, url: str) -> dict:
        async with httpx.AsyncClient(
            timeout=None, limits=self._limits, verify=CUSTOM_SSL_CONTEXT
        ) as client:
            succes = False
            while not succes:
                try:
                    r = await client.get(url)
                    logger.info(f"fetched data, status {r.status_code}: {url}")
                    response = json.loads(r.text)
                    if isinstance(response, dict):
                        return response
                    raise ValueError(f"Can bake json from response {url}")
                except Exception as e:
                    logger.debug(f"error: {e}")
                    await asyncio.sleep(3)
        raise ValueError(f"cant fetch data {url}")

    async def _get_json_data_async(self, url: str) -> dict:
        retry_seconds = 120
        json_data = await self._fetch(url)
        if "error" in json_data.keys():
            succes = False
            while not succes:
                logger.error(f"fetched data got error: {url}")
                logger.info(f"retry in {retry_seconds} seconds")
                await asyncio.sleep(retry_seconds)
                json_data = await self._fetch(url)
                if "error" not in json_data.keys():
                    succes = True

        return json_data

    async def _get_all_data_async(
        self, base_url: str, feature_offset: int = 2000
    ) -> dict:
        self.layer_info = await self._get_json_data_async(base_url + "?f=pjson")

        # get all data
        feature_service_url = (
            base_url + "/query?returnZ=true&returnM=true&f=json&outfields=*&where=1%3D1"
        )
        count_response = await self._get_json_data_async(
            feature_service_url + "&returnCountOnly=true"
        )

        # create batches
        feature_total_count = count_response["count"]
        if feature_total_count == 0:
            return {
                "dataset": base_url,
                "features": [],
                "geometryType": self.layer_info["geometryType"],
                "fields": self.layer_info["fields"],
                "objectIdFieldName": self.layer_info["objectIdField"],
                "globalIdFieldName": self.layer_info["globalIdField"],
                "spatialReference": {"latestWkid": None, "wkid": None},
            }

        batch_count = math.ceil(feature_total_count / feature_offset)
        batch_list = []
        offset = 0
        for n in range(batch_count):
            batch_list.append(feature_service_url + f"&resultOffset={offset}")
            offset += feature_offset

        # create and await all task
        tasks = [self._get_json_data_async(url) for url in batch_list]
        feature_data = await asyncio.gather(*tasks)

        logger.debug(f"Merging data {base_url}")

        features: List[dict] = sum([item["features"] for item in feature_data], [])

        feature_data[0]["features"] = features
        logger.debug(f"Done merging data {base_url}")

        # todo: make succeeded check on feature count
        feature_data[0]["dataset"] = base_url
        if isinstance(feature_data[0], dict):
            return feature_data[0]
        else:
            raise ValueError("")

    async def _get_layer_data(self, feature_service_layer_url: str) -> dict:
        return await self._get_all_data_async(feature_service_layer_url)

    async def _process_all_layers(self):
        self.feature_service_info = await self._get_json_data_async(
            self._base_url + "?f=pjson"
        )
        batch_list = [
            f"{self._base_url}/{item['id']}"
            for item in self.feature_service_info["layers"]
        ]
        tasks = [self._get_layer_data(url) for url in batch_list]
        feature_data = await asyncio.gather(*tasks)
        self.feature_layers = feature_data

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_transport"]
        return state

    def _pickle_save(self):
        with self._pickle_file.open(mode="wb") as file:
            pickle.dump(self, file)

    def _get_pickle(self):
        with self._pickle_file.open(mode="rb") as file:
            return pickle.load(file)


if __name__ == "__main__":
    pass
