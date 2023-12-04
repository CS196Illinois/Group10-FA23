import requests
import json
from datetime import datetime, timedelta

# def createtest(latitude, longitude, timestamp)

# For every 2 minutes, change longitude by 0.115 to keep in the biking threshold.
URL = "http://127.0.0.1:5000"

body = json_data = '''
{
  "extras": {},
  "battery": {
    "level": 0.27,
    "is_charging": true
  },
  "activity": {
    "confidence": 100,
    "type": "walking"
  },
  "is_moving": true,
  "age": 308,
  "uuid": "91ad2c8f-5de5-4835-aac3-23e5d890c429",
  "odometer": 646.5999755859375,
  "coords": {
    "age": 327,
    "ellipsoidal_altitude": 203.2,
    "altitude": 203.2,
    "altitude_accuracy": 1,
    "heading_accuracy": -1,
    "heading": 281.04,
    "speed": 0.23,
    "accuracy": 11.7,
    "longitude": -88.2199634,
    "speed_accuracy": -1,
    "latitude": 40.1002697
  },
  "timestamp": "2023-12-02T06:34:03.394Z"
}
'''
speed1 = 12  # biking speed = 12 km/h
speed2 = 4  # walking speed = 4 km/h
speed3 = 40  # driving speed = 40 km/h
longitude_delta1 = ((speed1 / 1.6) / 54.6) / 30
longitude_delta2 = ((speed2 / 1.6) / 54.6) / 30
longitude_delta3 = ((speed3 / 1.6) / 54.6) / 30
time_delta = 2  # update every 2 minutes

response = requests.get(URL + "/clear")  # clear previous data
payload = json.loads(body)

for i in range(150):
    if i < 25 or 50 <= i < 75:
        # biking from 0 - 24 and 50 - 74
        payload['coords']['longitude'] += longitude_delta1
    elif i < 100:
        # walking from 25 - 49 and 76 - 99
        payload['coords']['longitude'] += longitude_delta2
    else:
        # driving from 100 - 149
        payload['coords']['longitude'] += longitude_delta3
    payload['timestamp'] = (datetime.fromisoformat(payload['timestamp']) + timedelta(minutes=time_delta)).isoformat()
    response = requests.post(URL + "/location", json=payload)

response = requests.get(URL + "/stat")
# total expected biking distance = (100 / 60) h * 12 km / h = 20 km
print(response.text)
