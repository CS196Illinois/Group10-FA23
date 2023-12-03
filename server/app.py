import flask
from flask import request
from flask import Flask
from flask import jsonify
from haversine import haversine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from scipy.signal import medfilt

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
        return 'Walking'
    elif speed < threshold_bike:
        return 'Biking'
    else:
        return 'Driving'


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


@app.route("/stat", methods=["GET"], strict_slashes=False)
def get_stats():
    locations = Location.query.all()

    if locations:
        total_distance = 0
        total_points = len(locations)

        for i in range(1, total_points):
            coordinates1 = (locations[i - 1].latitude, locations[i - 1].longitude)
            coordinates2 = (locations[i].latitude, locations[i].longitude)

            distance = haversine(coordinates1, coordinates2)
            total_distance += distance

        speeds = []
        for i in range(1, total_points):
            coordinates1 = (locations[i - 1].latitude, locations[i - 1].longitude)
            coordinates2 = (locations[i].latitude, locations[i].longitude)

            time_difference = (iso8601_to_datetime(locations[i].timestamp) - iso8601_to_datetime(
                locations[i - 1].timestamp)).total_seconds()

            # Check if time difference is greater than zero to avoid division by zero
            if time_difference > 0:
                speed = haversine(coordinates1, coordinates2) / time_difference
                speeds.append(speed * 3600)  # Convert to kilometers per hour
            else:
                speeds.append(0.0)

        filtered_speeds = medfilt(speeds, kernel_size=5)

        # DEBUG
        print("Original speeds:", speeds)
        print("Filtered speeds:", filtered_speeds)

        # Classify movement for each segment
        segments = []
        if len(filtered_speeds) > 0:

            current_segment = {'start_index': 0, 'movement': classify_movement(filtered_speeds[0]), 'distance_for segment': 0}

            for i in range(1, len(filtered_speeds)):
                movement = classify_movement(filtered_speeds[i])

                if movement != current_segment['movement']:
                    current_segment['end_index'] = i - 1
                    segments.append(current_segment)
                    current_segment = {'start_index': i, 'movement': movement}

            current_segment['end_index'] = len(filtered_speeds) - 1
            segments.append(current_segment)

            if current_segment['start_index'] <= len(filtered_speeds) - 1:
                current_segment['end_index'] = len(filtered_speeds) - 1
                segments.append(current_segment)
        else:
            segments.append({'start_index': 0, 'end_index': 0, 'movement': 'Unknown'})

        # Calculate total time passed
        total_time_passed = (iso8601_to_datetime(locations[-1].timestamp) - iso8601_to_datetime(
            locations[0].timestamp)).total_seconds()
        
        total_average_speed = total_distance / total_time_passed * 360

        return jsonify({
            'total_distance_all_points_in_km': total_distance,
            'total_time_passed_in_seconds': total_time_passed,
            'total_average_speed_in_km_hr': total_average_speed,
            'segments': segments
        })
    else:
        return jsonify({'message': 'No data available'})


@app.route("/clear", methods=["GET"], strict_slashes=False)
def clear_data():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
    return jsonify({'message': 'Cleared tables'})


if __name__ == '__main__':
    app.run(debug=True)

""""average_speed_all_points = total_distance / total_points


        window_size = 5 
        current_time = iso8601_to_datetime(locations[-1].timestamp)
        start_time = current_time - timedelta(seconds=window_size)

        recent_locations = [loc for loc in locations if iso8601_to_datetime(loc.timestamp) >= start_time]

        if recent_locations:
            total_distance_recent = 0
            total_points_recent = len(recent_locations)

            for i in range(1, total_points_recent):
                coordinates1 = (recent_locations[i - 1].latitude, recent_locations[i - 1].longitude)
                coordinates2 = (recent_locations[i].latitude, recent_locations[i].longitude)

                distance = haversine(coordinates1, coordinates2)
                total_distance_recent += distance

            average_speed_recent = total_distance_recent / total_points_recent
        else:
            average_speed_recent = 0

        total_time_passed = (iso8601_to_datetime(locations[-1].timestamp) - iso8601_to_datetime(locations[0].timestamp)).total_seconds()


        return jsonify({
            'total_distance_all_points in km': total_distance,
            'average_speed_all_points in km/hr': average_speed_all_points,
            'total_distance_recent in km': total_distance_recent,
            'average_speed_recent in km': average_speed_recent,
            'total time passed in seconds': total_time_passed
 })"""
