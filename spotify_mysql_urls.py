import spotipy
import re
import mysql.connector
from multipart import file_path
from spotipy import SpotifyClientCredentials

# Setup spotify API Credentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="8aba661f55374c2992d3345d70a28545", # replace your client ID
    client_secret="567fe781ff2f4ee79fb66562291957a3",# replace with your client secret
))

# MYSQL Database connection

db_config = {
    "host":"localhost", # Change to your MySQL host
    "user":"root",  # Replace with your mysql username
    "password":"root", # Replace with your mysql password
    "database":"da_projects"  # Replace with your database name
}

# Connection to the database

connection = mysql.connector.connect(use_pure=True,**db_config)
cursor = connection.cursor()

# read track URL from file

file_path = "track_urls.txt"

with open(file_path,"r")as file:
    track_urls = file.readlines()

# Process each URL
for track_url in track_urls:
    track_url = track_url.strip() # remove any trailing/Whitespace
    try:
        # Extract track ID Directly from url using regex
        track_id = re.search(r"track/([a-zA-z0-9]+)", track_url).group(1)

        # fetch track data
        track = sp.track(track_id)

        # Extract meta data

        track_data = {
            'Track Name': track["name"],
            'Artist': track['artists'][0]['name'],
            'Album': track['album']['name'],
            'Popularity': track['popularity'],
            'Duration (minutes)': track['duration_ms'] / 60000
        }

        # Insert data into mysql

        insert_query = """
                       insert into spotify_DAnalysis(track_name, artist, album, popularity, duration_minutes)
                       values (%s, %s, %s, %s, %s) 
                       """
        cursor.execute(insert_query, (
            track_data['Track Name'],
            track_data['Artist'],
            track_data['Album'],
            track_data['Popularity'],
            track_data['Duration (minutes)']
        ))

        connection.commit()
        print(f"Inserted {track_data['Track Name']} by {track_data['Artist']}")

    except Exception as e:
        print(f"Error Processing Url:{track_url}, Error : {e}")

# close the connection

cursor.close()
connection.close()

print("All track have been processed and inserted into the database.")

