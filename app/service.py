from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

from app.tasks import capture_weather_info, get_user_data
from app.constants import LOCATION_IDS


description = """description"""

app = FastAPI(
    title="DevGrid OpenWeather Service",
    description=description,
    version="0.1"
)


class UserSchema(BaseModel):
    """TODO"""
    user_id: int


@app.post('/weather', status_code=status.HTTP_200_OK)
def start_capturing_weather_info(payload: UserSchema) -> dict:
    """TODO"""
    user_id = payload.user_id

    now = str(datetime.now())

    try:
        capture_weather_info.delay(user_id, now)

        return {
            'status': 'Now starting collecting weather info'
        }
    
    except Exception as excp:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error while running weather data collection task. Starting over...'
        ) from excp



@app.get('/weather/{user_id}', status_code=status.HTTP_200_OK)
def show_weather_capture_progress(user_id: int) -> dict:
    """TODO"""
    user_data = get_user_data(user_id)

    if not user_data:
        return {
            'info': 'No such user with data to be monitored.'
        }

    progress = (len(user_data['cities']) / len(LOCATION_IDS)) * 100
    
    return {
        'progress': f"{round(progress, 2)}%"
    }
