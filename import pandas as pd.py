import pandas as pd
import numpy as np
import random

# Load the CSV file containing charge level and destinations
data = pd.read_csv('C:\\Users\\ABC\\Downloads\\model.csv')
# Define the Q-table to store Q-values for each state-action pair
states = ['low', 'medium', 'high']
actions = ['SolarFarm', 'ResidentialFarm', 'Station']
num_states = len(states)
num_actions = len(actions)
q_table = pd.DataFrame(np.zeros((num_states, num_actions)), columns=actions)

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Epsilon-greedy policy parameter

# Convert charge levels and destinations to numeric values for indexing
charge_to_index = {
    'low': 0,
    'medium': 1,
    'high': 2
}

# Q-learning algorithm
num_episodes = 1000  # Number of episodes
for episode in range(num_episodes):
    state = random.choice(states)  # Start at a random state
    
    while True:
        # Choose an action based on epsilon-greedy policy
        if np.random.uniform(0, 1) < epsilon:
            action = random.choice(actions)  # Explore: choose a random action
        else:
            next_state_data = data[data['Charge_Level'] == state]
            if not next_state_data.empty:
                action_idx = q_table.columns.get_loc(next_state_data['Destination'].values[0])
                action = actions[action_idx]  # Exploit: choose the action with the highest Q-value for the state
            else:
                action = random.choice(actions)  # Choose a random action if data for the state is missing
        
        # Get the index of the chosen action
        action_index = charge_to_index[state]
        
        # Get the reward (0 for simplicity in this case)
        reward = 0
        
        next_state_data = data[data['Charge_Level'] == state]
        if not next_state_data.empty:
            next_state = next_state_data['Charge_Level'].values[0]
        else:
            next_state = state  # Stay in the same state if data is missing
        
        # Update the Q-value using the Q-learning formula
        next_state_index = charge_to_index[next_state]
        next_max = np.max(q_table.iloc[next_state_index])

        q_table.at[charge_to_index[state], action] += alpha * (reward + gamma * next_max - q_table.at[charge_to_index[state], action])
        
        # Break the loop if the state is 'high' (episode ends)
        if state == 'high':
            break
            
        # Update state to next state
        state = next_state

# Continuously predict destinations based on user input
while True:
    charge_input = input("Enter the charge percentage (0-100) or 'exit' to quit: ")
    
    if charge_input.lower() == 'exit':
        print("Exiting...")
        break
    
    try:
        charge = int(charge_input)
        if 0 <= charge <= 33:
            charge_state = 'low'
        elif 34 <= charge <= 66:
            charge_state = 'medium'
        elif 67 <= charge <= 100:
            charge_state = 'high'
        else:
            print("Charge percentage should be between 0 and 100.")
            continue

        charge_data = data[data['Charge_Level'] == charge_state]
        if not charge_data.empty:
            action_idx = np.argmax(q_table.loc[charge_to_index[charge_state]])
            predicted_destination = actions[action_idx]
            print(f"Predicted destination for charge level {charge_state}: {predicted_destination}")
        else:
            print(f"No data available for charge level {charge_state}.")
    except ValueError:
        print("Invalid input! Please enter a valid charge percentage (0-100) or 'exit' to quit.")
