import requests


class SearchFlightClient:
    def __init__(self, base_url="http://localhost:5000/search_flights"):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def search_by_destination(self, destination):
        url = f'{self.__base_url}/by_destination/{destination}'
        res = requests.get(url)
        return res.text

    def search_by_date(self, date):
        url = f'{self.__base_url}/by_date/{date}'
        res = requests.get(url)
        return res.text

    def search_by_date_time(self, date, time):
        url = f'{self.__base_url}/by_date_time/{date}/{time}'
        res = requests.get(url)
        return res.text

    def search_by_date_destination(self, date, destination):
        url = f'{self.__base_url}/by_date_destination/{date}/{destination}'
        res = requests.get(url)
        return res.text

