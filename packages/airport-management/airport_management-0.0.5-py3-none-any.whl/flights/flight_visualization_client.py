import requests
from PIL import Image
from io import BytesIO


class FlightVisualizationClient:
    def __init__(self, base_url="http://localhost:5000/visualization"):
        self.__base_url = base_url

    @property
    def base_url(self):
        return self.__base_url

    def destination_delay_plot(self):
        url = f'{self.__base_url}/destination_delay'
        res = requests.get(url)

        if res.status_code == 200:
            image_bytes = res.content
            img = Image.open(BytesIO(image_bytes))
            img.show()
            return img

        else:
            print(f"Error: Unable to fetch image. Status Code: {res.status_code}")
            return None

    def destination_frequency_plot(self):
        url = f'{self.__base_url}/destination_frequency'
        res = requests.get(url)

        if res.status_code == 200:
            image_bytes = res.content
            img = Image.open(BytesIO(image_bytes))
            img.show()
            return img

        else:
            print(f"Error: Unable to fetch image. Status Code: {res.status_code}")
            return None

    def airline_delay_plot(self):
        url = f'{self.__base_url}/airline_delay'
        res = requests.get(url)

        if res.status_code == 200:
            image_bytes = res.content
            img = Image.open(BytesIO(image_bytes))
            img.show()
            return img

        else:
            print(f"Error: Unable to fetch image. Status Code: {res.status_code}")
            return None

