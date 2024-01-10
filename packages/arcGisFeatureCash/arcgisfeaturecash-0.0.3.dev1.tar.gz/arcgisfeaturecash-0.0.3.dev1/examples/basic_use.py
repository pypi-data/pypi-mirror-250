import asyncio

from arcGisFeatureCash import ArcGisFeatureService

url = "https://mapservices.prorail.nl/arcgis/rest/services/Referentiesysteem_004/FeatureServer"


async def main():
    tester = await ArcGisFeatureService.factory(url)
    assert tester


if __name__ == "__main__":
    asyncio.run(main())
