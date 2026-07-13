import librosa
import numpy as np

from analysis_store import update_analysis_section


def classify_drum_hit(low_energy, mid_energy, high_energy, spectral_centroid):
    """Classify a transient by frequency-band energy and spectral centroid."""
    total_energy = low_energy + mid_energy + high_energy
    if total_energy <= np.finfo(float).eps:
        return None

    low_ratio = low_energy / total_energy
    high_ratio = high_energy / total_energy

    if low_ratio >= 0.45 or (low_energy > mid_energy * 1.25 and low_energy > high_energy * 1.5):
        return "kick"
    if high_ratio >= 0.45 and spectral_centroid >= 4500:
        return "hihat"
    return "snare"


def _mean_band_energy(spectrum, frequencies, minimum, maximum):
    band = (frequencies >= minimum) & (frequencies < maximum)
    return float(np.mean(spectrum[band])) if np.any(band) else 0.0


def process_drum_analysis(song_file, output_file, y=None, sr=None):
    """Detect transients and classify kick, snare, and hi-hat candidates."""
    if y is None or sr is None:
        y, sr = librosa.load(song_file, sr=None)

    percussive = librosa.effects.percussive(y)
    onset_env = librosa.onset.onset_strength(y=percussive, sr=sr, aggregate=np.median)
    onset_frames = librosa.onset.onset_detect(
        onset_envelope=onset_env,
        sr=sr,
        units="frames",
        backtrack=False,
    )
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    magnitude = np.abs(librosa.stft(percussive))
    frequencies = librosa.fft_frequencies(sr=sr)
    positions = {"kick": [], "snare": [], "hihat": []}

    for frame in onset_frames:
        start = max(0, int(frame) - 1)
        stop = min(magnitude.shape[1], int(frame) + 2)
        hit_spectrum = np.mean(magnitude[:, start:stop], axis=1)

        low_energy = _mean_band_energy(hit_spectrum, frequencies, 20, 180)
        mid_energy = _mean_band_energy(hit_spectrum, frequencies, 180, 5000)
        high_energy = _mean_band_energy(hit_spectrum, frequencies, 5000, sr / 2)
        energy_sum = float(np.sum(hit_spectrum))
        spectral_centroid = (
            float(np.sum(frequencies * hit_spectrum) / energy_sum)
            if energy_sum > np.finfo(float).eps
            else 0.0
        )

        drum_type = classify_drum_hit(
            low_energy,
            mid_energy,
            high_energy,
            spectral_centroid,
        )
        if drum_type:
            position = float(librosa.frames_to_time(frame, sr=sr))
            positions[drum_type].append(position)

    results = {
        "Tempo (BPM)": float(np.asarray(tempo).reshape(-1)[0]),
        "Beat Grid": beat_times.tolist(),
        "Kick Positions": positions["kick"],
        "Snare Positions": positions["snare"],
        "HiHat Positions": positions["hihat"],
        "Detected Onsets": int(len(onset_frames)),
        "Detection Method": "percussive onset frequency bands v1",
    }

    update_analysis_section(output_file, song_file, "Drum Analysis", results)
