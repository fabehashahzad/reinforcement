from flask import Flask, request, jsonify
from math import radians, sin, cos, sqrt, atan2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# Station coordinates
#
stations = {
    'North karachi': {'latitude': 24.988864, 'longitude': 67.060129},
    'NIPA': {'latitude': 24.916052, 'longitude': 67.097590},
    'Gulshan': {'latitude': 24.903651, 'longitude': 67.075440},
    'Airport': {'latitude': 24.900976, 'longitude': 67.164841},
    'Malir': {'latitude': 24.883098, 'longitude': 67.177078},
    'Saddar': {'latitude': 27.849422, 'longitude': 67.005415},
    'Johar': {'latitude': 24.903321, 'longitude': 67.113814},
    'Bahria Town': {'latitude': 25.001277, 'longitude': 67.316021},
    'Defense Housing Authority': {'latitude': 24.820710, 'longitude': 67.071325},
    'Korangi': {'latitude': 24.838487, 'longitude': 67.141990},
    'Tariq Road': {'latitude': 24.900976, 'longitude': 67.164841},
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

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
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
        suggested_location = calculate_highdemand_station(latitude, longitude)
    elif has_batteries.lower() == 'no':
        # Suggest "Solar Farm"
        suggested_location = 'Solar Farm'
    else:
        raise ValueError("Invalid value for 'hasBatteries'")

    return suggested_location

def calculate_highdemand_station(latitude, longitude):
    # Implement logic to calculate the farthest station
    # You can use the Haversine formula to calculate distances
    # Example: For simplicity, just return one of the hardcoded locations for now
    return 'Nipa'

if __name__ == '__main__':
    app.run(debug=True)