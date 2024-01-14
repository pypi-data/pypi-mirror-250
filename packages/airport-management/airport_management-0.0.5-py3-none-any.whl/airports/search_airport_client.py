import requests


class SearchAirportClient:

    def __init__(self, base_url='http://127.0.0.1:5000/search_airports'):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def search_by_city(self, city):
        url = f'{self.base_url}/by_city/{city}'
        response = requests.get(url)
        return response.text

    def search_by_country(self, country):
        url = f'{self.base_url}/by_country/{country}'
        response = requests.get(url)
        return response.text

    def search_weather(self, iata, date, time):
        url = f'{self.base_url}/weather/{iata}/{date}/{time}'
        response = requests.get(url)
        return response.text

    def distance(self, dep_iata, arr_iata):
        url = f'{self.base_url}/distance/{dep_iata}/{arr_iata}'
        response = requests.get(url)
        return response.text
