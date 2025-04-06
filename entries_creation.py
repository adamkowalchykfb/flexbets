import random
import json
from datetime import datetime

# Constants
NUM_ENTRIES = 1000
START_TIME = "2025-10-15 18:15:00"

# Random seed for reproducibility
random.seed(42)

# Helper function to generate a random entry, ensuring consistency of market_value for name_id and market_id combinations
def generate_entry():
    # Randomize the size of the entry (80% for 2-5, 20% for 6-8)
    entry_size = random.choices([2, 3, 4, 5], k=1, weights=[0.8, 0.8, 0.8, 0.8])[0] if random.random() < 0.8 else random.choice([6, 7, 8])
    entry = {}
    entry["id"] = random.randint(1, 100000000000)
    entry["user_id"] = random.randint(1, NUM_ENTRIES // 4)
    # Create entries
    props = []
    for _ in range(entry_size):
        # Randomize name_id (between 1-100)
        name_id = random.randint(1, 100)

        # Randomize market_id (between 1-3)
        market_id = random.randint(1, 3)

        # Randomize market_selection with 70% chance of 'Higher' and 30% chance of 'Lower'
        is_higher = random.choices([True, False], [0.7, 0.3])[0]

        # randomize main_line boolean with 65% chance of True
        main_line = random.choices([True, False], [0.65, 0.35])[0]

        # Create the entry
        prop = {
            "name_id": name_id,
            "market_id": market_id,
            "is_higher": is_higher,
            "start_time": START_TIME,
            "main_line": main_line
        }

        props.append(prop)
    entry["props"] = props

    return entry

# Generate 500 entries
data = {"entries": [generate_entry() for _ in range(NUM_ENTRIES)]}

# Write the generated data to a JSON file
with open("entries.json", "w") as f:
    json.dump(data, f, indent=4)

print("Entries generated and written to entries.json.")
