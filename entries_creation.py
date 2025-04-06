import random
import json
from datetime import datetime

# Constants
NUM_ENTRIES = 500
START_TIME = "2025-10-15 18:15:00"

# Random seed for reproducibility
random.seed(42)

# To store and ensure unique market_value per name_id and market_id combination
market_values = {}

# Helper function to generate a random market value ending in .5
def generate_market_value():
    # Generate a random market value that ends in .5 (e.g., 1.5, 2.5, 3.5, ..., 20.5)
    return random.choice([x + 0.5 for x in range(1, 21)])

# Helper function to generate a random entry, ensuring consistency of market_value for name_id and market_id combinations
def generate_entry():
    # Randomize the size of the entry (80% for 2-5, 20% for 6-8)
    entry_size = random.choices([2, 3, 4, 5], k=1, weights=[0.8, 0.8, 0.8, 0.8])[0] if random.random() < 0.8 else random.choice([6, 7, 8])

    # Create entries
    entries = []
    user_id = random.randint(1, 50)  # Random user_id between 1-50

    for _ in range(entry_size):
        # Randomize name_id (between 1-100)
        name_id = random.randint(1, 100)

        # Randomize market_id (between 1-3)
        market_id = random.randint(1, 3)

        # Check if we've already assigned a market_value for this name_id and market_id combination
        if (name_id, market_id) not in market_values:
            # If not, generate a new market_value and store it
            market_values[(name_id, market_id)] = generate_market_value()

        # Get the consistent market_value for this name_id, market_id combination
        market_value = market_values[(name_id, market_id)]

        # Randomize market_selection with 70% chance of 'Higher' and 30% chance of 'Lower'
        market_selection = random.choices(["Higher", "Lower"], [0.7, 0.3])[0]

        # Create the entry
        entry = {
            "name_id": name_id,
            "market_id": market_id,
            "market_value": market_value,
            "market_selection": market_selection,
            "start_time": START_TIME,
            "user_id": user_id
        }

        entries.append(entry)

    return entries

# Generate 500 entries
data = {"entries": [generate_entry() for _ in range(NUM_ENTRIES)]}

# Write the generated data to a JSON file
with open("entries.json", "w") as f:
    json.dump(data, f, indent=4)

print("Entries generated and written to entries.json.")
