import numpy as np

class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1):
        self.q_values = {}
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob

    def get_state_action_pair(self, state, action):
        return tuple([state.total_swaps_hour, state.total_swaps_day, state.slot_empty, action])

    def get_q_value(self, state, action):
        state_action_pair = self.get_state_action_pair(state, action)
        return self.q_values.get(state_action_pair, 0)

    def update_q_value(self, state, action, new_value):
        state_action_pair = self.get_state_action_pair(state, action)
        self.q_values[state_action_pair] = new_value

    def select_action(self, state):
        if np.random.rand() < self.exploration_prob:
            return np.random.choice(["High", "Low", "Normal"])
        else:
            q_values = [self.get_q_value(state, action) for action in ["High", "Low", "Normal"]]
            return ["High", "Low", "Normal"][np.argmax(q_values)]

def perform_action(action):
    if action == "High":
        return "High demand for the station!"
    elif action == "Low":
        return "Low demand for the station."
    else:
        return "Normal demand for the station."

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

    def check_demand(self, action):
        if action == "High":
            return self.slot_empty == 0, "High demand for the station! (No slots available)"
        else:
            return True, perform_action(action)

# Reinforcement Learning Training Loop
agent = QLearningAgent()

for episode in range(1000):  # You may adjust the number of episodes
    station_checker = StationDemandChecker()

    for _ in range(24):  # Simulate a day with 24 hours
        action = agent.select_action(station_checker)
        is_terminal, reward = station_checker.check_demand(action)

        if not is_terminal:
            new_state = station_checker
            best_future_value = max(agent.get_q_value(new_state, a) for a in ["High", "Low", "Normal"])
            current_q_value = agent.get_q_value(station_checker, action)
            new_q_value = current_q_value + agent.learning_rate * (reward + agent.discount_factor * best_future_value - current_q_value)
            agent.update_q_value(station_checker, action, new_q_value)

# Interaction Loop
# Interaction Loop
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
    station_checker.update_swaps(swaps_day)  # Update with total swaps for the day
    station_checker.update_slot_empty(slots_empty)

    # Use the learned policy to select an action
    action = agent.select_action(station_checker)

    # Get demand status based on the selected action
    is_terminal, demand_status = station_checker.check_demand(action)

    if is_terminal:
        print(demand_status)
        break
