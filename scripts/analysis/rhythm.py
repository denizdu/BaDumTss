import librosa
import json
import os
import numpy as np

def process_rhythm(song_file, output_file, y=None, sr=None):
    """
    Analyze rhythm features:
    - Beat Grid
    - Swing
    """
    try:
        if y is None or sr is None:
            y, sr = librosa.load(song_file, sr=None)
        
        # Beat Grid
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr).tolist()

        # Swing (rhythmic variation).
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        swing_variation = float(np.std(onset_env))  # Use standard deviation as rhythmic variation.

        # Build the analysis result.
        results = {
            "Beat Grid": beat_times[:10],  # Example: timestamps of the first 10 beats.
            "Swing": swing_variation
        }

        # Append the results to the JSON file.
        if os.path.exists(output_file):
            with open(output_file, "r+", encoding="utf-8") as f:
                data = json.load(f)
                if song_file not in data:
                    data[song_file] = {}
                data[song_file]["Rhythm"] = results
                f.seek(0)
                json.dump(data, f, indent=4)
        else:
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({song_file: {"Rhythm": results}}, f, indent=4)

        print(f"Rhythm analysis successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing rhythm for {song_file}: {e}")
