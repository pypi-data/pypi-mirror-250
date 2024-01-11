from .dassco_test_client import client


def test_can_list_collection():
    res = client.collections.list_collections("ld")
    status_code = res.get('status_code')
    collections = res.get('data')
    assert status_code == 200
    assert isinstance(collections, list)


def test_can_create_collection():
    # TODO: Requires a DELETE endpoint to clean up
    pass
