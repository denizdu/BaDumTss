import json
from unittest.mock import patch

import numpy as np

import analysis


def test_audio_is_loaded_once_and_shared_with_all_processors(tmp_path):
    song_file = tmp_path / "song.wav"
    song_file.write_bytes(b"placeholder")
    partial_output = tmp_path / "partial.json"
    y = np.array([0.1, -0.1, 0.0])
    processors = [
        "process_main_features",
        "process_freq_and_spectrum",
        "process_rhythm",
        "process_spectral_features",
        "process_extra_features",
        "process_drum_analysis",
    ]

    with patch.object(analysis.librosa, "load", return_value=(y, 44100)) as load_audio:
        processor_mocks = [patch.object(analysis, name) for name in processors]
        started_mocks = [mock.start() for mock in processor_mocks]
        try:
            result = analysis.analyze_and_delete_song(str(song_file), str(partial_output))
        finally:
            for mock in processor_mocks:
                mock.stop()

    assert result == str(partial_output)
    load_audio.assert_called_once_with(str(song_file), sr=None)
    for processor_mock in started_mocks:
        processor_mock.assert_called_once()
        assert processor_mock.call_args.kwargs["y"] is y
        assert processor_mock.call_args.kwargs["sr"] == 44100
    assert not song_file.exists()


def test_partial_analysis_files_are_merged_and_removed(tmp_path):
    destination = tmp_path / "analysis_output.json"
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    destination.write_text(json.dumps({"existing": {"value": 1}}), encoding="utf-8")
    first.write_text(json.dumps({"song-a": {"tempo": 90}}), encoding="utf-8")
    second.write_text(json.dumps({"song-b": {"tempo": 120}}), encoding="utf-8")

    analysis.merge_analysis_files([str(first), None, str(second)], str(destination))

    merged = json.loads(destination.read_text(encoding="utf-8"))
    assert merged == {
        "existing": {"value": 1},
        "song-a": {"tempo": 90},
        "song-b": {"tempo": 120},
    }
    assert not first.exists()
    assert not second.exists()
    assert not (tmp_path / "analysis_output.json.tmp").exists()
