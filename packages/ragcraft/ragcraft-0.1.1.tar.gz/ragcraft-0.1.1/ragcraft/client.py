import requests
import os 

class Datacraft:
    def __init__(self, base_url):
        self.base_url = base_url
        self.api_key = os.getenv('DATACRAFT_API_KEY')

    def generate(self, payload):
        payload["datacraft_api_key"] = self.api_key
        response = requests.post(f"{self.base_url}/api/generate", json=payload)
        return response.json()

    def list_datasets(self):
        params = {"datacraft_api_key": self.api_key}
        response = requests.get(f"{self.base_url}/api/dataset/list", params=params)
        return response.json()
 
    def fetch(self, payload):
        params = {
            "dataset_id": payload["dataset_id"],
            "org_id": payload["org_id"],
            "skip": payload["skip"],
            "limit": payload["limit"],
            "datacraft_api_key": self.api_key
        }
        response = requests.get(f"{self.base_url}/api/qa-data", params=params)
        return response.json()

    def evaluate(self, query_params):
        response = requests.get(f"{self.base_url}/api/evaluate", params=query_params)
        return response.json()

