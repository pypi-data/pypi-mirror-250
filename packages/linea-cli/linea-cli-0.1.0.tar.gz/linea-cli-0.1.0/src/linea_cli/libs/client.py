import requests
from .config import config


class Client:
    def __init__(self) -> None:
        self.root_url = config.root_url
        self.auth_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {config.api_token}",
        }

    def _api_call(self, uri) -> any:
        if not config.is_valid:
            return {"error": "Invalid linea config file detected. Skip API calls"}

        req_uri = f"{self.root_url}/{uri}"
        response = requests.get(req_uri, headers=self.auth_headers)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def list_pipelines(self):
        return self._api_call("api/v1/pipelines")

    def list_executions(self, pipeline: str):
        return self._api_call(f"api/v1/pipelines/{pipeline}/executions")

    def get_execution(self, pipeline: str, execution_id: str):
        uri = f"api/v1/pipelines/{pipeline}/executions/{execution_id}"
        return self._api_call(uri)
