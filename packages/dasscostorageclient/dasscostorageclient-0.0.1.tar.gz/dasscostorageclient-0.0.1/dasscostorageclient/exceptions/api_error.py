class APIError(Exception):
    def __init__(self, response, status_code):
        self.response = response
        self.status_code = status_code
        super().__init__(self.create_message())

    def create_message(self):
        error_message = self.response.get('errorMessage')
        return f"API request failed with status code {self.status_code}: {error_message}"

