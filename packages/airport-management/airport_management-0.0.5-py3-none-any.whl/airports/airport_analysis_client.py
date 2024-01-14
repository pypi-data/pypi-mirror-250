import requests


class AirportAnalysisClient:
    def __init__(self, base_url='http://127.0.0.1:5000/airports'):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def get_airports(self):
        url = f'{self.base_url}/list'
        response = requests.get(url)
        return response.text

    def add_airport(self, data):
        response = requests.post(f"{self.base_url}/", json=data)
        return response.json()

    def update_airport(self, data):
        response = requests.put(f"{self.base_url}/{data['icao']}", json=data)
        return response.json()

    def delete_airport(self, data):
        response = requests.delete(f"{self.base_url}/{data['icao']}", json=data)
        return response.json()
