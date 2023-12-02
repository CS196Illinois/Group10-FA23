import flask
from flask import request
from flask import jsonify
from haversine import haversine
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'  # SQLite database file
db = SQLAlchemy(app)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.Float, nullable=False)

db.create_all()

@app.route("/location", methods=["POST"], strict_slashes=False)

def update_location():
    data = request.json

    if 'latitude' in data and 'longitude' in data and 'timestamp' in data:
        latitude = float(data['latitude'])
        longitude = float(data['longitude'])
        timestamp = float(data['timestamp'])

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

        average_speed_all_points = total_distance / total_points

     
        window_size = 5 
        current_time = datetime.fromtimestamp(locations[-1].timestamp)
        start_time = current_time - timedelta(seconds=window_size)

        recent_locations = [loc for loc in locations if datetime.fromtimestamp(loc.timestamp) >= start_time]

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

        return jsonify({
            'total_distance_all_points': total_distance,
            'average_speed_all_points': average_speed_all_points,
            'total_distance_recent': total_distance_recent,
            'average_speed_recent': average_speed_recent
        })
    else:
        return jsonify({'message': 'No data available'})



