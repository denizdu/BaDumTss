import pytest

from midi_creation import seconds_to_ticks


def test_one_second_at_120_bpm_is_two_beats():
    assert seconds_to_ticks(1.0, 120, 960) == 1920


def test_one_second_at_60_bpm_is_one_beat():
    assert seconds_to_ticks(1.0, 60, 960) == 960


def test_half_second_at_120_bpm_is_one_beat():
    assert seconds_to_ticks(0.5, 120, 960) == 960


@pytest.mark.parametrize("seconds,bpm,ppq", [(-1, 120, 960), (1, 0, 960), (1, 120, 0)])
def test_rejects_invalid_timing_values(seconds, bpm, ppq):
    with pytest.raises(ValueError):
        seconds_to_ticks(seconds, bpm, ppq)
