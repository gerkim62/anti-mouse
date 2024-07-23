import requests

class APIClient:
    def __init__(self, api_endpoint):
        self.api_endpoint = api_endpoint

    def get_alternative(self, query):
       
        return "Error: Unable to fetch alternative"