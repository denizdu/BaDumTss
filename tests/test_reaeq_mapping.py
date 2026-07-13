from pathlib import Path


CREATION_SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "creation" / "creation.lua"
)


def test_raw_fft_magnitudes_are_not_written_to_reaeq_parameters():
    script = CREATION_SCRIPT.read_text(encoding="utf-8")

    assert 'TrackFX_AddByName(track, "ReaEQ"' not in script
    assert "TrackFX_SetParam(track, 0, i - 1, value / 50)" not in script
    assert "function process_freq_and_spectrum" not in script


def test_spectral_profile_uses_centroid_and_rolloff_measurements():
    script = CREATION_SCRIPT.read_text(encoding="utf-8")

    assert "function report_spectral_profile(spectral_features)" in script
    assert 'spectral_features["Spectral Centroid"]' in script
    assert 'spectral_features["Spectral Roll-off"]' in script
    assert 'report_spectral_profile(song_data["Spectral Features"])' in script


def test_script_explains_why_automatic_eq_is_disabled():
    script = CREATION_SCRIPT.read_text(encoding="utf-8")

    assert "Automatic EQ is disabled until calibrated frequency-band data is available." in script
