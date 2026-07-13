import numpy as np

from main_features import MAJOR_PROFILE, MINOR_PROFILE, estimate_key_from_chroma


def test_estimates_c_major_from_matching_profile():
    chroma = np.repeat(MAJOR_PROFILE[:, np.newaxis], 8, axis=1)

    key, confidence = estimate_key_from_chroma(chroma)

    assert key == "C major"
    assert confidence > 0.99


def test_estimates_a_minor_from_matching_profile():
    a_minor = np.roll(MINOR_PROFILE, 9)
    chroma = np.repeat(a_minor[:, np.newaxis], 8, axis=1)

    key, confidence = estimate_key_from_chroma(chroma)

    assert key == "A minor"
    assert confidence > 0.99


def test_returns_unknown_for_flat_chroma():
    key, confidence = estimate_key_from_chroma(np.ones((12, 4)))

    assert key == "Unknown"
    assert confidence == 0.0
