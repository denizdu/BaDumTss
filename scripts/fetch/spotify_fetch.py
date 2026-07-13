import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import re
from dotenv import load_dotenv

# Load environment variables.
load_dotenv()

SPOTIFY_SCOPE = "playlist-read-private user-library-read"

# Directories.
DIR_OUTPUT_FETCH = os.getenv("DIR_OUTPUT_FETCH")


def create_spotify_client(client_id=None, client_secret=None, redirect_uri=None):
    """Create a Spotify client only when an authenticated operation is requested."""
    credentials = {
        "SPOTIFY_CLIENT_ID": client_id or os.getenv("SPOTIFY_CLIENT_ID"),
        "SPOTIFY_CLIENT_SECRET": client_secret or os.getenv("SPOTIFY_CLIENT_SECRET"),
        "REDIRECT_URI": redirect_uri or os.getenv("REDIRECT_URI"),
    }
    missing = [name for name, value in credentials.items() if not value]
    if missing:
        raise RuntimeError(
            "Missing Spotify configuration: " + ", ".join(sorted(missing))
        )

    auth_manager = SpotifyOAuth(
        client_id=credentials["SPOTIFY_CLIENT_ID"],
        client_secret=credentials["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=credentials["REDIRECT_URI"],
        scope=SPOTIFY_SCOPE,
    )
    return spotipy.Spotify(auth_manager=auth_manager)

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
def get_playlists(spotify_client):
    playlists = spotify_client.current_user_playlists(limit=50)["items"]
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
def get_tracks_from_playlist(spotify_client, playlist_id):
    results = spotify_client.playlist_tracks(playlist_id)["items"]
    tracks = []
    for item in results:
        track = item["track"]
        if track:
            artist = track["artists"][0]["name"]
            tracks.append({
                "name": track["name"],
                "artist": artist,
                "metadata_source": "spotify",
                "audio_source": "youtube",
                "audio_reference": f"{track['name']} {artist}",
            })
    return tracks

# Save data as JSON.
def save_to_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    if not DIR_OUTPUT_FETCH:
        raise RuntimeError("DIR_OUTPUT_FETCH must be configured")

    spotify_client = create_spotify_client()

    # Fetch and save playlists.
    playlists = get_playlists(spotify_client)
    save_to_json(playlists, os.path.join(DIR_OUTPUT_FETCH, "playlists.json"))

    # Save each playlist's tracks to a separate file.
    for playlist in playlists:
        playlist_name = playlist["sanitized_name"]
        tracks = get_tracks_from_playlist(spotify_client, playlist["id"])
        save_to_json(tracks, os.path.join(DIR_OUTPUT_FETCH, f"{playlist_name}_tracks.json"))
