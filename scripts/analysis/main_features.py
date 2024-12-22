import librosa
import json
import os
import numpy as np

def process_main_features(song_file, output_file):
    """
    Temel özelliklerin analizi:
    - Tempo (BPM)
    - Key (Tonalite)
    - Loudness (dB)
    - Dynamics
    """
    try:
        # Şarkıyı yükle
        y, sr = librosa.load(song_file, sr=None)
        
        # Tempo (BPM)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Key (Tonalite) - Chroma features ile belirleme
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
        key = librosa.hz_to_note(chroma.argmax(axis=0).mean())

        # Loudness (dB)
        rms = librosa.feature.rms(y=y)
        loudness = 20 * np.log10(np.mean(rms))

        # Dynamics
        dynamics = float(np.max(rms) - np.min(rms))  # float32 -> float

        # Analiz sonuçlarını yaz
        results = {
            "Tempo (BPM)": float(tempo),  # float32 -> float
            "Key (Tonalite)": key,
            "Loudness (dB)": float(loudness),  # float32 -> float
            "Dynamics": dynamics
        }

        # Sonuçları JSON dosyasına ekle
        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                if song_file not in data:
                    data[song_file] = {}
                data[song_file]["Main Features"] = results
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({song_file: {"Main Features": results}}, f, indent=4)

        print(f"Main features successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing main features for {song_file}: {e}")
