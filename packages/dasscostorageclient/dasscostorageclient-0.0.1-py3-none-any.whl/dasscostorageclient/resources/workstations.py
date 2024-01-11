from typing import List
from ..utils import *
from pydantic import BaseModel, TypeAdapter
from enum import Enum


class WorkstationModel(BaseModel):
    name: str
    status: str
    institution_name: str


class WorkstationStatus(Enum):
    IN_SERVICE = 'IN_SERVICE'
    OUT_OF_SERVICE = 'OUT_OF_SERVICE'


class Workstations:

    def __init__(self, access_token):
        self.access_token = access_token

    def list_workstations(self, institution_name: str):
        """
        Gets a list of all workstations in a given institution

        Args:
            institution_name (str): The name of the given institution

        Returns:
            A list of Workstation objects
        """
        res = send_request(RequestMethod.GET, self.access_token, f"/v1/institutions/{institution_name}/workstations")

        ta = TypeAdapter(List[WorkstationModel])

        return {
            'data': ta.validate_python(res.get('data')),
            'status_code': res.get('status_code')
        }

    def create_workstation(self, institution_name: str, workstation_name: str, status: WorkstationStatus = WorkstationStatus.IN_SERVICE):
        """
           Creates a workstation in a given institution

           Args:
               institution_name (str): The name of the given institution
               workstation_name (str): The name of the workstation to be created
               status (WorkstationStatus): The status of the workstation to be created. The options are: IN_SERVICE or OUT_OF_SERVICE

           Returns:
               The created Workstation object
        """
        body = {
            'name': workstation_name,
            'status': status
        }
        res = send_request(RequestMethod.POST, self.access_token, f"/v1/institutions/{institution_name}/workstations", body)
        return WorkstationModel.model_validate(res.get('data'))

    def update_workstation(self, institution_name: str, workstation_name: str, body: dict):
        """
        Updates a workstation in a given institution

        Args:
            institution_name (str): The name of the given institution
            workstation_name (str): The name of the workstation to be updated
            body (dict): The fields to be updated in the given workstation

        Returns:
            Currently returns empty data as a 204 (No Content) status code is returned by the API
        """
        return send_request(RequestMethod.PUT, self.access_token, f"/v1/institutions/{institution_name}/workstations/{workstation_name}", body)
