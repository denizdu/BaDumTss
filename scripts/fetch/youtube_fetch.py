import os
import json
from pytube import Search, YouTube
from dotenv import load_dotenv
import os

# .env dosyasını yükle
load_dotenv()

#client_id = os.getenv("CLIENT_ID")
#client_secret = os.getenv("CLIENT_SECRET")
#redirect_uri = os.getenv("REDIRECT_URI")

# Dosya adlarını sanitize eden fonksiyon
def sanitize_filename(name):
    return name.replace("/", "_").replace("\\", "_").replace(":", "_").replace("*", "_").replace("?", "_").replace("\"", "_").replace("<", "_").replace(">", "_").replace("|", "_")

# Şarkı indirici
def download_song(song_name, artist_name, download_path):
    search_query = f"{song_name} {artist_name}"
    print(f"Searching for: {search_query}")
    search = Search(search_query)
    try:
        youtube_url = search.results[0].watch_url
        print(f"Found: {youtube_url}")
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(only_audio=True).first()
        sanitized_song_name = sanitize_filename(f"{song_name} - {artist_name}")
        file_path = os.path.join(download_path, f"{sanitized_song_name}.mp3")
        stream.download(output_path=download_path, filename=f"{sanitized_song_name}.mp3")
        print(f"Downloaded: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to download {song_name} by {artist_name}: {e}")
        return None

if __name__ == "__main__":
    # Playlist adı ve dosya yolu
    playlist_name = input("Enter the playlist name: ")
    playlist_file = f"./output/fetch/{playlist_name}_tracks.json"
    download_dir = f"./downloads/{playlist_name}"
    os.makedirs(download_dir, exist_ok=True)

    # Playlist şarkılarını yükle
    with open(playlist_file, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    # Her şarkıyı indir
    for track in tracks:
        song_name = track["name"]
        artist_name = track["artist"]
        download_song(song_name, artist_name, download_dir)
