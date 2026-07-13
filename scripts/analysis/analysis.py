import sys
import os
import logging
import json
import librosa
import hashlib
from pathlib import Path
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

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def required_project_path(variable_name):
    value = os.getenv(variable_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {variable_name}")
    path = Path(value).expanduser()
    return str(path if path.is_absolute() else PROJECT_ROOT / path)

# Dizinler
DIR_DOWNLOAD = required_project_path("DIR_DOWNLOAD")
DIR_OUTPUT_FETCH = required_project_path("DIR_OUTPUT_FETCH")
PLAYLIST_TOBE_ANALYZED = os.getenv("PLAYLIST_TOBE_ANALYZED")
DIR_OUTPUT_ANALYSIS = required_project_path("DIR_OUTPUT_ANALYSIS")

if not PLAYLIST_TOBE_ANALYZED:
    raise RuntimeError("Missing required environment variable: PLAYLIST_TOBE_ANALYZED")

# Sonuç dosyası yolu
output_file = os.path.join(DIR_OUTPUT_ANALYSIS, "analysis_output.json")
partial_output_dir = os.path.join(DIR_OUTPUT_ANALYSIS, ".partial")

# Log dosyası oluştur
logging.basicConfig(filename="errors.log", level=logging.ERROR, format='%(asctime)s - %(message)s')

# Analiz dosyasının bulunduğu dizini oluştur
os.makedirs(DIR_OUTPUT_ANALYSIS, exist_ok=True)

# Playlist adlarını parse et
playlists_to_analyze = [p.strip() for p in PLAYLIST_TOBE_ANALYZED.split(",")]

# Şarkı analiz et ve ardından sil
def analyze_and_delete_song(song_file, song_output_file):
    try:
        print(f"Analyzing: {song_file}")
        # Ses dosyasını yalnızca bir kez yükle ve tüm analizlerde paylaş.
        y, sr = librosa.load(song_file, sr=None)
        process_main_features(song_file, song_output_file, y=y, sr=sr)
        process_freq_and_spectrum(song_file, song_output_file, y=y, sr=sr)
        process_rhythm(song_file, song_output_file, y=y, sr=sr)
        process_spectral_features(song_file, song_output_file, y=y, sr=sr)
        process_extra_features(song_file, song_output_file, y=y, sr=sr)
        process_drum_analysis(song_file, song_output_file, y=y, sr=sr)

        print(f"Analysis completed for: {song_file}")
        return song_output_file
    except Exception as e:
        logging.error(f"Error during analysis of {song_file}: {e}")
        return None
    finally:
        if os.path.exists(song_file):
            os.remove(song_file)
            print(f"Deleted: {song_file}")

def process_track(track):
    search_query = f"{track['name']} {track['artist']}"
    print(f"Processing song: {track['name']} by {track['artist']}")

    # Şarkıyı indirirken YouTube çerezlerini kullan
    print(f"Attempting to download: {search_query}")
    song_file = download_song_as_wav(search_query, DIR_DOWNLOAD)
    print(f"Download result: {song_file}")

    # Şarkı indirildiyse analiz et ve sil
    if song_file and os.path.exists(song_file):
        os.makedirs(partial_output_dir, exist_ok=True)
        track_key = hashlib.sha256(search_query.encode("utf-8")).hexdigest()[:16]
        song_output_file = os.path.join(partial_output_dir, f"{track_key}.json")
        if os.path.exists(song_output_file):
            os.remove(song_output_file)
        return analyze_and_delete_song(song_file, song_output_file)
    else:
        print(f"Failed to process {search_query}. Skipping.")
        logging.error(f"Failed to download or process {search_query}")
        return None


def merge_analysis_files(partial_files, destination):
    """Worker çıktılarını ana süreçte tek ve atomik bir JSON dosyasında birleştirir."""
    merged_data = {}

    if os.path.exists(destination):
        with open(destination, "r", encoding="utf-8") as f:
            merged_data = json.load(f)

    completed_files = [path for path in partial_files if path and os.path.exists(path)]
    for partial_file in completed_files:
        with open(partial_file, "r", encoding="utf-8") as f:
            merged_data.update(json.load(f))

    temporary_file = f"{destination}.tmp"
    with open(temporary_file, "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporary_file, destination)

    for partial_file in completed_files:
        os.remove(partial_file)

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
            partial_files = pool.map(process_track, tracks)

        # Birleştirme yalnızca ana süreçte yapılır; worker'lar aynı dosyaya yazmaz.
        merge_analysis_files(partial_files, output_file)

        print(f"Analysis for playlist '{playlist_name}' completed.")
