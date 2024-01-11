from .dassco_test_client import client


def test_can_create_institution():
    # TODO: Requires a DELETE endpoint to clean up
    pass


def test_can_list_institutions():
    res = client.institutions.list_institutions()
    status_code = res.get('status_code')
    institutions = res.get('data')
    assert status_code == 200
    assert isinstance(institutions, list)


def test_can_call_get_institution():
    institution_name = "ld"
    res = client.institutions.get_institution(institution_name)
    status_code = res.get('status_code')
    institution = res.get('data')
    assert status_code == 200
    assert institution["name"] == institution_name
