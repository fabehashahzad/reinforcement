from flask import Flask, request, jsonify
from math import radians, sin, cos, sqrt, atan2
from flask_cors import CORS
app = Flask(_name_)
CORS(app)
# Station coordinates
stations = {
    'Johar': {'latitude': 24.8934, 'longitude': 67.0281},
    'NIPA': {'latitude': 24.9178, 'longitude': 67.0736},
    'Gulshan': {'latitude': 24.9415, 'longitude': 67.0822},
    'Airport': {'latitude': 24.8998, 'longitude': 67.1681},
    'Malir': {'latitude': 24.9169, 'longitude': 67.2059},
    'Saddar': {'latitude': 27.7172, 'longitude': 67.0694},
    'DHA Phase 6': {'latitude': 24.9408, 'longitude': 67.1297},
    'Clifton': {'latitude': 24.8617, 'longitude': 67.0353},
    'Defense Housing Authority': {'latitude': 24.8664, 'longitude': 67.0156},
    'Nazimabad': {'latitude': 24.9454, 'longitude': 67.0661},
    'KDA Scheme 1': {'latitude': 24.8922, 'longitude': 67.0642},
}

@app.route('/suggest-location', methods=['POST'])
def suggest_location():
    data = request.json

    option = data.get('option')
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    has_batteries = data.get('hasBatteries')

    try:
        if not (option and latitude and longitude and has_batteries):
            raise ValueError("Incomplete data provided")

        if option == 'cargo':
            suggested_location = handle_cargo_suggestion(latitude, longitude, has_batteries)
        else:
            suggested_location = calculate_suggested_location(latitude, longitude)

        return jsonify({'suggestedLocation': suggested_location})

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400  # Bad Request

    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500  # Internal Server Error

def calculate_distance(coord1, coord2):
    # Haversine formula for distance calculation
    R = 6371  # Radius of the Earth in kilometers

    lat1, lon1 = radians(coord1['latitude']), radians(coord1['longitude'])
    lat2, lon2 = radians(coord2['latitude']), radians(coord2['longitude'])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)*2 + cos(lat1) * cos(lat2) * sin(dlon / 2)*2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def calculate_suggested_location(latitude, longitude):
    user_coords = {'latitude': latitude, 'longitude': longitude}

    # Find the station with the minimum distance
    min_distance = float('inf')
    suggested_location = None

    for station, coords in stations.items():
        distance = calculate_distance(user_coords, coords)
        if distance < min_distance:
            min_distance = distance
            suggested_location = station

    return suggested_location

def handle_cargo_suggestion(latitude, longitude, has_batteries):
    if has_batteries.lower() == 'yes':
        # Suggest the farthest station
        suggested_location = calculate_farthest_station(latitude, longitude)
    elif has_batteries.lower() == 'no':
        # Suggest "Solar Farm"
        suggested_location = 'Solar Farm'
    else:
        raise ValueError("Invalid value for 'hasBatteries'")

    return suggested_location

def calculate_farthest_station(latitude, longitude):
    # Implement logic to calculate the farthest station
    # You can use the Haversine formula to calculate distances
    # Example: For simplicity, just return one of the hardcoded locations for now
    return 'Saddar'

if _name_ == '_main_':
    app.run(debug=True)