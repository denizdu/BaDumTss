import librosa
import numpy as np

from analysis_store import update_analysis_section

def process_spectral_features(song_file, output_file, y=None, sr=None):
    """
    Analyze spectral features:
    - Spectral Centroid
    - Spectral Roll-off
    """
    try:
        if y is None or sr is None:
            y, sr = librosa.load(song_file, sr=None)

        # Spectral Centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
        spectral_centroid_mean = float(np.mean(spectral_centroids))

        # Spectral Roll-off
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
        spectral_rolloff_mean = float(np.mean(spectral_rolloff))

        # Build the analysis result.
        results = {
            "Spectral Centroid": spectral_centroid_mean,
            "Spectral Roll-off": spectral_rolloff_mean
        }

        update_analysis_section(output_file, song_file, "Spectral Features", results)

        print(f"Spectral features successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing spectral features for {song_file}: {e}")
