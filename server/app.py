import flask
import numpy as np
from flask import request
from flask import Flask
from flask import jsonify
from haversine import haversine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from scipy.signal import medfilt

UNKNOWN = -1
WALKING = 0
BIKING = 1
DRIVING = 2

chunk_time_threshold = 120

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'  # SQLite database file
db = SQLAlchemy(app)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


def iso8601_to_datetime(iso8601_timestamp):
    return datetime.fromisoformat(iso8601_timestamp)


def classify_movement(speed, threshold_walk=5, threshold_bike=15.0):
    if speed < threshold_walk:
        return WALKING
    elif speed < threshold_bike:
        return BIKING
    else:
        return DRIVING


@app.route("/location", methods=["POST"], strict_slashes=False)
def update_location():
    data = request.json

    if 'coords' in data and 'latitude' in data['coords'] and 'longitude' in data['coords'] and 'timestamp' in data:
        latitude = float(data['coords']['latitude'])
        longitude = float(data['coords']['longitude'])
        timestamp = iso8601_to_datetime(data['timestamp'])

        new_location = Location(latitude=latitude, longitude=longitude, timestamp=timestamp)
        db.session.add(new_location)
        db.session.commit()

        return jsonify({'message': 'Location data received successfully'})
    else:
        return jsonify({'error': 'Invalid data format'}), 400


def get_chunk_average_speed(speeds, location_start, location_end):
    return np.average(speeds[location_start: location_end])


def get_chunk_total_distance(distances, location_start, location_end):
    return np.sum(distances[location_start, location_end])


@app.route("/stat", methods=["GET"], strict_slashes=False)
def get_stats():
    locations = Location.query.all()
    if locations:
        num_locations = len(locations)
        speeds = [-1] * (num_locations - 1)
        distances = [-1] * (num_locations - 1)
        for i in range(1, num_locations):
            coordinates1 = (locations[i - 1].latitude, locations[i - 1].longitude)
            coordinates2 = (locations[i].latitude, locations[i].longitude)

            time_difference = (iso8601_to_datetime(locations[i].timestamp) - iso8601_to_datetime(
                locations[i - 1].timestamp)).total_seconds()
            distance = haversine(coordinates1, coordinates2)
            distances[i - 1] = distance
            speed = distance / time_difference
            speeds[i - 1] = speed * 3600  # Convert to kilometers per hour

        speeds = medfilt(speeds, kernel_size=5)
        previous_endpoint = 0
        chunk_endpoints = [0]
        for i in range(1, num_locations):
            time_difference = (iso8601_to_datetime(locations[i].timestamp) - iso8601_to_datetime(
                locations[previous_endpoint].timestamp)).total_seconds()
            if time_difference > chunk_time_threshold:
                chunk_endpoints.append(i)
                previous_endpoint = i

        chunk_distances = np.zeros(shape=(len(chunk_endpoints) - 1,))
        chunk_classes = np.full(shape=(len(chunk_endpoints) - 1,), fill_value=UNKNOWN)
        for i in range(1, len(chunk_endpoints)):
            chunk_speed = get_chunk_average_speed(speeds, chunk_endpoints[i - 1], chunk_endpoints[i])
            chunk_distance = get_chunk_total_distance(distances, chunk_endpoints[i - 1], chunk_endpoints[i])
            chunk_distances[i - 1] = chunk_distance
            chunk_class = classify_movement(chunk_speed)
            chunk_classes[i - 1] = chunk_class

        distance_biking = sum([chunk_distances[i] for i in range(len(chunk_distances)) if chunk_classes[i] == BIKING])
        return jsonify({'num_chunks': len(chunk_classes), 'distance_biking': distance_biking})


@app.route("/clear", methods=["GET"], strict_slashes=False)
def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    return jsonify({'message': 'Cleared tables'})


if __name__ == '__main__':
    app.run(debug=True)
