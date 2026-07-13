import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

# Spotify API credentials.
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
scope = "playlist-read-private user-library-read"

# Directories.
DIR_OUTPUT_FETCH = os.getenv("DIR_OUTPUT_FETCH")

# Spotify client.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Sanitize file names.
def sanitize_filename(name):
    translation_table = str.maketrans({
        ' ': '_',
        'ı': 'i',
        'İ': 'I',
        'ş': 's',
        'Ş': 'S',
        'ğ': 'g',
        'Ğ': 'G',
        'ö': 'o',
        'Ö': 'O',
        'ü': 'u',
        'Ü': 'U',
        'ç': 'c',
        'Ç': 'C',
        '|': '',
        ',': '',
        '.': '',
        "'": ''
    })
    sanitized = name.translate(translation_table)
    sanitized = re.sub(r'_+', '_', sanitized)  # Collapse consecutive underscores.
    sanitized = sanitized.strip('_')  # Remove leading and trailing underscores.
    return sanitized

# Fetch playlist names and IDs.
def get_playlists():
    playlists = sp.current_user_playlists(limit=50)["items"]
    playlist_data = []
    for playlist in playlists:
        original_name = playlist["name"]
        sanitized_name = sanitize_filename(original_name)
        playlist_data.append({
            "original_name": original_name,
            "sanitized_name": sanitized_name,
            "id": playlist["id"]
        })
    return playlist_data

# Fetch tracks from a specific playlist.
def get_tracks_from_playlist(playlist_id):
    results = sp.playlist_tracks(playlist_id)["items"]
    tracks = []
    for item in results:
        track = item["track"]
        if track:
            tracks.append({
                "name": track["name"],
                "artist": track["artists"][0]["name"]
            })
    return tracks

# Save data as JSON.
def save_to_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    # Fetch and save playlists.
    playlists = get_playlists()
    save_to_json(playlists, os.path.join(DIR_OUTPUT_FETCH, "playlists.json"))

    # Save each playlist's tracks to a separate file.
    for playlist in playlists:
        playlist_name = playlist["sanitized_name"]
        tracks = get_tracks_from_playlist(playlist["id"])
        save_to_json(tracks, os.path.join(DIR_OUTPUT_FETCH, f"{playlist_name}_tracks.json"))
