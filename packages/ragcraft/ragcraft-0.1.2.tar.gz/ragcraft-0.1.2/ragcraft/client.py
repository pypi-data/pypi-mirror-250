import requests
import os 

class Ragcraft:
    def __init__(self, base_url):
        self.base_url = base_url
        self.api_key = os.getenv('RAGCRAFT_API_KEY')

    def generate(self, payload):
        payload["ragcraft_api_key"] = self.api_key
        response = requests.post(f"{self.base_url}/api/generate", json=payload)
        return response.json()

    def list_datasets(self):
        params = {"ragcraft_api_key": self.api_key}
        response = requests.get(f"{self.base_url}/api/dataset/list", params=params)
        return response.json()
 
    def fetch(self, payload):
        params = {
            "dataset_id": payload["dataset_id"],
            "org_id": payload["org_id"],
            "skip": payload["skip"],
            "limit": payload["limit"],
            "ragcraft_api_key": self.api_key
        }
        response = requests.get(f"{self.base_url}/api/qa-data", params=params)
        return response.json()

    def evaluate(self, query_params):
        response = requests.get(f"{self.base_url}/api/evaluate", params=query_params)
        return response.json()

