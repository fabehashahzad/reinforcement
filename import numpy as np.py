import numpy as np

# Get unique destinations and charge level ranges
destinations = ['Same Station', 'Residential Area', 'Solar Farm']
charge_levels = ['80-90%', '60-80%', '<60%']

# Create Q-tables for destinations and charge levels with zeros
q_table_destinations = np.zeros((len(charge_levels), len(destinations)))

# Define a function to convert user input to a charge level index
def convert_to_charge_level_index(charge_input):
    charge_input = charge_input.strip().lower()
    if charge_input.endswith('%'):
        charge_input = charge_input[:-1]  # Remove the '%' character
    try:
        charge = float(charge_input)
        if charge >= 80:
            return 0  # 80-90%
        elif 60 <= charge < 80:
            return 1  # 60-80%
        else:
            return 2  # <60%
    except ValueError:
        return -1  # Invalid input

# Define a function to choose an action based on epsilon-greedy policy
def choose_action(charge_level_idx, epsilon):
    if np.random.rand() < epsilon:
        # Choose a random action
        action_idx = np.random.randint(len(q_table_destinations[charge_level_idx]))
    else:
        # Choose the action with the highest Q-value for the current state
        action_idx = np.argmax(q_table_destinations[charge_level_idx])
    return action_idx

2# Define a function to update the Q-table based on rewards and learning rate
def update_q_table(charge_level_idx, action_idx, reward, lr, discount_factor):
    q_table_destinations[charge_level_idx, action_idx] += lr * (
        reward + discount_factor * np.max(q_table_destinations[charge_level_idx]) - q_table_destinations[charge_level_idx, action_idx]
    )

# Define a function to calculate reward based on charge levels and predicted destinations
def calculate_reward(charge_level_idx, action_idx):
    if action_idx == charge_level_idx:
        return 10  # Correct prediction reward
    else:
        return -1  # Incorrect prediction penalty

# Continuous loop for user input
while True:
    user_input = input("Enter the charge level (percentage or a number, 'exit' to quit): ")

    if user_input.lower() == 'exit':
        break  # Exit the loop if the user types 'exit'
    
    charge_level_idx = convert_to_charge_level_index(user_input)
    
    if charge_level_idx != -1:
        epsilon = 0.1  # Epsilon for epsilon-greedy policy
        
        # Choose action for destinations based on charge level
        action_index = choose_action(charge_level_idx, epsilon)
        predicted_destination = destinations[action_index]
        
        # Calculate reward based on charge level and predicted destination
        reward = calculate_reward(charge_level_idx, action_index)
        update_q_table(charge_level_idx, action_index, reward, lr=0.1, discount_factor=0.9)
        
        print(f"For charge level {charge_levels[charge_level_idx]}, predicted destination: {predicted_destination}")
    else:
        print("Invalid input. Please enter a valid charge level or 'exit'.")
