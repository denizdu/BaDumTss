import base64
import spotipy
import json
import re
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# Define the scope of the required permissions
SCOPE = "playlist-read-private user-library-read user-top-read"

# Define your client ID, client secret, and redirect URI
client_id = "73bce3be0fa34320a350e72d2a2cde3b"
client_secret = "318c48fdd78544f587c09363ee29a212"
redirect_uri = "http://localhost:8080"

# Initialize the Spotify client with the OAuth manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=SCOPE))

# Function to retrieve playlists
def get_playlists():
    playlists = []
    results = sp.current_user_playlists(limit=50)
    while results:
        for playlist in results['items']:
            playlists.append({
                'name': playlist['name'],
                'id': playlist['id'],
                'owner': playlist['owner']['display_name'],
                'tracks': playlist['tracks']['total']
            })
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return playlists

# Function to save playlists to a local file
def save_playlists_to_file(playlists, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(playlists, f, ensure_ascii=False, indent=4)

# Get playlists
playlists = get_playlists()

# Define the path to save the playlists
file_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/export/denizdu_playlists.json"

# Save playlists to a local file
save_playlists_to_file(playlists, file_path)
print(f"Playlists have been successfully saved to {file_path}.")

# Function to get songs from a specific playlist
def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    while results:
        for item in results['items']:
            track = item['track']
            if track:  # Check if track is not None
                tracks.append({
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'album': track['album']['name'],
                    'duration_ms': track['duration_ms'],
                    'track_id': track['id']
                })
        if results['next']:
            results = sp.next(results)
        else:
            results = None
    return tracks

# Function to save tracks to a local file
def save_tracks_to_file(tracks, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)

# Function to sanitize file names
def sanitize_filename(filename):
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', filename)
    return sanitized

# Load the playlists JSON file
playlists_file_path = "C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/export/denizdu_playlists.json"
with open(playlists_file_path, 'r', encoding='utf-8') as f:
    playlists = json.load(f)

# Iterate over each playlist and export the tracks
for playlist in playlists:
    playlist_id = playlist['id']
    playlist_name = playlist['name']
    print(f"Processing playlist: {playlist_name}")

    # Get tracks from the playlist
    tracks = get_playlist_tracks(playlist_id)

    # Sanitize the playlist name for use in the file path
    sanitized_playlist_name = sanitize_filename(playlist_name)

    # Define the file path for the playlist's tracks
    playlist_tracks_file_path = f"C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/export/{sanitized_playlist_name}_tracks.json"

    # Save tracks to a local file
    save_tracks_to_file(tracks, playlist_tracks_file_path)

    print(f"Tracks for playlist '{playlist_name}' have been successfully saved to {playlist_tracks_file_path}.")

print("All playlists have been processed.")
