"""TODO Module docstring"""
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
    # 1st STEP: Get user object
    user_object = None

    os.makedirs(DATA_PATH, exist_ok=True)

    filename = f'{DATA_PATH}/{user_id}.json'

    if not os.path.exists(filename):
        open(filename, 'w').close()

    with open(filename, 'r') as file:
        content = file.read()

        if content:
            user_object = json.loads(content)
    
    if not user_object:
        user_object = {
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

            user_object['cities'].append({
                'city_id': location_id,
                'temp': data.get('main').get('temp'),
                'humidity': data.get('main').get('humidity')
            })

            # 3rd STEP: Save user object
            filename = f"{DATA_PATH}/{user_object['user_id']}.json"

            with open(filename, 'w') as file:
                json.dump(user_object, file, indent=2)
        
        except Exception as excp:
            print(f"Error when fetching data for location {location_id}:{excp}")
