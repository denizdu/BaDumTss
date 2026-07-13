import librosa
import numpy as np

from analysis_store import update_analysis_section

def process_rhythm(song_file, output_file, y=None, sr=None):
    """
    Analyze rhythm features:
    - Beat Grid
    - Swing
    """
    if y is None or sr is None:
        y, sr = librosa.load(song_file, sr=None)

    # Beat Grid
    _, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()

    # Swing (rhythmic variation).
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    swing_variation = float(np.std(onset_env))

    results = {"Beat Grid": beat_times[:10], "Swing": swing_variation}

    update_analysis_section(output_file, song_file, "Rhythm", results)
