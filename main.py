import json
from pool_selection import PoolSelectionManager
import pymongo
from competition_selection import CompetitionManager

# Function to load entries from a JSON file
def load_entries_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["entries"]

def setup_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    client.drop_database("pool_db")
    db = client["pool_db"]
    db.time_groups.create_index([("start_time", pymongo.ASCENDING)], unique=True)
    return db

def start_time_group(db,time):
    return CompetitionManager(db, time).process_time_banks()


#Step 1, right after new entry is created, add entry to a qeueu
'''
This is done in a seperate service after a user makes a new entry
'''


#Step 2, grab entry at top of queue, add it to the correct pool
'''
This qeueue service will be constanty running
add_entry_to_pool will be connected lambda that is triggered for an entry at the top of the queue
'''
db = setup_db()
poolManager = PoolSelectionManager(db)
# Load entries from 'entries.json'
entries = load_entries_from_json('entries.json')
for entry in entries:
    poolManager.add_entry_to_pool(entry)


#Step 3, at end of time_bank, add entries into their competitions
'''
For the (18:00:00 - 18:30:00] time bank, this will be triggered around 18:31:00, pass in the time to the start_time_group lambda
'''
time = '2025-10-15 18:00:00'
competitions = start_time_group(db,time)



# total entries added
print(f"Total Entries added: {db.entries.count_documents({})}")
for entry_size in range(2, 9):
    print(f"Entry size {entry_size} count: {db.entries.count_documents({'entry_size': entry_size})}")
print()
for pool_name, competitions in competitions.items():
    print(f"{pool_name} n competitions: {len(competitions)}")
    for i, competition in enumerate(competitions):
        print(f"Comp {i + 1} Size: {len(competition['entries'])}")
        print(f"N matches: {competition['match_num']}")
        print()
    print()

# two_entries = competitions['2_entry'][0]["entries"]
# two_entries_matches = competitions['2_entry'][0]["matches"]
# for entry in two_entries:
#     print(entry)
# print()
# print()
# for entry in two_entries_matches:
#     print(entry)

