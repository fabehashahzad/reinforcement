class StationDemandChecker:
    def __init__(self):
        self.total_swaps_hour = 0
        self.total_swaps_day = 0
        self.slot_empty = 0

    def update_swaps(self, swaps):
        self.total_swaps_hour += swaps
        self.total_swaps_day += swaps

    def update_slot_empty(self, slots):
        self.slot_empty = slots

    def check_demand(self):
        if self.total_swaps_hour > 10 and self.total_swaps_day > 25:
            if self.slot_empty == 0:
                return "High demand for the station! (No slots available)"
            else:
                self.slot_empty <= 4
                return "High demand for the station!"
        elif self.total_swaps_day > 5 and self.slot_empty>=9:
            return "Low demand for the station."
        else:
            return "Normal demand for the station."

while True:
    try:
        swaps_hour = int(input("Enter the total number of swaps in an hour (0-100, type 'quit' to exit): "))
        if swaps_hour < 0 or swaps_hour > 100:
            print("Please enter a value between 0 and 100.")
            continue

        if swaps_hour == 0:  # Exit the loop if the user enters 0
            break

        swaps_day = int(input("Enter the total number of swaps in a day (0-100): "))
        if swaps_day < 0 or swaps_day > 100:
            print("Please enter a value between 0 and 100.")
            continue

        slots_empty = int(input("Enter the number of empty slots (0-100): "))
        if slots_empty < 0 or slots_empty > 100:
            print("Please enter a value between 0 and 100.")
            continue
    except ValueError:
        print("Please enter valid numeric values for swaps and slots.")
        continue

    # Example usage:
    station_checker = StationDemandChecker()
    station_checker.update_swaps(swaps_hour)

    # Check demand at the end of the day
    station_checker.update_swaps(swaps_day - swaps_hour)  # Update with remaining swaps for the day
    station_checker.update_slot_empty(slots_empty)
    demand_status = station_checker.check_demand()
    print(demand_status)
