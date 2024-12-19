import json
import requests
import librosa
import os
import tempfile
import re
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, error

# Deezer API bilgileri
deezer_api_url = "https://api.deezer.com/search"

# Geçici dosyalar için dizin
TEMP_DIR = tempfile.mkdtemp()

# Dosya adlarını sanitize eden fonksiyon
def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '_', name) if name else "unknown"

# Deezer API kullanarak şarkıyı indir
def download_track(track_name, artist_name):
    if not track_name or not artist_name:
        print(f"Track or artist name is missing: {track_name}, {artist_name}")
        return None
    try:
        track_url = f"{deezer_api_url}?q={track_name} {artist_name}"
        response = requests.get(track_url).json()
        if not response.get("data"):
            print(f"Track {track_name} by {artist_name} not found for download.")
            return None

        preview_url = response["data"][0].get("preview")
        if not preview_url:
            print(f"No preview available for {track_name} by {artist_name}.")
            return None

        temp_file_path = os.path.join(TEMP_DIR, sanitize_filename(f"{track_name}-{artist_name}.mp3"))
        with open(temp_file_path, "wb") as f:
            f.write(requests.get(preview_url).content)

        return temp_file_path
    except Exception as e:
        print(f"Error downloading track {track_name} by {artist_name}: {e}")
        return None

# ID3 etiketlerini temizleme
def clean_id3_tags(file_path):
    try:
        audio = MP3(file_path, ID3=ID3)
        audio.delete()
        audio.save()
        print(f"Cleaned ID3 tags for {file_path}")
    except error as e:
        print(f"Error cleaning ID3 tags for {file_path}: {e}")

# JSON uyumlu hale getirme fonksiyonu
def sanitize_for_json(data):
    if isinstance(data, dict):
        return {key: sanitize_for_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_for_json(item) for item in data]
    elif isinstance(data, float) or isinstance(data, int) or isinstance(data, str) or data is None:
        return data
    elif hasattr(data, "tolist"):  # ndarray veya benzeri yapılar için
        return data.tolist()
    else:
        return str(data)  # Diğer tüm türleri string'e çevir

# Librosa ile şarkıyı analiz et
def analyze_track(file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        energy = float(sum(librosa.feature.rms(y=y)[0]))

        chroma_mean = chroma.mean(axis=1)  # Ortalama değerler
        analysis_result = {
            "tempo": tempo,
            "energy": energy,
            "chroma_mean": chroma_mean
        }
        return analysis_result
    except Exception as e:
        print(f"Error analyzing track: {e}")
        return None

# JSON dosyasını güvenli şekilde yükle
def load_json_file(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error loading JSON file {file_path}: Invalid format. Creating a new file.")
        return []

# Şarkı analiz sürecini yönet
def process_and_analyze_tracks(input_file, cleaned_output, removed_output):
    tracks = load_json_file(input_file)

    cleaned_tracks = load_json_file(cleaned_output)
    removed_tracks = load_json_file(removed_output)

    processed_track_ids = {sanitize_filename(track.get("name", "") + track.get("artist", "")) for track in cleaned_tracks + removed_tracks}

    for track in tracks:
        track_name = track.get("name")
        artist_name = track.get("artist")

        if not track_name or not artist_name:
            print(f"Skipping track with missing name or artist: {track}")
            removed_tracks.append(track)
            continue

        if sanitize_filename(track_name + artist_name) in processed_track_ids:
            print(f"Skipping already processed track: {track_name} by {artist_name}")
            continue

        print(f"Processing track: {track_name} by {artist_name}")

        file_path = download_track(track_name, artist_name)
        if not file_path:
            removed_tracks.append(track)
            continue

        clean_id3_tags(file_path)

        analysis = analyze_track(file_path)
        os.remove(file_path)

        if analysis:
            track.update(sanitize_for_json(analysis))  # JSON uyumlu hale getirme
            cleaned_tracks.append(track)
        else:
            removed_tracks.append(track)

    os.makedirs(os.path.dirname(cleaned_output), exist_ok=True)
    os.makedirs(os.path.dirname(removed_output), exist_ok=True)

    with open(cleaned_output, "w", encoding="utf-8") as f:
        json.dump(sanitize_for_json(cleaned_tracks), f, ensure_ascii=False, indent=4)

    with open(removed_output, "w", encoding="utf-8") as f:
        json.dump(sanitize_for_json(removed_tracks), f, ensure_ascii=False, indent=4)

    print("Processing completed. Cleaned and removed tracks saved.")

if __name__ == "__main__":
    process_and_analyze_tracks(
        input_file="./output/spotify_tracks.json",
        cleaned_output="./output/cleaned/cleaned_tracks.json",
        removed_output="./output/removed/removed_tracks.json"
    )