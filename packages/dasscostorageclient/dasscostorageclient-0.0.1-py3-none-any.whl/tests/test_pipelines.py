from .dassco_test_client import client


def test_can_list_pipelines():
    res = client.pipelines.list_pipelines("ld")
    status_code = res.get('status_code')
    pipelines = res.get('data')
    assert status_code == 200
    assert isinstance(pipelines, list)


def test_can_create_pipeline():
    # TODO: Requires a DELETE endpoint to clean up
    pass
