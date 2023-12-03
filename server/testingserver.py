
import requests
import json
from datetime import datetime, timedelta
#def createtest(latitude, longitude, timestamp)

#For every 2 minutes, change longitude by 0.115 to keep in the biking threshold.
URL = "http://127.0.0.1:5000/location"

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

payload = json.loads(body)


for i in range(100):

    payload['coords']['longitude'] += 0.115
    payload['timestamp'] = (datetime.fromisoformat(payload['timestamp']) + timedelta(minutes=2)).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%S") + 'Z'    

    response = requests.post(URL, json=payload)

    print(f"Request {i + 1}: {response.status_code}")
    print(response.text)

   