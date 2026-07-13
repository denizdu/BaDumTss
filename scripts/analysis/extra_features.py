import librosa
import numpy as np

from analysis_store import update_analysis_section

def process_extra_features(song_file, output_file, y=None, sr=None):
    """
    Analyze higher-level audio features:
    - MFCCs (Mel-Frequency Cepstral Coefficients)
    - Zero-Crossing Rate
    """
    try:
        if y is None or sr is None:
            y, sr = librosa.load(song_file, sr=None)

        # MFCCs (Mel-Frequency Cepstral Coefficients)
        mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)  # Calculate the first 13 MFCC coefficients.
        mfccs_mean = np.mean(mfccs, axis=1).tolist()

        # Zero-Crossing Rate
        zcr = librosa.feature.zero_crossing_rate(y)
        zcr_mean = float(np.mean(zcr))

        # Build the analysis result.
        results = {
            "MFCCs": mfccs_mean,
            "Zero-Crossing Rate": zcr_mean
        }

        update_analysis_section(output_file, song_file, "Extra Features", results)

        print(f"Extra features successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing extra features for {song_file}: {e}")
