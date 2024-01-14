import requests


class FlightAnalysisClient:
    def __init__(self, base_url="http://localhost:5000/flights"):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def get_destination(self):
        url = f'{self.__base_url}/destination'
        res = requests.get(url)
        return res.text

    def get_time(self):
        url = f'{self.__base_url}/time_date'
        res = requests.get(url)
        return res.text

    def get_date_destination(self):
        url = f'{self.__base_url}/date_destination'
        res = requests.get(url)
        return res.text

    def get_common_destinations(self):
        url = f'{self.__base_url}/common_destinations'
        res = requests.get(url)
        return res.text

    def get_delay_per_airline(self):
        url = f'{self.__base_url}/delay_per_airline'
        res = requests.get(url)
        return res.text

    def add_flight(self, data):
        response = requests.post(f"{self.base_url}/", json=data)
        return response.json()

    def update_flight(self, data):
        response = requests.put(f"{self.base_url}/", json=data)
        return response.json()

    def delete_flight(self, data):
        response = requests.delete(f"{self.base_url}/", json=data)
        return response.json()
