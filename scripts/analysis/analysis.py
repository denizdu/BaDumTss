import os
import json
import requests
from derived_features import process_derived_features
from extra_features import process_extra_features
from freq_and_spectrum import process_freq_and_spectrum
from main_features import process_main_features
from rhythm import process_rhythm
from spectral_features import process_spectral_features

# Dosya adlarını sanitize eden fonksiyon
def sanitize_filename(name):
    return name.replace("/", "_").replace("\\", "_")

# Şarkı indirme fonksiyonu (dummy olarak hazırlanmış, gerçek indirme için API entegrasyonu gerekebilir)
def download_song(song_name, artist_name, download_path):
    # Şarkı ve sanatçı adlarını birleştirip sanitize et
    sanitized_song_name = sanitize_filename(f"{song_name} - {artist_name}")
    file_path = os.path.join(download_path, f"{sanitized_song_name}.mp3")
    
    # Dummy dosya oluştur
    with open(file_path, "w") as f:
        f.write("Dummy audio data for " + sanitized_song_name)
    
    return file_path

# Şarkı analiz et ve ardından sil
def analyze_and_delete_song(song_file):
    try:
        process_main_features(song_file)
        process_derived_features(song_file)
        process_extra_features(song_file)
        process_freq_and_spectrum(song_file)
        process_rhythm(song_file)
        process_spectral_features(song_file)
    finally:
        return
        #if os.path.exists(song_file):
            #os.remove(song_file)

if __name__ == "__main__":
    # Analiz yapmak istediğimiz playlist adı
    playlist_name = input("Enter the playlist name: ")

    # Playlist dosyasını kontrol et
    playlist_file = f"./output/fetch/{playlist_name}_tracks.json"
    download_dir = "./downloads"
    os.makedirs(download_dir, exist_ok=True)

    with open(playlist_file, "r", encoding="utf-8") as f:
        tracks = json.load(f)

    # Playlistteki her şarkıyı tek tek indir, analiz et ve sil
    for track in tracks:
        song_file = download_song(track["name"], track["artist"], download_dir)
        print(f"Processing song: {track['name']} by {track['artist']}")
        analyze_and_delete_song(song_file)

    print(f"Analysis for playlist '{playlist_name}' completed.")
