import librosa
import json
import os
import numpy as np

def process_extra_features(song_file, output_file):
    """
    Daha karmaşık özelliklerin analizi:
    - MFCCs (Mel-Frequency Cepstral Coefficients)
    - Zero-Crossing Rate
    """
    try:
        # Şarkıyı yükle
        y, sr = librosa.load(song_file, sr=None)

        # MFCCs (Mel-Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # İlk 13 MFCC katsayısını hesaplar
        mfccs_mean = np.mean(mfccs, axis=1).tolist()

        # Zero-Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = float(np.mean(zcr))

        # Analiz sonuçlarını yaz
        results = {
            "MFCCs": mfccs_mean,
            "Zero-Crossing Rate": zcr_mean
        }

        # Sonuçları JSON dosyasına ekle
        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                if song_file not in data:
                    data[song_file] = {}
                data[song_file]["Extra Features"] = results
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({song_file: {"Extra Features": results}}, f, indent=4)

        print(f"Extra features successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing extra features for {song_file}: {e}")
