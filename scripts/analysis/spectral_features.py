import librosa
import json
import os
import numpy as np

def process_spectral_features(song_file, output_file):
    """
    Spektral özelliklerin analizi:
    - Spectral Centroid
    - Spectral Roll-off
    """
    try:
        # Şarkıyı yükle
        y, sr = librosa.load(song_file, sr=None)

        # Spectral Centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_centroid_mean = float(np.mean(spectral_centroids))

        # Spectral Roll-off
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
        spectral_rolloff_mean = float(np.mean(spectral_rolloff))

        # Analiz sonuçlarını yaz
        results = {
            "Spectral Centroid": spectral_centroid_mean,
            "Spectral Roll-off": spectral_rolloff_mean
        }

        # Sonuçları JSON dosyasına ekle
        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                if song_file not in data:
                    data[song_file] = {}
                data[song_file]["Spectral Features"] = results
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({song_file: {"Spectral Features": results}}, f, indent=4)

        print(f"Spectral features successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing spectral features for {song_file}: {e}")
