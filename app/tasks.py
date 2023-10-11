"""TASK QUEUE

This module encapsulates the logic used for the task queue process involved
on fetching the weather data from OpenWeather API.

"""
import os
import json
import requests

from celery import Celery

from app import constants


app = Celery(
    __name__,
    broker=constants.REDIS_URL,
    backend=constants.REDIS_URL,
    broker_connection_retry_on_startup=True
)


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

    os.makedirs(constants.DATA_PATH, exist_ok=True)

    filename = f'{constants.DATA_PATH}/{user_id}.json'

    if not os.path.exists(filename):
        open(filename, 'w').close()

    with open(filename, 'r') as file:
        content = file.read()

        if content:
            user_data = json.loads(content)
    
    return user_data



@app.task(rate_limit='60/m')
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
    
    for location_id in constants.LOCATION_IDS:
        try:
            # 2nd STEP: Get weather info
            api_url = f"{constants.OPEN_WEATHER_API_URL}/weather?id={location_id}&appid={constants.OPEN_WEATHER_API_KEY}&units=metric"
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()

            user_data['cities'].append({
                'city_id': location_id,
                'temp': data.get('main').get('temp'),
                'humidity': data.get('main').get('humidity')
            })

            # 3rd STEP: Save user object
            filename = f"{constants.DATA_PATH}/{user_data['user_id']}.json"

            with open(filename, 'w') as file:
                json.dump(user_data, file, indent=2)
        
        except Exception as excp:
            print(f"Error when fetching data for location {location_id}:{excp}")
