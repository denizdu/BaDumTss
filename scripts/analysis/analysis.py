import sys
import os
import logging
import json
from multiprocessing import Pool
from dotenv import load_dotenv
from scripts.fetch.youtube_fetch import download_song_as_wav
from derived_features import process_derived_features
from extra_features import process_extra_features
from freq_and_spectrum import process_freq_and_spectrum
from main_features import process_main_features
from rhythm import process_rhythm
from spectral_features import process_spectral_features
from drum_analysis import process_drum_analysis

# .env dosyasını yükle
load_dotenv(dotenv_path="C://Users//denizdu//OneDrive//Masaüstü//BaDumTss//.env")

# Dizinler
DIR_DOWNLOAD = os.getenv("DIR_DOWNLOAD")
DIR_OUTPUT_FETCH = os.getenv("DIR_OUTPUT_FETCH")
PLAYLIST_TOBE_ANALYZED = os.getenv("PLAYLIST_TOBE_ANALYZED")
DIR_OUTPUT_ANALYSIS = os.getenv("DIR_OUTPUT_ANALYSIS")

# Sonuç dosyası yolu
output_file = os.path.join(DIR_OUTPUT_ANALYSIS, "analysis_output.json")

# Log dosyası oluştur
logging.basicConfig(filename="errors.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

# Analiz dosyasının bulunduğu dizini oluştur
os.makedirs(DIR_OUTPUT_ANALYSIS, exist_ok=True)

# Playlist adlarını parse et
playlists_to_analyze = [p.strip() for p in PLAYLIST_TOBE_ANALYZED.split(",")]

# Şarkı analiz et ve ardından sil
def analyze_and_delete_song(song_file):
    try:
        print(f"Analyzing: {song_file}")
        process_main_features(song_file, output_file)
        process_freq_and_spectrum(song_file, output_file)
        process_rhythm(song_file, output_file)
        process_spectral_features(song_file, output_file)
        process_extra_features(song_file, output_file)
        process_drum_analysis(song_file, output_file)

        print(f"Analysis completed for: {song_file}")
    except Exception as e:
        logging.error(f"Error during analysis of {song_file}: {e}")
    finally:
        if os.path.exists(song_file):
            os.remove(song_file)
            print(f"Deleted: {song_file}")

def process_track(track):
    search_query = f"{track['name']} {track['artist']}"
    print(f"Processing song: {track['name']} by {track['artist']}")

    # Şarkıyı indirirken YouTube çerezlerini kullan
    print(f"Attempting to download: {search_query}")
    song_file = download_song_as_wav(search_query, DIR_DOWNLOAD, browser="edge", profile="Default")
    print(f"Download result: {song_file}")

    # Şarkı indirildiyse analiz et ve sil
    if song_file and os.path.exists(song_file):
        analyze_and_delete_song(song_file)
    else:
        print(f"Failed to process {search_query}. Skipping.")
        logging.error(f"Failed to download or process {search_query}")

if __name__ == "__main__":
    os.makedirs(DIR_DOWNLOAD, exist_ok=True)  # İndirme dizinini oluştur
    for playlist_name in playlists_to_analyze:
        print(f"Starting analysis for playlist: {playlist_name}")

        # Playlist dosyasını kontrol et
        playlist_file = os.path.join(DIR_OUTPUT_FETCH, f"{playlist_name}_tracks.json")
        if not os.path.exists(playlist_file):
            print(f"Playlist file {playlist_file} does not exist. Skipping.")
            continue

        with open(playlist_file, "r", encoding="utf-8") as f:
            tracks = json.load(f)

        # Paralel işlemle şarkıları işleme
        with Pool(processes=4) as pool:
            pool.map(process_track, tracks)

        print(f"Analysis for playlist '{playlist_name}' completed.")
