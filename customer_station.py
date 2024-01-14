import time
from math import radians, sin, cos, sqrt, atan2
from geopy.distance import geodesic
from concurrent.futures import ThreadPoolExecutor
import random

class Station:
    def __init__(self, name, location):
        self.name = name
        self.location = location

class Customer:
    def __init__(self):
        self.vehicle_type = None
        self.has_batteries = False
        self.location = None

    def get_vehicle_type(self):
        while True:
            vehicle_type = input("Are you a bike owner or cargo owner? Enter 'bike' or 'cargo': ").lower()
            if vehicle_type in ['bike', 'cargo']:
                self.vehicle_type = vehicle_type
                break
            else:
                print("Invalid input. Please enter 'bike' or 'cargo'.")

    def get_location(self):
        if self.vehicle_type == 'bike':
            try:
                latitude = float(input("Enter your latitude: "))
                longitude = float(input("Enter your longitude: "))
                self.location = (latitude, longitude)
            except ValueError:
                print("Invalid input. Please enter numeric values for latitude and longitude.")

    def get_batteries_info(self):
        if self.vehicle_type == 'cargo':
            batteries_info = input("Do you have batteries? Enter 'yes' or 'no': ").lower()
            self.has_batteries = batteries_info == 'yes'

class StationChooser:
    def __init__(self):
        self.stations = [
            Station("Station A", (41.8781, -87.6298)),
            Station("Station B", (37.7749, -122.4194)),
            Station("Station C", (34.0522, -118.2437)),
            Station("Station D", (40.7128, -74.0060)),
            Station("Station E", (51.5074, -0.1278))
        ]

    def demand(self, station):
        # Simulate demand as a random value between 0 and 20
        return station.name, random.randint(0, 20)

    def monitor_demand(self):
        with ThreadPoolExecutor(max_workers=len(self.stations)) as executor:
            demand_results = executor.map(self.demand, self.stations)

        print("Demand Monitoring:")
        for station_name, demand_value in demand_results:
            print(f"{station_name}: {demand_value} swaps/hour")

    def suggest_destinations(self):
        print("EV CHARGING BIKE")

    def predict_destination(self, customer):
        if customer.vehicle_type == 'bike' and customer.location:
            distances = []
            for station in self.stations:
                distance = haversine(customer.location[0], customer.location[1], station.location[0], station.location[1])
                distances.append((station.name, distance))

            print("Distances to Stations:")
            for station_name, distance in distances:
                print(f"{station_name}: {distance:.2f} kilometers")

            nearest_station = min(distances, key=lambda x: x[1])
            return nearest_station[0]
        elif customer.vehicle_type == 'bike':
            print("Location not provided. Cannot calculate distances.")
        elif customer.vehicle_type == 'cargo' and customer.has_batteries:
            self.monitor_demand()

            # Find the station with the maximum number of swaps in the last hour
            max_demand_station = max(self.stations, key=lambda station: self.demand(station)[1])
            time.sleep(2)
            print(f"The user should go to {max_demand_station.name} (Demand: {self.demand(max_demand_station)[1]} swaps/hour)")
            return max_demand_station.name
        elif customer.vehicle_type == 'cargo' and not customer.has_batteries:
            return "solar farm"

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Radius of the Earth in kilometers (mean value)
    radius = 6371.0

    # Calculate the distance
    distance = radius * c

    return distance

def main():
    station_chooser = StationChooser()
    station_chooser.suggest_destinations()

    time.sleep(2)  # Delay for 2 seconds

    customer = Customer()
    customer.get_vehicle_type()

    if customer.vehicle_type == 'bike':
        customer.get_location()
    elif customer.vehicle_type == 'cargo':
        customer.get_batteries_info()

    destination = station_chooser.predict_destination(customer)

    print("After considering the input,")
    time.sleep(1)  # Delay for 1 second

    if customer.vehicle_type == 'bike':
        nearest_station = min(station_chooser.stations, key=lambda station: haversine(customer.location[0], customer.location[1], station.location[0], station.location[1]))
        print(f"The user should go to {destination} (Distance: {haversine(customer.location[0], customer.location[1], nearest_station.location[0], nearest_station.location[1]):.2f} kilometers)")
        time.sleep(1.5)
        print(f"......Bike owner from location {customer.location} is going to {destination}")
    elif customer.vehicle_type == 'cargo':
        time.sleep(2)
        print(f"......Cargo owner is going to {destination}")
        time.sleep(2)
        print("cargo has reached to the destination")

        # Check if the user has batteries
        
if __name__ == "__main__":
    main()
