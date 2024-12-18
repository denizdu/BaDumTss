import base64
import spotipy
import json
import re
import random
import time
import logging

from spotipy.oauth2 import SpotifyOAuth
from spotipy.exceptions import SpotifyException


logging.basicConfig(level=logging.DEBUG)

# Define the scope of the required permissions
SCOPE = "playlist-read-private user-library-read user-top-read user-read-playback-position"
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
    try:
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
    except SpotifyException as e:
        print(f"Error retrieving playlists: {e}")
    return playlists

# Function to get songs from a specific playlist
def get_playlist_tracks(playlist_id):
    tracks = []
    try:
        results = sp.playlist_tracks(playlist_id)
        while results:
            for item in results['items']:
                track = item['track']
                if track and track['id']:  # Check if track and track ID are valid
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
    except SpotifyException as e:
        print(f"Error retrieving tracks for playlist {playlist_id}: {e}")
    return tracks

# Function to get audio features for tracks
def get_audio_features(track_ids):
    audio_features = []
    for i in range(0, len(track_ids), 100):  # API supports up to 100 track IDs per call
        try:
            response = sp.audio_features(track_ids[i:i + 100])
            if response:
                audio_features.extend([feature for feature in response if feature])
            time.sleep(1)  # Wait for 1 second between calls
        except SpotifyException as e:
            print(f"Error retrieving audio features: {e}")
            audio_features.extend([None] * len(track_ids[i:i + 100]))
    return audio_features

def get_audio_features_with_retry(track_ids):
    audio_features = []
    for i in range(0, len(track_ids), 100):
        retry_count = 0
        while retry_count < 3:
            try:
                response = sp.audio_features(track_ids[i:i + 100])
                if response:
                    audio_features.extend([feature for feature in response if feature])
                time.sleep(1)  # Wait for 1 second between calls
                break
            except SpotifyException as e:
                if e.http_status == 429:  # Too Many Requests
                    retry_after = int(e.headers.get("Retry-After", 5))
                    print(f"Rate limited. Retrying after {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    print(f"Error retrieving audio features: {e}")
                    audio_features.extend([None] * len(track_ids[i:i + 100]))
                    break
            retry_count += 1
    return audio_features

# Function to save tracks to a local file
def save_tracks_to_file(tracks, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)

# Sanitize file names for saving
def sanitize_filename(filename):
    return re.sub(r'[<>:"/\\|?*]', '_', filename)

# Load and process playlists
playlists = get_playlists()
if not playlists:
    print("No playlists found. Check your Spotify account and permissions.")
else:
    for playlist in playlists:
        playlist_id = playlist['id']
        playlist_name = playlist['name']
        print(f"Processing playlist: {playlist_name}")

        # Get tracks from the playlist
        tracks = get_playlist_tracks(playlist_id)
        track_ids = [track['track_id'] for track in tracks if track['track_id'] is not None]

        # Get audio features
        print("Track IDs:", track_ids)
        sample_track_ids = ["6cnczA8kq5z7hGmwLeRQYI", "1RnpgW5yFMvk3BLygSYZHc"]
        response = sp.audio_features(sample_track_ids)
        print(response)
        audio_features = get_audio_features_with_retry(track_ids)

        # Add audio features to tracks
        for i, track in enumerate(tracks):
            if i < len(audio_features) and audio_features[i]:
                track.update(audio_features[i])
            else:
                # Add default values for missing audio features
                track.update({
                    'tempo': random.uniform(60, 180),
                    'energy': random.uniform(0, 1),
                    'danceability': random.uniform(0, 1),
                })

        # Save the processed tracks to a file
        sanitized_name = sanitize_filename(playlist_name)
        file_path = f"C:/Users/denizdu/OneDrive/Masaüstü/BaDumTss/export/{sanitized_name}_tracks.json"
        save_tracks_to_file(tracks, file_path)
        print(f"Tracks for playlist '{playlist_name}' have been saved to {file_path}.")
