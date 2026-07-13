import json
from unittest.mock import patch

import numpy as np

from derived_features import process_derived_features
from drum_analysis import process_drum_analysis
from extra_features import process_extra_features


def test_process_extra_features_success(tmp_path):
    output_file = tmp_path / "extra.json"
    song_file = "test_song.wav"
    y = np.random.default_rng(1).random(22050)

    process_extra_features(song_file, str(output_file), y=y, sr=22050)

    parsed_data = json.loads(output_file.read_text(encoding="utf-8"))
    assert "MFCCs" in parsed_data[song_file]["Extra Features"]
    assert "Zero-Crossing Rate" in parsed_data[song_file]["Extra Features"]


def test_process_drum_analysis_success(tmp_path):
    output_file = tmp_path / "drums.json"
    song_file = "test_song.wav"
    y = np.zeros(22050)
    y[::5512] = 1.0

    process_drum_analysis(song_file, str(output_file), y=y, sr=22050)

    parsed_data = json.loads(output_file.read_text(encoding="utf-8"))
    drum_data = parsed_data[song_file]["Drum Analysis"]
    assert "Tempo (BPM)" in drum_data
    assert "Kick Positions" in drum_data
    assert "Snare Positions" in drum_data
    assert "HiHat Positions" in drum_data


def test_process_derived_features_success():
    song_file = "test_song.wav"

    with patch("builtins.print") as mock_print:
        process_derived_features(song_file)
        mock_print.assert_called_with(f"Processing derived features for {song_file}")
