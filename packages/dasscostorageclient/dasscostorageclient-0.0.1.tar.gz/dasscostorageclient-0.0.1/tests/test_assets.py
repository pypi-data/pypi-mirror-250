from .dassco_test_client import client


def test_can_create_asset():
    # TODO: Requires a DELETE endpoint to clean up
    pass


def test_can_get_asset():
    asset_guid = "test_asset2"
    res = client.assets.get_asset(asset_guid)
    status_code = res.get('status_code')
    asset = res.get('data')
    assert status_code == 200
    assert asset.guid == asset_guid


def test_can_update_asset():
    # TODO: Replace asset_guid with the created asset guid from the first test when DELETE endpoint is available
    asset_guid = "test_asset2"
    body = {
        'funding': 'test funding',
        'subject': 'test subject',
        'updateUser': 'Test user',  # Required
        'institution': 'ld',  # Required
        'pipeline': 'lpipe',  # Required
        'collection': 'lcoll',  # Required
        'workstation': 'lwork',  # Required
        'status': 'WORKING_COPY'  # Required

    }
    res = client.assets.update_asset(asset_guid, body)
    status_code = res.get('status_code')
    asset = res.get('data')
    assert status_code == 200
    assert asset.funding == 'test funding'
    assert asset.subject == 'test subject'


def test_can_list_events():
    asset_guid = "test_asset2"
    res = client.assets.list_events(asset_guid)
    status_code = res.get('status_code')
    events = res.get('data')
    assert status_code == 200
    assert isinstance(events, list)

