from ..utils import *


class Pipelines:

    def __init__(self, access_token):
        self.access_token = access_token

    def list_pipelines(self, institution_name: str):
        """
        Gets a list of all pipelines in a given institution

        Args:
            institution_name (str): The name of the given institution

        Returns:
            A dictionary containing the pipelines
        """
        return send_request(RequestMethod.GET, self.access_token, f"/v1/institutions/{institution_name}/pipelines")

    def create_pipeline(self, institution_name: str, pipeline_name: str):
        """
          Creates a pipeline in a given institution

          Args:
              institution_name (str): The name of the institution to create the pipeline in
              pipeline_name (str): The name of the pipeline to be created

         Returns:
            A dictionary containing the created pipeline
        """
        body = {
            'name': pipeline_name,
        }
        return send_request(RequestMethod.POST, self.access_token, f"/v1/institutions/{institution_name}/pipelines", body)
