import librosa
import numpy as np

from analysis_store import update_analysis_section

KEY_NAMES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")
MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def estimate_key_from_chroma(chroma):
    """Estimate a major or minor key and confidence from 12-bin chroma data."""
    if chroma.ndim != 2 or chroma.shape[0] != 12:
        raise ValueError("Chroma data must have shape (12, frames)")

    chroma_profile = np.mean(chroma, axis=1)
    if not np.all(np.isfinite(chroma_profile)) or np.allclose(chroma_profile, chroma_profile[0]):
        return "Unknown", 0.0

    candidates = []
    for root, key_name in enumerate(KEY_NAMES):
        major_score = np.corrcoef(chroma_profile, np.roll(MAJOR_PROFILE, root))[0, 1]
        minor_score = np.corrcoef(chroma_profile, np.roll(MINOR_PROFILE, root))[0, 1]
        candidates.append((float(major_score), f"{key_name} major"))
        candidates.append((float(minor_score), f"{key_name} minor"))

    score, key = max(candidates, key=lambda candidate: candidate[0])
    confidence = float(np.clip((score + 1.0) / 2.0, 0.0, 1.0))
    return key, confidence


def process_main_features(song_file, output_file, y=None, sr=None):
    """
    Analyze core audio features:
    - Tempo (BPM)
    - Key (Tonality)
    - Loudness (dB)
    - Dynamics
    """
    if y is None or sr is None:
        y, sr = librosa.load(song_file, sr=None)

    # Tempo (BPM)
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # Use the harmonic component to reduce percussion interference in key estimation.
    harmonic = librosa.effects.harmonic(y)
    chroma = librosa.feature.chroma_cqt(y=harmonic, sr=sr)
    key, key_confidence = estimate_key_from_chroma(chroma)

    # Loudness (dB)
    rms = librosa.feature.rms(y=y)
    loudness = 20 * np.log10(np.mean(rms))

    # Dynamics
    dynamics = float(np.max(rms) - np.min(rms))  # float32 -> float

    # Build the analysis result.
    results = {
        "Tempo (BPM)": float(tempo),  # float32 -> float
        "Key (Tonalite)": key,
        "Key Confidence": key_confidence,
        "Loudness (dB)": float(loudness),  # float32 -> float
        "Dynamics": dynamics,
    }

    update_analysis_section(output_file, song_file, "Main Features", results)
