import requests
from .resources.institutions import Institutions
from .resources.assets import Assets
from .resources.shares import Shares
from .resources.workstations import Workstations
from .resources.pipelines import Pipelines
from .resources.collections import Collections
from .exceptions.api_error import APIError


class DaSSCoStorageClient:

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = "https://idp.test.dassco.dk/realms/dassco/protocol/openid-connect/token"
        self.api_url = "https://storage.test.dassco.dk/api"
        self.access_token = self.__get_access_token()
        self.institutions = Institutions(self.access_token)
        self.assets = Assets(self.access_token)
        self.shares = Shares(self.access_token)
        self.workstations = Workstations(self.access_token)
        self.pipelines = Pipelines(self.access_token)
        self.collections = Collections(self.access_token)

    def __get_access_token(self):
        """
            Authenticates the client_id and client_secret. If the credentials are valid, an access token is obtained.

            Returns:
                A valid access token that will be used in subsequent requests
        """
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': 'openid'
        }

        res = requests.post(self.token_endpoint, data=data)

        if res.status_code == 200:
            token_data = res.json()
            return token_data.get("access_token")
        else:
            raise APIError(response=res.json(), status_code=res.status_code)
