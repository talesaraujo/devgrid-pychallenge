import os
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.tasks import capture_weather_info


def test_post_endpoint_must_return_data_successfully():
    capture_weather_info.delay(
        user_id=6969, datetime="2023-10-10 22:17:43.794951"
    )

    print(os.listdir('data'))

    time.sleep(2)
    assert os.path.isfile(os.path.join('data', '6969.json'))
