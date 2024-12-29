import librosa
import json
import os
import numpy as np

def process_drum_analysis(song_file, output_file):
    """ bla bla """
    try:
        # Şarkıyı yükle
        y, sr = librosa.load(song_file, sr=None)

        # onset_strength argümanlarını doğru şekilde düzenliyoruz
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, aggregate=np.median)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
        beat_times = librosa.frames_to_time(beats, sr=sr)

        # Kick, Snare, HiHat tahminleri
        kick_positions = beat_times[::4]
        snare_positions = beat_times[1::4]
        hihat_positions = beat_times[2::4]

        results = {
            "Tempo (BPM)": tempo,
            "Beat Grid": beat_times.tolist(),
            "Kick Positions": kick_positions.tolist(),
            "Snare Positions": snare_positions.tolist(),
            "HiHat Positions": hihat_positions.tolist()
        }

        # Sonuçları JSON dosyasına ekle
        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                if song_file not in data:
                    data[song_file] = {}
                data[song_file]["Drum Analysis"] = results
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({song_file: {"Extra Features": results}}, f, indent=4)

        print(f"Drum analysis successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing drum analysis for {song_file}: {e}")
