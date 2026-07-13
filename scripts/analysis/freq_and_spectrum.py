import librosa
import json
import os
import numpy as np

def process_freq_and_spectrum(song_file, output_file, y=None, sr=None):
    """
    Analyze frequency and spectrum features:
    - Frequency Spectrum
    - Melody Contour
    - Harmonic Content
    """
    try:
        if y is None or sr is None:
            y, sr = librosa.load(song_file, sr=None)
        
        # Frequency spectrum (power spectrum).
        spectrum = np.abs(librosa.stft(y))
        freq_spectrum = np.mean(spectrum, axis=1).tolist()  # Average power values.

        # Melody Contour (Pitch Tracking)
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        melody_contour = [float(np.max(pitches[:, i])) for i in range(pitches.shape[1])]  # Strongest pitch over time.

        # Harmonic Content (Harmonic-percussive source separation)
        harmonic, _ = librosa.effects.hpss(y)
        harmonic_content = np.mean(np.abs(harmonic)).tolist()

        # Build the analysis result.
        results = {
            "Frequency Spectrum": freq_spectrum[:10],  # Example: intensity of the first 10 frequency bins.
            "Melody Contour": melody_contour[:10],     # Example: contour for the first 10 time frames.
            "Harmonic Content": harmonic_content
        }

        # Append the results to the JSON file.
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
