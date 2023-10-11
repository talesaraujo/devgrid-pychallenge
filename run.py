from app.tasks import capture_weather_info

if __name__ == '__main__':
    capture_weather_info.delay('124', '10/10/2023')
