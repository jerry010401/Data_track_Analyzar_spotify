import re
import spotipy
from spotipy import SpotifyClientCredentials
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Setup Spotify API Credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="8aba661f55374c2992d3345d70a28545",
    client_secret="567fe781ff2f4ee79fb66562291957a3",
))

# MySQL Database connection
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "root",
    "database": "da_projects"
}

connection = mysql.connector.connect(use_pure=True, **db_config)
cursor = connection.cursor()

track_url = "https://open.spotify.com/track/4nOygULhEuDO5ZBRNPFaso"
track_id = re.search(r"track/([a-zA-Z0-9]+)", track_url).group(1)

track = sp.track(track_id)

track_data = {
    'Track Name': track["name"],
    'Artist': track['artists'][0]['name'],    # ✔ Correct
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration (minutes)': track['duration_ms'] / 60000
}

insert_query = """
INSERT INTO spotify_DAnalysis(track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration (minutes)']
))

connection.commit()

print(f"Track '{track_data['Track Name']}' by '{track_data['Artist']}' inserted!")

cursor.close()
connection.close()

