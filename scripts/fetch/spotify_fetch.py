import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
import re
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Spotify API bilgileri
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
scope = "playlist-read-private user-library-read"

# Dizinler
DIR_OUTPUT_FETCH = os.getenv("DIR_OUTPUT_FETCH")

# Spotify istemcisi
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Dosya adlarını sanitize eden fonksiyon
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
    sanitized = re.sub(r'_+', '_', sanitized)  # Birden fazla alt çizgiyi tek bir alt çizgiye indir
    sanitized = sanitized.strip('_')  # Baştaki ve sondaki alt çizgileri kaldır
    return sanitized

# Çalma listesi adlarını ve ID'lerini çek
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
    save_to_json(playlists, os.path.join(DIR_OUTPUT_FETCH, "playlists.json"))

    # Her çalma listesi için şarkıları ayrı dosyalara kaydet
    for playlist in playlists:
        playlist_name = playlist["sanitized_name"]
        tracks = get_tracks_from_playlist(playlist["id"])
        save_to_json(tracks, os.path.join(DIR_OUTPUT_FETCH, f"{playlist_name}_tracks.json"))
