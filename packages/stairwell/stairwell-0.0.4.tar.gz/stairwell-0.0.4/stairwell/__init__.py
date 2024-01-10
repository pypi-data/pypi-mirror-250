import requests

class Client:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_asset(self, asset_id):
        url = f"https://app.stairwell.com/v1/assets/{asset_id}"
        headers = {
            "Content-Type": "application/json",
            "X-Api-Source": "Stairwell Python Client",
            'Authorization': self.api_key,
        }
        response = requests.get(url, headers=headers)
        return response.text
