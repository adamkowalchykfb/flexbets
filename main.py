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


# Load entries from 'entries.json'
entries = load_entries_from_json('entries.json')
db = setup_db()
poolManager = PoolSelectionManager(db)

for entry in entries:
    poolManager.add_entry_to_pool(entry)

#get number of db['entries'] documents
print(f"Total Entries added: {db.entries.count_documents({})}")

#print one entry
print(db.entries.find_one())

# for each entry_size from 2 to 8, get the number of entries
for entry_size in range(2, 9):
    print(f"Number of entries with size {entry_size}: {db.entries.count_documents({'entry_size': entry_size})}")

# get one time_group and its start_time
time_group = db.time_groups.find_one()
print(f"Time group: {time_group}")

time = '2025-10-15 18:00:00'
competitions = start_time_group(db,time)
# print(f"Competitions: {competitions}")

