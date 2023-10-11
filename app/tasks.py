"""TASK QUEUE

This module encapsulates the logic used for the task queue process involved
on fetching the weather data from OpenWeather API.

"""
from dotenv import load_dotenv; load_dotenv() #TODO: Remove this asap
import os
import json
import requests

from celery import Celery

from app.constants import LOCATION_IDS


REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379')
DATA_PATH = os.environ.get('DATA_PATH', 'data')

OPEN_WEATHER_API_URL = os.environ.get('OPEN_WEATHER_API_URL')
OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')


app = Celery(__name__, broker=REDIS_URL, backend=REDIS_URL)


def get_user_data(user_id: int) -> dict:
    """Tries to recover user information if it already exists.
    
    Arguments
    ---------
    user_id: int
        An user identifier number.

    Returns
    -------
    dict: The data regarding that specific user.
    
    """
    user_data = None

    os.makedirs(DATA_PATH, exist_ok=True)

    filename = f'{DATA_PATH}/{user_id}.json'

    if not os.path.exists(filename):
        open(filename, 'w').close()

    with open(filename, 'r') as file:
        content = file.read()

        if content:
            user_data = json.loads(content)
    
    return user_data



@app.task
def capture_weather_info(user_id: int, datetime: str) -> None:
    """Retrieves weather data from OpenWeather API.

    Arguments
    ---------
    user_id: int
        An user identifier number.
    datetime: str
        The datetime that represents the current time of processing.

    Returns
    -------
    None
    
    """
    # 1st STEP: Get user data
    user_data = get_user_data(user_id)
    
    if not user_data:
        user_data = {
            'user_id': user_id,
            'request_datetime': datetime,
            'cities': []
        }
    
    for location_id in LOCATION_IDS:
        try:
            # 2nd STEP: Get weather info
            api_url = f"{OPEN_WEATHER_API_URL}/weather?id={location_id}&appid={OPEN_WEATHER_API_KEY}&units=metric"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

            user_data['cities'].append({
                'city_id': location_id,
                'temp': data.get('main').get('temp'),
                'humidity': data.get('main').get('humidity')
            })

            # 3rd STEP: Save user object
            filename = f"{DATA_PATH}/{user_data['user_id']}.json"

            with open(filename, 'w') as file:
                json.dump(user_data, file, indent=2)
        
        except Exception as excp:
            print(f"Error when fetching data for location {location_id}:{excp}")
