from ..utils import *


class Institutions:

    def __init__(self, access_token):
        self.access_token = access_token

    def list_institutions(self):
        """
        Gets a list of all institutions

        Returns:
            A dictionary containing all the institutions
        """
        return send_request(RequestMethod.GET, self.access_token, "/v1/institutions")

    def get_institution(self, name: str):
        """
        Gets the institution with the given name

        Args:
            name (str): The name of the institution to be retrieved

        Returns:
            A dictionary containing the retrieved institution
        """
        return send_request(RequestMethod.GET, self.access_token, f"/v1/institutions/{name}")

    def create_institution(self, name: str):
        """
          Creates an institution with the given name

          Args:
              name (str): The name of the institution to be created

          Returns:
              A dictionary containing the created institution
        """
        body = {
            'name': name,
        }
        return send_request(RequestMethod.POST, self.access_token, "/v1/institutions", body)
