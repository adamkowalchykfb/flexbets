#Step 1, right after new entry is created, add entry to a qeueu

#Step 2, grab entry at top of queue, add it to the correct pool
'''
get start_time of earliest prop in entry
add the entry to the n_picks pool in that time bank, 6 pick entry at 6:05 would go in the 6:00 - 6:30 6_pick pool
'''

#Step 3, at beginning of time_bank, so for a [6:00 - 7:30) time bank add entries into their competitions
'''
for each pool in time bank (should be 7 total, start with 2)
    create n competitons based on number of entries, modulo 20
    for each entry in pool //loop 1
        comp_number = add_entry_to_comp()
        
'''

'''
fun add_entry_to_comp:
    create list prop_matches, swapping the props 'lower' with 'higher' and vice versa
    for each prop in prop_matches, search for a match in a competition: //loop 2
        for comp in competions: //loop 3
            if prop in unique_props_dict:
                add entry to competition
                exit loop 2
    if no match found:
        add entry to smallest competition
    return comp_number
'''

{"Lebron James","Points","20.5","Higher"}




