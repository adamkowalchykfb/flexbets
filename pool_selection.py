import pymongo
from datetime import datetime
import math

class PoolSelectionManager:
    def __init__(self, db):
        """
        Initialize the PoolSelectionManager with a database connection.
        
        :param db: The MongoDB database object.
        """
        self.entry = None
        self.db = db
        self.props = None

    def get_time_group(self):
        """
        Given incoming data containing a list of entries, 
        find the earliest start_time and return the corresponding 30-minute time block.
        """
        
        # Find the earliest start_time
        earliest_prop = min(self.props, key=lambda x: datetime.strptime(x['start_time'], '%Y-%m-%d %H:%M:%S'))
        earliest_start_time = datetime.strptime(earliest_prop['start_time'], '%Y-%m-%d %H:%M:%S')

        # Round down to the nearest 30-minute interval
        minutes = earliest_start_time.minute
        rounded_minutes = math.floor(minutes / 30) * 30  # Get the nearest lower multiple of 30
        rounded_time = earliest_start_time.replace(minute=rounded_minutes, second=0, microsecond=0)

        # return date in string format
        return rounded_time.strftime('%Y-%m-%d %H:%M:%S')

    def get_or_create_time_group(self, time_group_start_time):
        """
        Check if the time group already exists in the collection based on the start_time.
        If it does not exist, create a new time group and return its ID.
        
        :param time_group_start_time: The start time of the time group.
        :return: The ID of the time group.
        """
        # Check if the time group exists
        time_group = self.db.time_groups.find_one({"start_time": time_group_start_time})
        
        if time_group:
            # If the time group exists, return its ID
            return time_group["_id"]
        else:
            # If the time group doesn't exist, create a new time group
            new_time_group = {
                "start_time": time_group_start_time,
            }
            # Insert the new time group into the collection
            result = self.db.time_groups.insert_one(new_time_group)
            
            # Return the ID of the newly created time group
            return result.inserted_id
    
    def insert_entry(self,time_group_id):
        entry_size = len(self.props)

        # Create the entry document
        entry_document = {
            "entry": self.entry,
            "time_group_id": time_group_id,
            "entry_size": entry_size
        }

        # Insert the entry document into the 'entries' collection
        result = self.db.entries.insert_one(entry_document)

        # Return the inserted entry's ID
        return result.inserted_id

    def add_entry_to_pool(self, entry):
        # Step 1: Get the earliest start_time's time group
        self.entry = entry
        self.props = entry['props']
        earliest_time_group = self.get_time_group()

        # Step 2: Get or create the time group document and get its ID
        time_group_id = self.get_or_create_time_group(earliest_time_group)

        self.insert_entry(time_group_id)
