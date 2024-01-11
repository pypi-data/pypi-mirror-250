from typing import List
from .models.sambainfo import SambaInfoModel
from .models.specimen import SpecimenModel
from ..utils import *
from pydantic import TypeAdapter, Field, BaseModel
from datetime import datetime


class AssetModel(BaseModel):
    pid: str = Field(alias='asset_pid')
    guid: str = Field(alias='asset_guid')
    status: str
    multi_specimen: bool
    specimens: list[SpecimenModel]
    funding: str | None
    subject: str | None
    payload_type: str | None
    file_formats: list[str]
    asset_locked: bool
    restricted_access: list[str]
    institution: str
    collection: str
    sambaInfo: SambaInfoModel | None
    pipeline: str
    digitiser: str | None


class EventModel(BaseModel):
    user: str
    timestamp: datetime = Field(alias="timeStamp")
    event: str
    workstation: str
    pipeline: str


class Assets:

    def __init__(self, access_token):
        self.access_token = access_token

    def get_asset(self, guid: str):
        """
        Gets the metadata of the given asset

        Args:
            guid (str): The guid of the asset to be retrieved

        Returns:
            An Asset object that contains the metadata
        """
        res = send_request(RequestMethod.GET, self.access_token, f"/v1/assetmetadata/{guid}")
        return {
            'data': AssetModel.model_validate(res.get('data')),
            'status_code': res.get('status_code')
        }

    def create_asset(self, body: dict):
        """
        Creates a new asset

        Args:
            body (dict): The metadata of the new asset

        Returns:
            An Asset object that contains the metadata of the created asset
        """
        res = send_request(RequestMethod.POST, self.access_token, f"/v1/assetmetadata", body)
        return {
            'data': AssetModel.model_validate(res.get('data')),
            'status_code': res.get('status_code')
        }

    def update_asset(self, guid: str, body: dict):
        """
        Updates the asset with the given guid

        Args:
            guid (str): The guid of the asset to be updated
            body (dict): The metadata to be updated in the given asset

        Returns:
            An Asset object that contains the metadata of the updated asset
        """
        res = send_request(RequestMethod.PUT, self.access_token, f"/v1/assetmetadata/{guid}", body)
        return {
            'data': AssetModel.model_validate(res.get('data')),
            'status_code': res.get('status_code')
        }

    def list_events(self, guid: str):
        """
        Lists the events of the given asset

        Args:
            guid (str): The guid of the asset

        Returns:
            A list of Event objects
        """
        res = send_request(RequestMethod.GET, self.access_token, f"/v1/assetmetadata/{guid}/events")
        ta = TypeAdapter(List[EventModel])
        return {
            'data': ta.validate_python(res.get('data')),
            'status_code': res.get('status_code')
        }
