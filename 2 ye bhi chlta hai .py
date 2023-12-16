import numpy as np

class ChargingEnvironment:
    def __init__(self, initial_charging_level):
        self.observation_space = 100  # Charging level from 0 to 100
        self.action_space = 3  # Charging station, residential area, solar farm
        self.state = initial_charging_level

        # Define target locations
        self.target_locations = {
            0: ((80, 90), "charging_station"),
            1: ((50, 79), "residential_area"),
            2: ((0, 49), "solar_farm"),
        }

    def reset(self):
        self.state = np.random.randint(0, 101)
        return self.state

    def step(self, action):
        charging_range, destination = self.target_locations[action]

        reward = 1.0 if charging_range[0] <= self.state <= charging_range[1] else 0.0

        self.state = np.random.randint(max(0, self.state - 5), min(100, self.state + 5))

        return self.state, reward, False, destination


class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=0.5, target_locations=None):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.q_table = np.zeros((100, 3))
        self.target_locations = target_locations  # Store target_locations

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(3)
        else:
            state = state % self.q_table.shape[0]
            return np.argmax(self.q_table[state, :])

    def update_q_table(self, state, action, reward, next_state):
        state = state % self.q_table.shape[0]
        next_state = next_state % self.q_table.shape[0]

        best_next_action = np.argmax(self.q_table[next_state, :])
        self.q_table[state, action] += self.alpha * (reward + self.gamma * self.q_table[next_state, best_next_action] - self.q_table[state, action])

    def predict_destination(self, charge_level):
        charge_level = int(charge_level) % self.q_table.shape[0]
        return np.argmax(self.q_table[charge_level, :])


# Randomly set initial charging level within the environment
initial_charging_level = np.random.randint(0, 101)
env = ChargingEnvironment(initial_charging_level)
agent = QLearningAgent(target_locations=env.target_locations)

# Training the agent
for episode in range(1000):
    state = env.reset()
    total_reward = 0

    for _ in range(100):
        action = agent.choose_action(state)
        next_state, reward, done, destination = env.step(action)

        agent.update_q_table(state, action, reward, next_state)

        total_reward += reward
        state = next_state

        if done:
            command = " ".join(destination.lower().split("_"))
            print(f"Episode: {episode}, Command: {command}, Charge Level: {state}, Total Reward: {total_reward}")
            break

# Predict the destination based on charge level
while True:
    test_charge_level = float(input("Enter the charge level for prediction (0-100) or 'q' to quit: "))
    
    if not test_charge_level:
        break
    
    try:
        test_charge_level_float = float(test_charge_level)
        if 0 <= test_charge_level_float <= 100:
            predicted_destination = agent.predict_destination(test_charge_level_float)
            predicted_command = " ".join(env.target_locations[predicted_destination][1].lower().split("_"))
            print(f"Predicted Command: {predicted_command}")
        else:
            print("Please enter a valid charge level between 0 and 100.")
    except ValueError:
        print("Please enter a valid number or 'q' to quit.")