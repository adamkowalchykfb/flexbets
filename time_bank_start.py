from competition_selection import CompetitionManager
from pool_selection import PoolSelectionManager
import json


# Function to load entries from a JSON file
def load_entries_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["entries"]

# Load entries from 'entries.json'
entries = load_entries_from_json('entries.json')

poolManager = PoolSelectionManager()

for entry in entries:
    poolManager.add_entry_to_pool(entry)

# Output the categorized pools (for testing)
print("Pools:")
for pool_name, pool_entries in pools.items():
    print(f"\n{pool_name}: {len(pool_entries)}")

comp_manager = CompetitionManager()

# Run the process on pools
comp_manager.process_time_banks(pools)

for pool_name, competitions in comp_manager.competitions_by_pool.items():
    print(pool_name)
    for competition in competitions:
        print(f"Size: {len(competition['entries'])}")
        print(f"N matches: {competition['match_num']}")
        print()

two_entries = comp_manager.competitions_by_pool['2_entry'][0]["entries"]
two_entries_matches = comp_manager.competitions_by_pool['2_entry'][0]["matches"]
for entry in two_entries:
    print(entry)
print()
print()
for entry in two_entries_matches:
    print(entry)