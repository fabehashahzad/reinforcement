
import time
from math import radians, sin, cos, sqrt, atan2
from concurrent.futures import ThreadPoolExecutor
import random
import csv

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
            vehicle_type = input("Are you a bike owner or cargo owner? Enter 'bike' or 'cargo' (or 'exit' to quit): ").lower()
            
            if vehicle_type == 'exit':
                break

            if vehicle_type in ['bike', 'cargo']:
                self.vehicle_type = vehicle_type
                break
            else:
                print("Invalid input. Please enter 'bike' or 'cargo'.")

    def get_location(self):
        try:
            latitude = float(input("Enter your latitude: "))
            longitude = float(input("Enter your longitude: "))
            self.location = (latitude, longitude)
        except ValueError:
            print("Invalid input. Please enter numeric values for latitude and longitude.")

    def get_batteries_info(self):
        if self.vehicle_type == 'cargo':
            try:
                latitude = float(input("Enter your cargo latitude: "))
                longitude = float(input("Enter your cargo longitude: "))
                self.location = (latitude, longitude)
            except ValueError:
                print("Invalid input. Please enter numeric values for cargo latitude and longitude.")
            batteries_info = input("Do you have batteries? Enter 'yes' or 'no': ").lower()
            self.has_batteries = batteries_info == 'yes'


class StationChooser:
    def __init__(self):
        self.stations = [
            Station("Station A", (random.uniform(30, 40), random.uniform(-90, -80))),
            Station("Station B", (random.uniform(35, 45), random.uniform(110, 100))),
            Station("Station C", (random.uniform(32, 42), random.uniform(-105, -95))),
            Station("Station D", (random.uniform(38, 48), random.uniform(-70, -100))),
            Station("Station E", (random.uniform(28, 38), random.uniform(65, 90)))
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

            if distances:
                nearest_station = min(distances, key=lambda x: x[1])
                print(f"The user should go to {nearest_station[0]} (Distance: {nearest_station[1]:.2f} kilometers)")
                return nearest_station[0]
            else:
                print("No stations available.")
        elif customer.vehicle_type == 'bike':
            print("Location not provided. Cannot calculate distances.")
        elif customer.vehicle_type == 'cargo' and customer.has_batteries:
            # Calculate demand for each station
            demands = [(station, self.demand(station)[1]) for station in self.stations]
            print("Demands for Stations:")
            for station, demand_value in demands:
                print(f"{station.name}: {demand_value} swaps/hour")

            # Find stations with the maximum demand
            max_demand_value = max(demands, key=lambda x: x[1])[1]
            max_demand_stations = [station for station, demand_value in demands if demand_value == max_demand_value]

            # If there are multiple stations with the same demand, choose the nearest one
            if len(max_demand_stations) > 1 and customer.location:
                distances_to_max_demand_stations = [(station, haversine(customer.location[0], customer.location[1], station.location[0], station.location[1])) for station in max_demand_stations]
                nearest_station = min(distances_to_max_demand_stations, key=lambda x: x[1])
                time.sleep(2)
                print(f"The user should go to {nearest_station[0].name} (Demand: {max_demand_value} swaps/hour, Distance: {nearest_station[1]:.2f} kilometers)")
                return nearest_station[0].name
            elif max_demand_stations:
                time.sleep(2)
                print(f"The user should go to {max_demand_stations[0].name} (Demand: {max_demand_value} swaps/hour)")
                return max_demand_stations[0].name
            else:
                print("No stations available.")
        elif customer.vehicle_type == 'cargo' and not customer.has_batteries:
            # Commented out the CSV append statement
            # append_to_csv("cargo_user.csv", ["solar farm", time.strftime("%Y-%m-%d %H:%M:%S")])
            print("User should go to solar farm.")
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
    while True:
        station_chooser = StationChooser()
        station_chooser.suggest_destinations()

        time.sleep(2)  # Delay for 2 seconds

        customer = Customer()
        customer.get_vehicle_type()

        if customer.vehicle_type == 'bike':
            customer.get_location()
            # Commented out the CSV append statement
            # append_to_csv("bike_user.csv", [customer.location[0], customer.location[1], time.strftime("%Y-%m-%d

        elif customer.vehicle_type == 'cargo':
            customer.get_batteries_info()

        destination = station_chooser.predict_destination(customer)

        print("After considering the input,")
        time.sleep(1)  # Delay for 1 second
        if customer.vehicle_type == 'bike':
            nearest_station = min(station_chooser.stations, key=lambda station: haversine(customer.location[0], customer.location[1], station.location[0], station.location[1]))
            print(f"The user should go to {nearest_station.name} (Distance: {haversine(customer.location[0], customer.location[1], nearest_station.location[0], nearest_station.location[1]):.2f} kilometers)")

            time.sleep(1.5)
            print(f"......Bike owner from location {customer.location} is going to {destination}")
        elif customer.vehicle_type == 'cargo':
            time.sleep(1.8)
            print(f"......Cargo owner is going to {destination}")
            time.sleep(2)
            print("cargo has reached the destination")

if __name__ == "__main__":
    main()
    