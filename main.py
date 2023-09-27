import os
import requests

from dotenv import load_dotenv
from pprint import pprint

load_dotenv('.env')

OPEN_WEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')

API_URL = "https://api.openweathermap.org/data/2.5"


def get_weather_by_geolocation(latitude: float, longitude: float) -> dict:
    """TODO"""
    try:
        response = requests.get(f"{API_URL}/weather?lat={latitude}&lon={longitude}&units=metric&appid={OPEN_WEATHER_API_KEY}")

        if response.status_code == 200:
            return response.json()

    except Exception as e:
        print(e)


def get_weather_by_city_id(city_id: int) -> dict:
    """TODO"""
    try:
        response = requests.get(f"{API_URL}/weather?id={city_id}&units=metric&appid={OPEN_WEATHER_API_KEY}")

        if response.status_code == 200:
            return response.json()

    except Exception as e:
        print(e)

if __name__ == '__main__':

    pprint(get_weather_by_city_id(3443013))

