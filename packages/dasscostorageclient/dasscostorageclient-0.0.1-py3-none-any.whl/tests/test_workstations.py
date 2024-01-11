from .dassco_test_client import client


def test_can_create_workstation():
    # TODO: Requires a DELETE endpoint to clean up
    pass


def test_can_list_workstations():
    institution_name = "ld"
    res = client.workstations.list_workstations(institution_name)
    status_code = res.get('status_code')
    workstations = res.get('data')
    assert status_code == 200
    assert isinstance(workstations, list)


def test_can_update_workstation():
    institution_name = "ld"
    workstation_name = "lwork3"
    body = {
        'name': workstation_name,
        'status': 'OUT_OF_SERVICE'
    }
    res = client.workstations.update_workstation(institution_name, workstation_name, body)
    status_code = res.get('status_code')
    assert status_code == 204


