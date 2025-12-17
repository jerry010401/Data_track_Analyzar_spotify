import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re

from spotipy import SpotifyClientCredentials

# set up the client credentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="8aba661f55374c2992d3345d70a28545", # replace your client ID
     client_secret="567fe781ff2f4ee79fb66562291957a3",# replace with your client secret
))

# full track URL (example: wavin' flag coca-cola by K'naan)
track_url = "https://open.spotify.com/track/4nOygULhEuDO5ZBRNPFaso"

# Extract track ID directly from url using regex

track_id = re.search(r"track/([a-zA-z0-9]+)",track_url).group(1)

# fetch track details

track = sp.track(track_id)
print(track)

# Extract meta data

track_data = {
    "Track_Name":track["name"],
    "Artist":track["artists"][0]["name"],
    "Album":track["album"]["name"],
    "Popularity":track["popularity"],
    "Duration(minutes)":track["duration_ms"]/60000
}

# Display meta data
print(f"\nTrack Name: {track_data['Track_Name']}")
print(f"Artist: {track_data['Artist']}")
print(f"Album : {track_data['Album']}")
print(f"Popularity: {track_data['Popularity']}")
print(f"Duration: {track_data['Duration(minutes)']:.2f} minutes")

# convert meta data to DataFrame

df = pd.DataFrame([track_data])
print("\n Data as DataFrame:")
print(df)

# save meta data to csv

df.to_csv("spotify_track_data.csv",index=False)

# Visualize track data
features = ["Popularity","Duration(minutes)"]
values = [track_data["Popularity"],track_data["Duration(minutes)"]]

plt.figure(figsize=(8,5))
plt.bar(features,values,color="skyblue",edgecolor="black")
plt.title(f"Track Meta data for '{track_data['Track_Name']}'")
plt.ylabel("Value")
plt.savefig("bar_track_data.png")
plt.show()