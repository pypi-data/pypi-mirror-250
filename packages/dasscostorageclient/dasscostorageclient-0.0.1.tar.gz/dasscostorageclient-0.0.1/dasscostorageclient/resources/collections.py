from ..utils import *


class Collections:

    def __init__(self, access_token):
        self.access_token = access_token

    def list_collections(self, institution_name: str):
        """
        Gets a list of all collections in a given institution

        Args:
            institution_name (str): The name of the given institution

        Returns:
            A dictionary containing the collections
        """
        return send_request(RequestMethod.GET, self.access_token, f"/v1/institutions/{institution_name}/collections")

    def create_collection(self, institution_name: str, collection_name: str):
        """
          Creates a collection in a given institution

          Args:
              institution_name (str): The name of the institution to create the collection in
              collection_name (str): The name of the collection to be created

          Returns:
              A dictionary containing the created collection
        """
        body = {
            'name': collection_name,
        }
        return send_request(RequestMethod.POST, self.access_token, f"/v1/institutions/{institution_name}/collections", body)
