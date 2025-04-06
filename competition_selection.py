class CompetitionManager:
    def __init__(self, db, time):
        # Initialize a dictionary of competitions for each pool size
        self.competitions_by_pool = {
            "2_entry": [],
            "3_entry": [],
            "4_entry": [],
            "5_entry": [],
            "6_entry": [],
            "7_entry": [],
            "8_entry": []
        }

        self.db = db
        self.time = time
    # Add entry to competition
    def add_entry_to_comp(self,entry, competition):
        """
        Try to add an entry to a competition, or create a new one if no match is found.
        """
        prop_combo = (entry['name_id'], entry['market_id'], entry['market_value'], entry['market_selection'])
        
        # Check if the entry's unique combination already exists in the competition's unique_props_dict
        if prop_combo not in competition['unique_props_dict']:
            # If not, add the entry to the competition
            competition['entries'].append(entry)
            competition['unique_props_dict'][prop_combo] = entry
            return True
        return False

    # Add to the smallest competition if no match is found
    def add_to_smallest_competition(self,entry, pool_size):
        """
        Adds entry to the smallest competition if no match is found.
        """
        # Find the competition with the least number of entries in the specific pool size
        if self.competitions_by_pool[pool_size]:
            competition = min(self.competitions_by_pool[pool_size], key=lambda x: len(x['entries']))
            competition['entries'].append(entry)
            # print(entry)
            # breakpoint()
            for prop in entry:
                # print(prop)
                # breakpoint()
                key = (prop['name_id'],prop['market_id'], prop['market_value'], prop['market_selection'])
                competition['unique_props_dict'][key] = key

    # Create the required number of competitions based on pool size // 20
    def create_competitions(self,pool_size, pool_name):
        """
        Create the number of competitions based on pool size // 20.
        """
        num_competitions = pool_size // 20
        
        # Create the competitions for this pool
        for i in range(num_competitions):
            new_competition = {'entries': [], 'unique_props_dict': {}, 'match_num': 0, 'matches': []}
            self.competitions_by_pool[pool_name].append(new_competition)

    # Function to find prop match (swapping market_selection)
    def find_prop_match(self,prop):
        """
        Given a prop, find the matching prop by swapping the market_selection.
        """
        match = prop.copy()
        match['market_selection'] = 'Lower' if prop['market_selection'] == 'Higher' else 'Higher'
        return match

    # Add entry to competition by searching for a match
    def add_entry_to_correct_competition(self,entry, pool_size):
        """
        Adds entry to the correct competition by checking for prop matches in the pool.
        """
        # Loop through each prop in the entry
        for prop in entry:
            prop_match = self.find_prop_match(prop)  # Find the matching prop
            
            # Search for the matching prop in all competitions of the same pool
            added_to_comp = False
            for competition in self.competitions_by_pool[pool_size]:
                # Search for the matching prop in the competition's unique_props_dict
                if (prop_match['name_id'], prop_match['market_id'], prop_match['market_value'], prop_match['market_selection']) in competition['unique_props_dict']:
                    # If match found, add the entry to the competition
                    competition['entries'].append(entry)
                    competition['matches'].append(entry)
                    competition['match_num'] += 1
                    added_to_comp = True
                    for prop in entry:
                        key = (prop['name_id'],prop['market_id'], prop['market_value'], prop['market_selection'])
                        competition['unique_props_dict'][key] = key
                    break
            
            if added_to_comp:
                break
            
        # If no match found, add the entry to the smallest competition
        if not added_to_comp:
            self.add_to_smallest_competition(entry, pool_size)

    # Process pools and create competitions based on number of entries
    def process_time_banks(self):
        """
        Iterate over the pools for each time bank, create competitions based on the number of entries.
        """

        # Get the time group ID for the given time
        time_group_id = self.db.time_groups.find_one({"start_time": self.time})["_id"]

        # get all entries with start_time = self.time and group by entry_size
        pools = self.db.entries.aggregate([
            {"$match": {"time_group_id": time_group_id}},
            {"$group": {"_id": "$entry_size", "entries": {"$push": "$$ROOT"}}}
        ])
        print(f"Processing time bank: {self.time}") 

        # Loop through the pools and create competitions
        for pool in pools:
            pool_size = pool['_id']
            pool_entries = pool['entries']
            pool_name = f"{pool_size}_entry"
            
            # Create competitions based on number of entries (divided by 20)
            self.create_competitions(len(pool_entries), pool_name)
            
            # Loop through the entries in the pool and try to add them to competitions
            for entry in pool_entries:
                self.add_entry_to_correct_competition(entry['entry'], pool_name)
            
            # print the number of competitions created for each pool size
            print(f"Created {len(self.competitions_by_pool[pool_name])} competitions for wntry size {pool_size}")
            #  print the number of entries in each competition
            for competition in self.competitions_by_pool[pool_name]:
                print(f"Competition size: {len(competition['entries'])}")
            print()
        return self.competitions_by_pool

        # for pool_name, pool in pools.items():  # Loop 1
        #     pool_size = len(pool)
            
        #     # Create competitions based on number of entries (divided by 20)
        #     self.create_competitions(pool_size, pool_name)
            
        #     # Loop through the entries in the pool and try to add them to competitions
        #     for entry in pool:  # Loop through each entry group in the pool
        #         # Add the entry to its correct competition
        #         self.add_entry_to_correct_competition(entry, pool_name)
