import numpy as np

class ChargingEnvironment:
    def __init__(self, initial_charging_level):
        self.observation_space = 100  # Charging level from 0 to 100
        self.action_space = 3  # Charging station, residential area, solar farm
        self.state = initial_charging_level

    def reset(self):
        self.state = np.random.randint(0, 101)
        return self.state

    def step(self, action):
        # Define the reward based on the action and current state
        target_locations = {
            0: ((80, 90), "charging_station"),
            1: ((50, 79), "residential_area"),
            2: ((0, 49), "solar_farm"),
        }

        charging_range, destination = target_locations[action]

        # Calculate the reward
        reward = 1.0 if charging_range[0] <= self.state <= charging_range[1] else 0.0

        # Update the state (charging level)
        self.state = np.random.randint(max(0, self.state - 5), min(100, self.state + 5))

        return self.state, reward, False, destination  # Return the destination as part of the environment state


# Q-learning agent
class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.99, epsilon=0.1):
        self.alpha = alpha  # Learning rate
        self.gamma = gamma  # Discount factor
        self.epsilon = epsilon  # Exploration-exploitation trade-off
        self.q_table = np.zeros((100, 3))  # Q-table for 100 charging levels and 3 actions

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(3)  # Exploration
        else:
            # Use modulo to ensure the state is within the valid range
            state = state % self.q_table.shape[0]
            return np.argmax(self.q_table[state, :])  # Exploitation

    def update_q_table(self, state, action, reward, next_state):
        # Use modulo to ensure the state and next_state are within the valid range
        state = state % self.q_table.shape[0]
        next_state = next_state % self.q_table.shape[0]

        best_next_action = np.argmax(self.q_table[next_state, :])
        self.q_table[state, action] += self.alpha * (reward + self.gamma * self.q_table[next_state, best_next_action] - self.q_table[state, action])

# Take user input for initial charging level
initial_charging_level = float(input("Enter the initial charging level (0-100): "))

# Initialize environment with user-provided initial charging level
env = ChargingEnvironment(initial_charging_level)
agent = QLearningAgent()

# Training the agent
for episode in range(100):
    state = env.reset()
    total_reward = 0

    for _ in range(100):  # Limiting the episode length to 100 steps
        action = agent.choose_action(state)
        next_state, reward, done, destination = env.step(action)  # Extract the destination

        agent.update_q_table(state, action, reward, next_state)

        total_reward += reward
        state = next_state

        if done:
            command = " ".join(destination.lower().split("_"))  # Format command from "charging_station" to "charging station"
            print(f"Episode: {episode}, Command: {command}, Charge Level: {state}, Total Reward: {total_reward}")
            break

# Testing the trained agent
test_state = env.reset()
test_total_reward = 0

for _ in range(10):
    test_action = np.argmax(agent.q_table[test_state, :])
    test_next_state, test_reward, test_done, test_destination = env.step(test_action)  # Extract the destination

    test_total_reward += test_reward
    test_state = test_next_state

    if test_done:
        test_command = " ".join(test_destination.lower().split("_"))  # Format command from "charging_station" to "charging station"
        print(f"Test Command: {test_command}, Test Charge Level: {test_state}, Test Total Reward: {test_total_reward}")
        break
