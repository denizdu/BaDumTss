import librosa
import numpy as np

from analysis_store import update_analysis_section

def process_freq_and_spectrum(song_file, output_file, y=None, sr=None):
    """
    Analyze frequency and spectrum features:
    - Frequency Spectrum
    - Melody Contour
    - Harmonic Content
    """
    if y is None or sr is None:
        y, sr = librosa.load(song_file, sr=None)

    # Frequency spectrum (power spectrum).
    spectrum = np.abs(librosa.stft(y))
    freq_spectrum = np.mean(spectrum, axis=1).tolist()

    # Melody Contour (Pitch Tracking)
    pitches, _ = librosa.piptrack(y=y, sr=sr)
    melody_contour = [float(np.max(pitches[:, i])) for i in range(pitches.shape[1])]

    # Harmonic Content (Harmonic-percussive source separation)
    harmonic, _ = librosa.effects.hpss(y)
    harmonic_content = np.mean(np.abs(harmonic)).tolist()

    results = {
        "Frequency Spectrum": freq_spectrum[:10],
        "Melody Contour": melody_contour[:10],
        "Harmonic Content": harmonic_content,
    }

    update_analysis_section(output_file, song_file, "Frequency and Spectrum", results)
