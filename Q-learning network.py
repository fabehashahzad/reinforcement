import mysql.connector
import numpy as np

# Connect to MySQL database
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "2k24WbAmyOmL!",
    database = "swap_station"
)

# Define the Q-learning parameters
alpha = 0.1  # learning rate
gamma = 0.9  # discount factor
epsilon = 0.1  # exploration-exploitation trade-off
q_table = np.zeros((101, 3))  # Q-table for SOC from 1% to 100%

# Function to select an action based on epsilon-greedy policy
def choose_action(state):
    if np.random.uniform(0, 1) < epsilon:
        return np.random.choice(3)  # explore
    else:
        return np.argmax(q_table[state, :])  # exploit

# Function to update Q-value based on the reward
def update_q_value(state, action, reward, next_state):
    best_next_action = np.argmax(q_table[next_state, :])
    q_table[state, action] = (1 - alpha) * q_table[state, action] + \
                             alpha * (reward + gamma * q_table[next_state, best_next_action])

# Function to retrieve entity_table data from the database
def get_entity_table_data():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM entity_table")
    data = cursor.fetchall()
    cursor.close()
    return data

# Main Q-learning loop
episodes = 1000  # Number of training episodes

for episode in range(episodes):
    # Get initial state (SOC) from the user
    soc = int(input("Enter the SOC (1-100%): "))
    state = soc

    # Retrieve data from the entity_table
    entity_data = get_entity_table_data()

    # Perform Q-learning based on entity_table data (modify as needed)
    for row in entity_data:
        # For simplicity, you can use the data from the entity_table directly
        distance, capacity, cost, charging_rate, energy_efficiency, high_demand = row[1:]

        # Use the retrieved data as needed in your Q-learning process

    # Choose an action based on epsilon-greedy policy
    action = choose_action(state)

    # Determine the destination based on the selected action
    destinations = ['solar farm', 'residential area', 'swapping station']
    destination = destinations[action]
    print(f"The recommended destination is: {destination}")

    # Prompt user for feedback
    feedback = input("Was the decision correct? (yes/no): ").lower()

    # Calculate reward based on user feedback
    if feedback == 'yes':
        reward = 1
    else:
        reward = -1

    # Define charging rate (modify this based on your application)
    charging_rate = 5  # percentage per time step

    # Assume a fixed charging rate 
    next_soc = min(100, soc + charging_rate)  # Cap next SOC at 100%
    next_state = next_soc

    # Update Q-value based on the reward
    update_q_value(state, action, reward, next_state)

# Close the database connection
db.close()
