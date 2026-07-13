import importlib
from types import SimpleNamespace
from unittest.mock import patch

import pytest

import analysis


PROCESSORS = (
    ("main_features", "process_main_features"),
    ("freq_and_spectrum", "process_freq_and_spectrum"),
    ("rhythm", "process_rhythm"),
    ("spectral_features", "process_spectral_features"),
    ("extra_features", "process_extra_features"),
    ("drum_analysis", "process_drum_analysis"),
)


@pytest.mark.parametrize("module_name,function_name", PROCESSORS)
def test_analysis_processors_propagate_audio_loading_errors(module_name, function_name):
    module = importlib.import_module(module_name)
    processor = getattr(module, function_name)

    with patch.object(module.librosa, "load", side_effect=OSError("unreadable audio")):
        with pytest.raises(OSError, match="unreadable audio"):
            processor("broken.wav", "analysis.json")


def test_analysis_failure_has_context_and_removes_temporary_audio(tmp_path):
    song_file = tmp_path / "broken.wav"
    song_file.write_bytes(b"invalid")

    with patch.object(analysis.librosa, "load", side_effect=OSError("bad codec")):
        with pytest.raises(analysis.AnalysisPipelineError) as raised:
            analysis.analyze_and_delete_song(song_file, tmp_path / "partial.json")

    assert str(song_file) in str(raised.value)
    assert isinstance(raised.value.__cause__, OSError)
    assert not song_file.exists()


def test_audio_source_resolution_failure_is_not_skipped(tmp_path):
    config = SimpleNamespace(download_dir=tmp_path)
    track = {"name": "Missing", "artist": "Track"}

    with patch.object(
        analysis,
        "resolve_audio_source",
        side_effect=FileNotFoundError("source missing"),
    ):
        with pytest.raises(analysis.AnalysisPipelineError) as raised:
            analysis.process_track(track, config)

    assert "Missing Track" in str(raised.value)
    assert isinstance(raised.value.__cause__, FileNotFoundError)


def test_missing_playlist_is_not_silently_skipped(tmp_path):
    config = analysis.AnalysisConfig(
        download_dir=tmp_path / "downloads",
        fetch_output_dir=tmp_path / "fetch",
        analysis_output_dir=tmp_path / "analysis",
        playlists=("missing",),
    )

    with pytest.raises(FileNotFoundError, match="missing_tracks.json"):
        analysis.run_pipeline(config, worker_count=1)
