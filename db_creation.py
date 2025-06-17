import psycopg2
import pymongo

def get_postgres_connection():
    conn = psycopg2.connect(
        dbname="db",
        user="adamk",
        password="1234",
        host="localhost"
    )
    return conn 

def setup_mongo_db():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    client.drop_database("pool_db")
    db = client["pool_db"]
    db.time_groups.create_index([
        ("start_time", pymongo.ASCENDING),
        ("game_type", pymongo.ASCENDING)
    ], unique=True)
    return db

def get_mongo_connection():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["pool_db"]
    return db

def create_tables():
    con = get_postgres_connection()
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS entries;")
    cur.execute("DROP TABLE IF EXISTS competitions;")

    cur.execute(
        "CREATE TABLE competitions (" \
        "competition_id SERIAL PRIMARY KEY" \
        ");" 
    )
    cur.execute(
        "CREATE TABLE entries (" \
        "entry_id SERIAL PRIMARY KEY, " \
        "competition_id INT," \
        "FOREIGN KEY (competition_id) REFERENCES competitions(competition_id)" \
        ");"
    )
    con.commit()
    con.close()


def post_stats(competitions,game_type, filename="stats_output.txt"):
    mongo_db = get_mongo_connection()
    if game_type == 'prop_picks':
        entry_sizes = range(2, 9)
    else:  # team_props
        entry_sizes = range(13, 20)
    
    with open(filename, 'w') as file:
        file.write(f"Total Entries added: {mongo_db.entries.count_documents({})}\n\n")
        
        for entry_size in entry_sizes:
            count = mongo_db.entries.count_documents({'entry_size': entry_size})
            file.write(f"Entry size {entry_size} count: {count}\n")
        file.write("\n")

        for pool_name, comps in competitions.items():
            file.write(f"{pool_name} n competitions: {len(comps)}\n")
            for i, competition in enumerate(comps):
                file.write(f"Comp {i + 1} Size: {len(competition['entries'])}\n")
                file.write(f"N matches: {competition['match_num']}\n\n")
            file.write("\n")

        if game_type == 'prop_picks':  
            smallest_size = 2
        else:  # team_props
            smallest_size = 13
        # print all entries in pool_size 2_props in the first competition
        first_comp = competitions[f'{smallest_size}_props'][0]
        file.write(f"Entries in {smallest_size}_props Comp 1:\n")
        for entry in first_comp['entries']:
            file.write(f"{entry}\n")

