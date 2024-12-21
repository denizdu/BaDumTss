import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import re
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Spotify API bilgileri
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
scope = "playlist-read-private user-library-read"

# Spotify istemcisi
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Dosya adlarını sanitize eden fonksiyon
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name)

# Çalma listesi adlarını ve ID'lerini çek
def get_playlists():
    playlists = sp.current_user_playlists(limit=50)["items"]
    playlist_data = []
    for playlist in playlists:
        playlist_data.append({
            "name": playlist["name"],
            "id": playlist["id"]
        })
    return playlist_data

# Belirli bir çalma listesindeki şarkıları çek
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

# Veriyi JSON olarak kaydet
def save_to_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_path}")

if __name__ == "__main__":
    # Çalma listelerini çek ve kaydet
    playlists = get_playlists()
    save_to_json(playlists, "./output/fetch/playlists.json")

    # Her çalma listesi için şarkıları ayrı dosyalara kaydet
    for playlist in playlists:
        playlist_name = sanitize_filename(playlist["name"])
        tracks = get_tracks_from_playlist(playlist["id"])
        save_to_json(tracks, f"./output/fetch/{playlist_name}_tracks.json")
