import os
import asyncio
import httpx


from datetime import datetime
from dotenv import load_dotenv

load_dotenv('.env')

OPEN_WEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')

API_URL = "https://api.openweathermap.org/data/2.5"






async def get_weather_by_geolocation(latitude: float, longitude: float) -> dict:
    """TODO"""
    try:
        response = httpx.get(f"{API_URL}/weather?lat={latitude}&lon={longitude}&units=metric&appid={OPEN_WEATHER_API_KEY}")

        if response.status_code == 200:
            return response.json()

    except Exception as e:
        print(e)


async def get_weather_by_city_id(city_id: int) -> dict:
    """TODO"""
    print(f"{datetime.now()} | [{city_id}]")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/weather?id={city_id}&units=metric&appid={OPEN_WEATHER_API_KEY}")

        if response.status_code == 200:
            # print(response.json())
            return response.json()

    except Exception as e:
        print(e)
    


async def main() -> None:
    # print(get_weather_by_city_id(3443013))
    # print(get_weather_by_geolocation(-3.736568, -38.571617))


    # for idx, location in enumerate(locations_list):
    #     print(f"{datetime.now()} | [{idx+1}/{len(locations_list)}]")
    #     info = await get_weather_by_city_id(location)
    #     data.append(info)
    # Retrieve locations list
    with open('locations_list.txt', 'r') as loc_list:
        locations_list = loc_list.readlines()

    locations_list = [ int(line[:-1]) for line in locations_list ]


    locations_list = locations_list + locations_list + locations_list + locations_list

    data = [ get_weather_by_city_id(location) for location in locations_list ]
    await asyncio.gather(*data)

    print(len(data))


if __name__ == '__main__':
    asyncio.run(main())
