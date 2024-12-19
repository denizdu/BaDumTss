import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import re

# Spotify API bilgileri
client_id = "73bce3be0fa34320a350e72d2a2cde3b"
client_secret = "318c48fdd78544f587c09363ee29a212"
redirect_uri = "http://localhost:8080"
scope = "playlist-read-private user-library-read"

# Spotify istemcisi
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Dosya adlarını sanitize eden fonksiyon
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Spotify'dan çalma listelerini ve şarkıları al
def get_spotify_tracks():
    playlists = sp.current_user_playlists(limit=50)["items"]
    all_tracks = []
    for playlist in playlists:
        playlist_name = playlist["name"]
        print(f"Processing playlist: {playlist_name}")
        results = sp.playlist_tracks(playlist["id"])["items"]
        for item in results:
            track = item["track"]
            if track:
                all_tracks.append({
                    "name": track["name"],
                    "artist": track["artists"][0]["name"]
                })
    return all_tracks

# Şarkıları kaydet
def save_tracks_to_json(tracks, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(tracks, f, ensure_ascii=False, indent=4)
    print(f"Tracks saved to {file_path}")

if __name__ == "__main__":
    spotify_tracks = get_spotify_tracks()
    save_tracks_to_json(spotify_tracks, "./output/spotify_tracks.json")