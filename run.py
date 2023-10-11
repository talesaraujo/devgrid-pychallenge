from app.tasks import capture_weather_info

if __name__ == '__main__':
    capture_weather_info.delay('125', '11/10/2023')
