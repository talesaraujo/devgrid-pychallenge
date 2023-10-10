import os
import asyncio
import httpx


from datetime import datetime
from dotenv import load_dotenv
from random import randint
from pprint import pprint

load_dotenv('.env')

OPEN_WEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')

API_URL = "https://api.openweathermap.org/data/2.5"

user_defined_id = randint(0, 1000)


def iterate_chunks(lst: list, n: int) -> list:
    """"""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]
    



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
    print(f"{datetime.now()} | {user_defined_id} | [{city_id}]")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/weather?id={city_id}&units=metric&appid={OPEN_WEATHER_API_KEY}")

        if response.status_code == 200:
            # print(response.json())
            return response.json()

    except Exception as e:
        print(e)


async def get_weather_by_city_several_ids(city_ids: list) -> dict:
    """TODO"""
    # print(f"{datetime.now()} | {user_defined_id} | [{city_id}]")

    # city_ids = city_ids[:20]

    if len(city_ids) > 20:
        raise Exception("OpenWeather API does not support more than 20 ids per request.")

    endpoint_entry = ",".join(city_ids)

    url = f"{API_URL}/group?id={endpoint_entry}&units=metric&appid={OPEN_WEATHER_API_KEY}"

    print(url)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            print(response.status_code)
            assert response.status_code == 200

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

    locations_list = [ str(line[:-1]) for line in locations_list ]


    # locations_list = locations_list + locations_list + locations_list + locations_list
    locations_list = locations_list * 20

    print(len(locations_list))

    # data = [ get_weather_by_city_id(location) for location in locations_list ]
    # await asyncio.gather(*data)

    # print(len(data))

    data = []

    for chunk in iterate_chunks(locations_list, 20):
        response = await get_weather_by_city_several_ids(chunk)
        data.append(response)

    # pprint(data)
    # import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    asyncio.run(main())
