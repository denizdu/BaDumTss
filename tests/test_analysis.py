import pytest
import json
import os
import numpy as np
from unittest.mock import patch, mock_open
from extra_features import process_extra_features
from derived_features import process_derived_features
from drum_analysis import process_drum_analysis

@pytest.fixture
def mock_librosa_load():
    with patch("librosa.load") as mock_load:
        mock_load.return_value = (np.random.rand(22050 * 30), 22050)  # 30 saniyelik sahte bir ses
        yield mock_load

@patch("builtins.open", new_callable=mock_open)
def test_process_extra_features_success(mock_open_file, mock_librosa_load):
    output_file = "test_output.json"
    song_file = "test_song.wav"

    # Test edilen fonksiyonu çalıştır
    process_extra_features(song_file, output_file)

    # JSON dosyası içerik kontrolü
    mock_open_file.assert_called_with(output_file, "w", encoding="utf-8")
    written_data = "".join(call.args[0] for call in mock_open_file().write.call_args_list)  # Yazılan veri

    try:
        parsed_data = json.loads(written_data)
        assert song_file in parsed_data
        assert "Extra Features" in parsed_data[song_file]
        assert "MFCCs" in parsed_data[song_file]["Extra Features"]
        assert "Zero-Crossing Rate" in parsed_data[song_file]["Extra Features"]
    except json.JSONDecodeError:
        print(f"Invalid JSON format: {written_data}")
        raise

@patch("builtins.open", new_callable=mock_open)
def test_process_drum_analysis_success(mock_open_file, mock_librosa_load):
    output_file = "test_output.json"
    song_file = "test_song.wav"

    # Test edilen fonksiyonu çalıştır
    process_drum_analysis(song_file, output_file)

    # JSON dosyası içerik kontrolü
    mock_open_file.assert_called_with(output_file, "w", encoding="utf-8")
    written_data = "".join(call.args[0] for call in mock_open_file().write.call_args_list)  # Yazılan veri

    try:
        parsed_data = json.loads(written_data)
        assert song_file in parsed_data
        assert "Drum Analysis" in parsed_data[song_file]
        assert "Tempo (BPM)" in parsed_data[song_file]["Drum Analysis"]
        assert "Kick Positions" in parsed_data[song_file]["Drum Analysis"]
        assert "Snare Positions" in parsed_data[song_file]["Drum Analysis"]
        assert "HiHat Positions" in parsed_data[song_file]["Drum Analysis"]
    except json.JSONDecodeError:
        print(f"Invalid JSON format: {written_data}")
        raise

def test_process_derived_features_success():
    song_file = "test_song.wav"

    # Test edilen fonksiyonu çalıştır
    with patch("builtins.print") as mock_print:
        process_derived_features(song_file)
        mock_print.assert_called_with(f"Processing derived features for {song_file}")
