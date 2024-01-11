from ..utils import *
from ..resources.models.sambainfo import SambaInfoModel


class Shares:

    def __init__(self, access_token):
        self.access_token = access_token

    def disconnect_share(self, share_name: str, asset_guid: str):
        body = {
            'shareName': share_name,
            'assetGuid': asset_guid
        }
        res = send_request(RequestMethod.POST, self.access_token, "/v1/shares/disconnect", body)
        return SambaInfoModel.model_validate(res.get('data'))

    def open_share(self, asset_guid):
        body = {
            'users': [],
            'assets': [
                {
                    'asset_guid': asset_guid
                }
            ]
        }
        res = send_request(RequestMethod.POST, self.access_token, f"/v1/shares/open", body)
        return SambaInfoModel.model_validate(res.get('data'))

    def reopen_share(self, share_name):
        body = {
            'shareName': share_name,
        }
        res = send_request(RequestMethod.POST, self.access_token, f"/v1/shares/reopen", body)
        return SambaInfoModel.model_validate(res.get('data'))

    def close_share(self, share_name: str, asset_guid, sync=False):
        body = {
            'minimalAsset': {
                'asset_guid': asset_guid
            },
            'shareName': share_name
        }
        res = send_request(RequestMethod.POST, self.access_token, f"/v1/shares/close?syncERDA={sync}", body)
        return SambaInfoModel.model_validate(res.get('data'))
