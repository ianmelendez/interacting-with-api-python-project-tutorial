import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
conexion = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = client_id,
                                                              client_secret = client_secret))
# NICO MORENO
artist_id = 'spotify:artist:6fjhNhp9IoeiZpEXq9AT2S'
results = conexion.artist_albums(artist_id, album_type='album')
albums = results['items']
while results['next']:
    results = conexion.next(results)
    albums.extend(results['items'])
for album in albums:
    print(album['name'])
print("-"*60)
results_2 = conexion.artist_top_tracks(artist_id)
for track in results_2['tracks']:
    print('Canción : ' + track['name'])
print("-"*60)
if results:
  # We keep the "tracks" object of the answer
  tracks = results_2["tracks"]
  # We select, for each song, the data we are interested in and discard the rest
  tracks = [{k: (v/(1000*60))%60 if k == "duration_ms" else v for k, v in track.items() if k in ["name", "popularity", "duration_ms"]} for track in tracks]
tracks_df = pd.DataFrame.from_records(tracks)
tracks_df.sort_values(["popularity"], inplace = True)
print(tracks_df.head())