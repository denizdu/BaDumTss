import librosa
import json
import os
import numpy as np

def process_freq_and_spectrum(song_file, output_file):
    """
    Frekans ve spektrum analizi:
    - Frekans Spektrumu
    - Melody Contour
    - Harmonic Content
    """
    try:
        # Şarkıyı yükle
        y, sr = librosa.load(song_file, sr=None)
        
        # Frekans Spektrumu (Power Spectrum)
        spectrum = np.abs(librosa.stft(y))
        freq_spectrum = np.mean(spectrum, axis=1).tolist()  # Ortalama güç değerleri

        # Melody Contour (Pitch Tracking)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        melody_contour = [float(np.max(pitches[:, i])) for i in range(pitches.shape[1])]  # Zaman içindeki en güçlü pitch

        # Harmonic Content (Harmonic-percussive source separation)
        harmonic, _ = librosa.effects.hpss(y)
        harmonic_content = np.mean(np.abs(harmonic)).tolist()

        # Analiz sonuçlarını yaz
        results = {
            "Frequency Spectrum": freq_spectrum[:10],  # İlk 10 frekansın yoğunluğu (örnek)
            "Melody Contour": melody_contour[:10],     # İlk 10 zaman dilimindeki melody contour (örnek)
            "Harmonic Content": harmonic_content
        }

        # Sonuçları JSON dosyasına ekle
        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                if song_file not in data:
                    data[song_file] = {}
                data[song_file]["Frequency and Spectrum"] = results
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({song_file: {"Frequency and Spectrum": results}}, f, indent=4)

        print(f"Frequency and spectrum analysis successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing frequency and spectrum for {song_file}: {e}")
