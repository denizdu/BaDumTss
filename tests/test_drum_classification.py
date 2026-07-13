from drum_analysis import classify_drum_hit


def test_classifies_low_frequency_hit_as_kick():
    assert classify_drum_hit(0.8, 0.15, 0.05, 120) == "kick"


def test_classifies_broad_mid_frequency_hit_as_snare():
    assert classify_drum_hit(0.15, 0.65, 0.20, 2400) == "snare"


def test_classifies_bright_high_frequency_hit_as_hihat():
    assert classify_drum_hit(0.05, 0.20, 0.75, 7200) == "hihat"


def test_ignores_silent_hit():
    assert classify_drum_hit(0.0, 0.0, 0.0, 0.0) is None
