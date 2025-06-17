import json
from pool_selection import PoolSelectionManager
import pymongo
from competition_selection import CompetitionManager
from entries_creation import generate_entries
from db_creation import post_stats, setup_mongo_db

GAME_TYPE = 'team_props'  # or 'team_props'

# Function to load entries from a JSON file
def load_entries_from_json(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data["entries"]


#Generates N random entries for testing purposes
#In normal app flow, entries are generated on users request
generate_entries(GAME_TYPE)
entries = load_entries_from_json('entries.json')

#Setting up MongoDB connection
db = setup_mongo_db()


# This adds each entry into their correct pool
# In normal app flow, after an entry is created by a user, json information is passed to add_entry_to_pool
# Entries are added to the pool based on their start_time
poolManager = PoolSelectionManager(db)
for entry in entries:
    poolManager.add_entry_to_pool(entry)


#At end of time_bank, all entries within the time bank will be added to their competitions
#For the (18:00:00 - 18:30:00] time bank, process_time_bank will be triggered shortly after 18:30:00
time = '2025-10-15 18:00:00'
competitions =  CompetitionManager(db, time, GAME_TYPE).process_time_bank()

# At this point, all entries have been added to their respective competitions
# The competition_id is updated in the entries SQL table

# outputs post stats of competitions to txt file
post_stats(competitions, GAME_TYPE)


#TODO
# 1. Create endpoint for PoolSelectionManager which will accept entry json and add it to the pool
# 2. Create endpoint for CompetitionManager which will accept time and process the competitions
# 3. Create Event Scheduler to trigger process_time_bank at the end of each time bank
# 4. Test the entire flow with real-time data

