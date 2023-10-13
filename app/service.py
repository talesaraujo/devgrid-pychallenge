"""API WEBSERVICE

This module implements the API webservice that provides the interface for
weather data fetching.

"""
from fastapi import FastAPI, HTTPException, status
from starlette.responses import RedirectResponse
from pydantic import BaseModel
from datetime import datetime

from app.tasks import capture_weather_info, get_user_data
from app.constants import LOCATION_IDS


app = FastAPI(
    title="DevGrid OpenWeather Service",
    description="""A simple web-service that wraps the OpenWeather API so as
to provide information about the temperature of certain locations.""",
    version="0.1"
)

# ------------------------------ MODELS --------------------------------------#

class UserSchema(BaseModel):
    """Definition of the endpoint payload for the user data."""
    user_id: int

# ---------------------------- ENDPOINTS -------------------------------------#

@app.post('/weather', status_code=status.HTTP_200_OK)
def start_capturing_weather_info(payload: UserSchema) -> dict:
    """Gets weather information for a given user id."""
    user_id = payload.user_id

    now = str(datetime.now())

    try:
        capture_weather_info.delay(user_id, now)

        return {
            'status': 'Now starting collecting weather info...'
        }
    
    except Exception as excp:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error while running weather data collection task. Starting over...'
        ) from excp



@app.get('/weather/{user_id}', status_code=status.HTTP_200_OK)
def show_weather_capture_progress(user_id: int) -> dict:
    """Displays the progress of the data fetching process for a specific user."""
    user_data = get_user_data(user_id)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No such user with data to be monitored.'
        )

    progress = (len(user_data['cities']) / len(LOCATION_IDS)) * 100
    
    return {
        'progress': f"{round(progress, 2)}%"
    }


@app.get("/", tags=['index'], include_in_schema=False)
def index():
    """API Index."""
    response = RedirectResponse(url="/docs")
    return response
