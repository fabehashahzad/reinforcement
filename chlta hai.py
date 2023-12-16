
import numpy as np

# Get unique charging levels and destinations
charging_levels = ['80-90%', '60-80%', '<60%']
destinations = ['Same Station', 'Residential Area', 'Solar Farm']

# Create a Q-table with zeros
q_table = np.zeros((len(charging_levels), len(destinations)))

# Define a function to choose an action based on epsilon-greedy policy
def choose_action(charging_level_idx, epsilon):
    if np.random.rand() < epsilon:
        # Choose a random action
        action_idx = np.random.randint(len(destinations))
    else:
        # Choose the action with the highest Q-value for the current state
        action_idx = np.argmax(q_table[charging_level_idx])
    return action_idx

# Define a function to update the Q-table based on rewards and learning rate
def update_q_table(charging_level_idx, destination_idx, reward, lr, discount_factor):
    q_table[charging_level_idx, destination_idx] += lr * (
        reward + discount_factor * np.max(q_table[charging_level_idx]) - q_table[charging_level_idx, destination_idx]
    )

# Define a function to calculate reward based on conditions
def calculate_reward(charging_level_idx, destination_idx):
    # Assign rewards based on charging levels and destinations
    if charging_level_idx == 0 and destination_idx == 0:  # 80-90% -> Same Station
        return 10
    elif charging_level_idx == 1 and destination_idx == 1:  # 60-80% -> Residential Area
        return 15
    elif charging_level_idx == 2 and destination_idx == 2:  # <60% -> Solar Farm
        return 20
    else:
        return 0  # No reward for other cases

# Continuous loop for user input
while True:
    user_charging_level = input("Enter the charging level (in percentage, e.g., 10 for 10%, 'exit' to quit): ")

    if user_charging_level.lower() == 'exit':
        break  # Exit the loop if the user types 'exit'
    
    try:
        user_charging_level = int(user_charging_level)
        if user_charging_level >= 80:
            predicted_destination = 'Same Station'
        elif user_charging_level >= 60:
            predicted_destination = 'Residential Area'
        else:
            predicted_destination = 'Solar Farm'
        print(f"For charging level {user_charging_level}%, predicted destination: {predicted_destination}")
    except ValueError:
        print("Invalid input. Please enter a valid charging level.")