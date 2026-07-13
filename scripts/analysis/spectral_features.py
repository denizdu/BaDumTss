import librosa
import numpy as np

from analysis_store import update_analysis_section

def process_spectral_features(song_file, output_file, y=None, sr=None):
    """
    Analyze spectral features:
    - Spectral Centroid
    - Spectral Roll-off
    """
    if y is None or sr is None:
        y, sr = librosa.load(song_file, sr=None)

    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    spectral_centroid_mean = float(np.mean(spectral_centroids))

    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)
    spectral_rolloff_mean = float(np.mean(spectral_rolloff))

    results = {
        "Spectral Centroid": spectral_centroid_mean,
        "Spectral Roll-off": spectral_rolloff_mean,
    }

    update_analysis_section(output_file, song_file, "Spectral Features", results)
