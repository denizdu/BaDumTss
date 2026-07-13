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

        update_analysis_section(
            output_file, song_file, "Frequency and Spectrum", results
        )

        print(f"Frequency and spectrum analysis successfully processed for {song_file}")

    except Exception as e:
        print(f"Error processing frequency and spectrum for {song_file}: {e}")
