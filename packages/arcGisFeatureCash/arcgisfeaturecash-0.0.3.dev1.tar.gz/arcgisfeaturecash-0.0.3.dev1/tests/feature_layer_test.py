import pytest
from arcGisFeatureCash import ArcGisFeatureService


@pytest.fixture
@pytest.mark.asyncio
async def feature_cash():
    url = "https://mapservices.prorail.nl/arcgis/rest/services/Referentiesysteem_004/FeatureServer"
    return await ArcGisFeatureService.factory(url)


@pytest.mark.asyncio
async def test_get_features(feature_cash):
    feature_service = await feature_cash
    all_features = feature_service.get_all_features()
    print(all_features)


if __name__ == "__main__":
    pytest.main()


# todo test service on feature service:
#  small feature service with all geometry types
#  layers:
#  - point
#  - point 3d
#  - polyline 3d
#  - polyline 3d m values
#  - polyline 2d m values
#  - polygon 2d
#  - polygon 2d multipath (not implemented)
#  - polygon 3d (not implemented)
#  - polygon 3d multipath (not implemented)
